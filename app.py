import requests
from flask import redirect, request
from flask_openapi3 import Info, OpenAPI, Tag, Header
from schema import CreateOrderSchema, SearchStockSchema, GetOrderById, SellStockSchema, GetUserByIdSchema, \
    CreateUserSchema, EditUserSchema, FilterOrderByUser, GetUserAuthenticationToken

from helpers import authenticate, get_user_id

# Gateway config
info = Info(title="Project Home Broker -  Gateway", version="1.0.0")

# JWT Bearer Sample
jwt = {
  "type": "http",
  "scheme": "bearer",
  "bearerFormat": "JWT"
}

security_schemes = {"jwt": jwt}

app = OpenAPI(__name__, info=info, security_schemes=security_schemes)

# Tags for documentation
home_tag = Tag(name="Documentation - Gateway", description="Select doc: Swagger, Redoc")
gateway_tag = Tag(name="Gateway")
orders_tag = Tag(name="Orders Service")
stocks_tag = Tag(name="Stocks Service")
users_tag = Tag(name="Users Service")


ORDER_SERVICE_URL = "http://127.0.0.1:5000"
STOCK_SERVICE_URL = "http://127.0.0.1:5001"
USER_SERVICE_URL = "http://127.0.0.1:8000"

security = [
    {"jwt": []}
]


@app.get("/", tags=[home_tag])
def home():
    return redirect('/openapi')


# STOCK SERVICE:
@app.get("/stock", tags=[stocks_tag])
def get_stock(query: SearchStockSchema):

    # Stock's symbol
    symbol = query.symbol

    try:
        # Request to Stock Service to retrieve stocks information
        stock_request = requests.get(STOCK_SERVICE_URL + "/stock", params={"symbol": symbol})

        # Check if Stock Service returned a 404 status code (not found)
        if stock_request.status_code == 404:
            return {"error": "Stock information not available"}

        stock_data = stock_request.json()
    except requests.exceptions.ConnectionError:
        return "Stock Service encounter an error"

    return {"message": f"Stock data: {stock_data}"}


# ORDER SERVICE:
@app.get("/order/user", security=security, tags=[orders_tag])
def filter_order_by_user():

    url = ORDER_SERVICE_URL + "/order/user"

    try:
        # Authenticate user
        auth_req = authenticate()
        auth_req.raise_for_status()

        # Get authenticated user id
        user_id = get_user_id()

        # Request to filter orders by user id
        filter_transactions_by_user_request = requests.get(url=url, params={"user_id": user_id})
        filter_transactions_by_user_request.raise_for_status()
        user_transactions = filter_transactions_by_user_request.json()

        return {
            "message": "User's transactions",
            "user_transactions": user_transactions
        }, 200

    except requests.exceptions.HTTPError as e:

        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "Order Service unavailable", 503


@app.get("/order", tags=[orders_tag])
def get_order_by_id(query: GetOrderById):
    order_id = query.order_id

    url = ORDER_SERVICE_URL + "/order"

    try:
        req = requests.get(url=url, params={"id": order_id})
        if req.status_code == 404:
            return {"error": "Stock information not available"}

        order_data = req.json()
        print(order_data)

    except requests.exceptions.ConnectionError:
        return "Order Service unavailable"

    return {"Order": f"{order_data}"}


@app.post("/order/create", security=security, tags=[orders_tag])
def create_orders(form: CreateOrderSchema):

    url = ORDER_SERVICE_URL + "/order/create"

    try:
        # Authenticate user
        auth_response = authenticate()
        auth_response.raise_for_status()

        # Get authenticated user ID
        user_id = get_user_id()

        # Data for order request
        data = {
            "stock_symbol": form.stock_symbol,
            "quantity": form.quantity,
            "user_id": user_id
        }

        # Send request to Order Service
        order_request = requests.post(url=url, data=data)
        order_response = order_request.json()

        return {
            "message": "Successfully bought stocks",
            "order_transaction_details": order_response
        }, 200

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "Order Service unavailable", 503


@app.post("/order/sell", security=security, tags=[orders_tag])
def sell_stocks(form: SellStockSchema):

    url = ORDER_SERVICE_URL + "/order/sell"

    try:
        # Authenticate user
        auth_response = authenticate()
        auth_response.raise_for_status()

        # Get authenticated user ID
        user_id = get_user_id()

        # Data for sell request
        data = {
            "stock_symbol": form.stock_symbol,
            "quantity": form.quantity,
            "user_id": user_id
        }

        # Send request to Order Service
        req = requests.post(url=url, data=data)
        req.raise_for_status()
        transaction_sell = req.json()

        return {
            "message": "Successfully sold stocks",
            "sold_transaction_details": transaction_sell
        }, 200

    except requests.exceptions.HTTPError as e:

        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "Order Service unavailable", 503


# USER SERVICE
@app.post("/user/token", tags=[users_tag])
def get_user_token(form: GetUserAuthenticationToken):

    url = USER_SERVICE_URL + "/api/token/"

    try:
        # Data for token request
        data = {
            "username": form.email,
            "password": form.password
        }

        # Send request to User Service
        user_token_request = requests.post(url=url, data=data)
        user_token_request.raise_for_status()
        token = user_token_request.json()

        return {"message": token['access']}, 200

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503


@app.get("/user", security=security, tags=[users_tag])
def get_user():

    response = authenticate()
    user_details = response.json()

    return user_details, 200


@app.post("/user/create", tags=[users_tag])
def create_user(form: CreateUserSchema):

    url = "http://127.0.0.1:8000/user/create/"

    try:
        # Data for register user
        data = {
            "email": form.email,
            "password": form.password
        }
        # Send request to User Service
        register_user_request = requests.post(url=url, json=data)
        register_user_request.raise_for_status()

        created_user = register_user_request.json()

        return {
            "message": "Successfully created user",
            "created_user": created_user
        }, 200

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503


@app.delete("/user/delete", security=security, tags=[users_tag])
def delete_user():

    try:
        # Authenticate user
        auth_req = authenticate()
        auth_req.raise_for_status()

        # Get authenticated user id
        user_id = get_user_id()

        url = USER_SERVICE_URL + f"/user/create/{user_id}"

        # Request to delete authenticated user
        delete_user_request = requests.delete(url=url)
        delete_user_request.raise_for_status()

        return {
            "message": "Successfully deleted user",
        }, 200

    except requests.exceptions.HTTPError as e:

        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503


@app.put("/user/edit", security=security, tags=[users_tag])
def edit_user(form: EditUserSchema):

    email = form.email
    username = form.email
    password = form.password

    # Data for edit user request
    data = {
        "email": email,
        "username": username,
        "password": password
    }

    try:
        # Authenticate user
        auth_req = authenticate()
        auth_req.raise_for_status()

        # Get authenticated user ID
        user_id = get_user_id()

        url = USER_SERVICE_URL + f"/user/create/{user_id}/"

        # Request to edit authenticated user
        edit_user_request = requests.put(url=url, json=data)
        edit_user_request.raise_for_status()

        user_edited = edit_user_request.json()

        return {
            "message": "Successfully edited user",
            "user_edited": user_edited
        }, 200

    except requests.exceptions.HTTPError as e:

        status_code = e.response.status_code
        error_message = e.response.text

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503
