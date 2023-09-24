from pydantic import BaseModel


# Stocks Schemas:
class SearchStockSchema(BaseModel):
    symbol: str


# Oder Schemas:
class CreateOrderSchema(BaseModel):
    stock_symbol: str
    quantity: int


class GetOrderById(BaseModel):
    order_id: int


class SellStockSchema(BaseModel):
    stock_symbol: str
    quantity: int


# User Schemas
class GetUserByIdSchema(BaseModel):
    id: str


class CreateUserSchema(BaseModel):
    email: str
    password: str


class EditUserSchema(BaseModel):
    email: str
    password: str


class FilterOrderByUser(BaseModel):
    user_id: int


class GetUserAuthenticationToken(BaseModel):
    email: str
    password: str



