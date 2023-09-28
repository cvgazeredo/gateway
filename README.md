# MVP 03 - Project HomeBroker 

Projeto de uma aplicação responsavel por comprar e vender ações.

---

## Componente A: Gateway
 + Atua como um intermediário entre os serviços e os clientes, direcionando as solicitações;
 + Roteia as solicitações dos usuários para os serviços apropriados com base nos endpoints definidos.

Este projeto utiliza uma API externa, sendo necessário uma API KEY. As intruções 
para uso estão no [Serviço de Stocks](https://github.com/cvgazeredo/stocks_service).

Os serviços acessados pelo Gateway são:

- [Seriço de Orders](https://github.com/cvgazeredo/orders_service);
- [Serviço de Stocks](https://github.com/cvgazeredo/stocks_service);
- [Serviço de Autenticação de Usuário](https://github.com/cvgazeredo/user_authentication_service);


### Criação de usuário e autenticação:

+ Use o endpoint **/user/create** para registrar um novo usuário;
+ Fornça um endereço de e-mail e uma senha;
+ O serviço de Usuários criará uma conta e retornará uma confirmação de sucesso.

#### Autenticação com Token:

+ Use o endpoint **/user/token** para autenticar um usuário;
+ Forneça um endereço de e-mail e a senha correspondente;
+ O serviço de usuários gerará e retornará um token de acesso válido;
+ Após a autenticação, o usuário poderá acessar recursos protegidos.
No OpenAPI (Swagger), haverá cadeados ao lado de endpoints protegidos.
Para acessar esses endpoints, clique em "Authorize" e insira o token de acesso.


---
### Execução através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) 
instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
docker build -t gateway .
```

Caso nao esteja criada, execute o comando abaixo, para a criação de uma nova
network:

```
docker network create <my_network> 
```

Para a execução o container basta executar, **como administrador**, seguinte o comando:
```
docker run -p 5002:5002 --name gateway --network <my_network> gateway
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5002](http://localhost:5002) no navegador.
