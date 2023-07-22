from .models import loan, customer, payment, paymentdetail
from .serializers import loanserializer, customerserializer, paymentserializer, paymentdetail_serializer

from rest_framework import viewsets, views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models

class BalanceView(views.APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request):
        """
        Endpoint que permite obtener el balance del cliente, para ello requeire autenticacion mediante 
        TokenAuthentication y permiso de autenticado mediante IsAuthenticated.

        Esta vista toma el 'external_id' del cliente desde los parámetros de la consulta (query_params)
        de la solicitud y valida si el parámetro está presente. Si no se proporciona el 'external_id',
        se devuelve una respuesta con un mensaje de error y el código de estado 400. Luego,
        intenta buscar al cliente en la base de datos utilizando el 'external_id' proporcionado. Si no se
        encuentra ningún cliente con el 'external_id' dado, se devuelve una respuesta con un mensaje de
        error y el código de estado 404 (NOT FOUND). Si se encuentra el cliente, se calcula su balance
        sumando todos los montos pendientes de los préstamos activos y pendientes asociados a él, y luego
        se resta este valor de su puntuación ('score'). Finalmente, se devuelve una respuesta con el balance
        del cliente y los detalles adicionales en formato JSON con el código de estado 200 (OK).

        Respuesta: 
        Devuelve un JSON con el detalle del balance y el cliente.
        """  
        external_id = request.query_params.get('external_id')
        #validacion del parametro obligatorio para la peticion
        if not external_id:
            return Response({"error": "Se requiere el parámetro 'external_id'."}, status=400)
        try:
            customeri = customer.objects.get(external_id=external_id)
            #validacion de la existencia del cliente con el parametro solicitado
        except customer.DoesNotExist:
            return Response({"error": "No hay cliente con el external_id proporcionado."}, status=404)

        response_data = {
            "external_id": customeri.external_id,
            "score": customeri.score,
        }
        #calculo para obtener la suma de los outstanding de todos los prestamos pendiente y activos
        total_debt = loan.objects.filter(customer_id=customeri, status=1).aggregate(sum_debt=models.Sum('outstanding'))['sum_debt'] or 0
        #calculo para obtener el monto disponible
        available_amount = customeri.score - total_debt

        response_data["available_amount"] = available_amount
        response_data["total_debt"] = total_debt

        return Response(response_data) # response del balance del cliente
  
class CustomerView(views.APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]
   
   def post(self, request):
        """
        Endpoint que permite crear un cliente, para ello requeire autenticacion mediante 
        TokenAuthentication y permiso de autenticado mediante IsAuthenticated.

        Esta vista toma los datos del cliente desde el cuerpo de la solicitud (request.data),
        deserializa los datos utilizando el serializador 'customerserializer' y valida si el
        'external_id' del cliente ya existe en la base de datos. Si el 'external_id' ya existe,
        se devuelve una respuesta con un mensaje de error (409).
        Si el 'external_id' no existe y el campo 'status' del cliente es igual a 1 ('activo'),
        se guarda el cliente en la base de datos. Si el campo 'status' no es igual a 1, 
        se devuelve una respuesta con un mensaje de error(409).

        Respuesta: 
        Devuelve un JSON con el detalle del cliente creado.
        """
        serializer = customerserializer(data=request.data)
        if serializer.is_valid():
            # Valida si ya existe un external_id
            external_id = serializer.validated_data['external_id']
            existing_external_id = customer.objects.filter(external_id=external_id).exists() 
            validate_status=serializer.validated_data['status']      
            # Si ya existe, devuelve un error de conflicto
            if existing_external_id:
                return Response({"error": "external_id del cliente diligenciado ya existe."},
                                status=status.HTTP_409_CONFLICT)
            # Validacion crear cliente en estado 1 (activo) 
            if validate_status==1:
                serializer.save()
            else:
               return Response({"error": "El campo 'status' debe ser 1"},
                                status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def get(self, request):
        """
        Obtiene todos los clientes existentes.

        Esta vista obtiene todos los clientes existentes en la base de datos, serializa los datos
        utilizando el serializador 'customerserializer' y devuelve una respuesta con una lista de
        los clientes y sus detalles en formato JSON con el código de estado 200 (OK).

        Returns:
            Un objeto JSON que contiene una lista de los clientes y sus detalles.

        """
        cliente = customer.objects.all()
        serializer = customerserializer(cliente, many=True)
        return Response(serializer.data)

class LoanView(views.APIView):      
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]
   
   def post(self, request):
        """
        Endpoint que permite crear un Prestamo, para ello requeire autenticacion mediante 
        TokenAuthentication y permiso de autenticado mediante IsAuthenticated.

        Esta vista toma los datos del préstamo desde el cuerpo de la solicitud (request.data),
        deserializa los datos utilizando el serializador 'loanserializer' y valida si el estado
        del préstamo es igual a 1 ('activo'). Si la validación es exitosa, se guarda el préstamo
        en la base de datos y se devuelve la respuesta correctamente.
        En caso de que el estado del préstamo no sea 1, se devuelve una respuesta con un mensaje
        de error y el código de estado 409 (CONFLICT).

        Respuesta: 
        Devuelve un JSON con el detalle del prestamo creado.
        """
        serializer = loanserializer(data=request.data)

        if serializer.is_valid():
            # Valida si el estado del prestamos es 1 ('activo')
            validate_status=serializer.validated_data['status']      
            if validate_status==1:
                # si el estado es igual a 1 crea el prestamo y se almacena en base de datos
                serializer.save()
            else:
               return Response({"error": "El Prestamo debe crearse con estado 1 'activo'."},
                                status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def get(self, request):
        """
        Obtiene todos los préstamos almacenados en base de datos.

        Esta vista obtiene todos los préstamos existentes en la base de datos, serializa los datos
        utilizando el serializador 'loanserializer' y devuelve una respuesta con una lista de los
        préstamos y sus detalles en formato JSON con el código de estado 200 (OK).

        Returns:
            Un objeto JSON que contiene una lista de los préstamos y sus detalles.

        """
        cliente = loan.objects.all()
        serializer = loanserializer(cliente, many=True)
        return Response(serializer.data)

class paymentView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Endpoint para procesar pagos de clientes.
        Recibe un pago con el external_id del cliente, externer_id referencia del pago y el monto total del pago.
        El pago se distribuye entre los préstamos activos del cliente hasta cubrir la deuda total.
        Si el monto del pago es superior a la deuda total, se rechaza el pago.

        Parámetros:
        - external_id: Identificador único del pago.
        - customer_id: Identificador único del cliente.
        - total_amount: Monto total del pago.

        """
        serializer = paymentserializer(data=request.data)

        if serializer.is_valid():
            # Validar si ya existe un external_id
            external_id = serializer.validated_data['external_id']
            customer_external_id = serializer.validated_data['customer_id']
            totalamount = serializer.validated_data['total_amount']
            activeloan = loan.objects.filter(customer_id=customer_external_id, status=1, outstanding__gt=0)
            total_outstanding = activeloan.aggregate(sum_outstanding=models.Sum('outstanding'))['sum_outstanding']
            #validacion si el cliente tiene prestamnos activos
            if not activeloan.exists():
                return Response({"error": "El cliente no tiene préstamos activos con deudas pendientes."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            if total_outstanding < totalamount:
                return Response({"error": "El monto del pago excede la deuda total del cliente."},
                                status=status.HTTP_400_BAD_REQUEST)
            # objeto del pago y se almacena en la base de datos
            payment_obj = payment.objects.create(external_id=external_id, customer_id=customer_external_id, total_amount=totalamount)
            # Distribuir el pago entre los préstamos activos
            for loan_obj in activeloan:
                amount_to_pay = min(loan_obj.outstanding, totalamount)
                loan_obj.outstanding -= amount_to_pay
                if loan_obj.outstanding == 0:
                    loan_obj.status = '1'
                loan_obj.save()
                # objeto con del detalle del pago y se almacenna en la base de datos
                paymentdetail.objects.create(amount=amount_to_pay, loan_id=loan_obj, payment_id=payment_obj)

                totalamount -= amount_to_pay
                if totalamount == 0:
                    break

            return Response({"message": "Pago creado exitosamente."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
        Endpoint para consultar pagos de clientes.
        Con base a los pagos realizados, devolvera el detalle de los pagos realizados por cliente,
        tomando el parametro 'customer_id' para buscar los pagos realizados por el cliente.

        Parámetros:
        - external_id: Identificador único del pago.
        - customer_id: Identificador único del cliente.

        Respuesta: 
        Devuelve un JSON con el detalle de los pagos realizados por el cliente

        """
        customer_external_id = request.query_params.get('customer_id')
        # Obtiene el objeto del cliente del external_id solicitado
        customer_obj = get_object_or_404(customer, external_id=customer_external_id)
        # Filtra los pagos relacionados con el cliente
        payments = payment.objects.filter(customer_id=customer_obj)
        # Se crea una lista para guardar los pagos y detalles del pago
        payment_data = []
        
        for payment_obj in payments:
            # filtra el detalle del pago asociado al pago
            payment_details = paymentdetail.objects.filter(payment_id=payment_obj.id)
            loan_details = []
            total_payment_amount = 0
            
            for detail in payment_details:
                # Obtiene el objeto del prestamo asociado al detalle de pago
                loan_obj = get_object_or_404(loan, external_id=detail.loan_id)
                total_payment_amount += detail.amount
                # agrega los detalle del prestamo del pago recibido en detalles del prestamo
                loan_details.append({
                    "loan_external_id": loan_obj.external_id,
                    "outstanding": loan_obj.outstanding,
                    "amount_paid": detail.amount
                })
            # Agrega los datos del pago actual a la lista de datos de pago
            payment_data.append({
                "external_id": payment_obj.external_id,
                "customer_external_id": payment_obj.customer_id.external_id,
                "loan_external_id": [loan_detail["loan_external_id"] for loan_detail in loan_details],
                "payment_date": payment_obj.paid_at,
                "status": payment_obj.status,
                "total_amount": payment_obj.total_amount,
                "payment_amount": total_payment_amount
            })
        
        return Response(payment_data, status=status.HTTP_200_OK)