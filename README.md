# apiloanspayments
Apiloanspayments, es un proyecto desarrollado en Django que ofrece una API para gestionar préstamos y pagos de clientes. Permite crear, obtener y realizar pagos en préstamos activos, así como consultar el balance de un cliente. El proyecto utiliza el framework Django Rest Framework para proporcionar una API RESTful segura y autenticada mediante tokens.

## Despliegue en Docker
### Paso 1
Clonar el repositorio

#### git clone https://github.com/saenz03/apiloanspayments.gi

### Paso 2
Asumiendo que ya tengas instalado docker en tu equipo, en la termina situarse en la ruta del proyecto construir y correr el docker.
- docker build -t app/apiloanspayments/ .
- docker run -p 8000:8000 app/apiloanspayments


# Uso API
Una vez se construya el docker , puedes acceder a la API y al panel de administración utilizando la URL proporcionada en la terminal.

## API Endpoints

-----------------KEY--------------------
### Crear usuario

curl -X POST http://127.0.0.1:8000/api/registration/ -d "password1=loan1234JUAN&password2=loan1234JUAN&email=test90@test90.com&username=customer90

### Autenticarse para obtener key

curl -X POST http://127.0.0.1:8000/api/auth/login/ -d "password=loan1234JUAN&email=test90@test90.com&username=customer90"

key: 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954

---------------------------------------
### Crear cliente

curl -X POST http://127.0.0.1:8000/api/v1/customer/ -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954" -d "external_id=111&status=1&score=1000&preapproved_at=2023-07-20T17:44:00Z"

### Consultar cliente

curl -X GET http://127.0.0.1:8000/api/v1/customer/ -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954"

---------------------------------------

### Obtener el balance

curl -X GET "http://127.0.0.1:8000/api/v1/balance/?external_id=111" -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954"

---------------------------------------

### Crear prestamo

curl -X POST http://127.0.0.1:8000/api/v1/loan/ -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954" -d "external_id=112p&customer_id=111&status=2&amount=100&outstanding=100"

### Consultar prestamo

curl -X GET "http://127.0.0.1:8000/api/v1/loan/?external_id=111p" -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954"

---------------------------------------
### Crear pago

curl -X POST http://127.0.0.1:8000/api/v1/payment/ -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954" -d "customer_id=111p&total_amount=100"

### consultar el pago

curl -X GET "http://127.0.0.1:8000/api/v1/payment/?customer_id=111" -H "Authorization: Token 9c94a4fe8369f2fb3f99eebcee2c0fe445ed0954"

# Créditos
Este proyecto fue desarrollado por Juan Sebastian Chaparro Saenz.
