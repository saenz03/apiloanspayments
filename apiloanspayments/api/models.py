from django.db import models
"""
    Modelo para representar un cliente.

    Atributos:
        id (IntegerField): ID único del cliente.
        external_id (CharField): Identificador externo único del cliente.
        status (PositiveIntegerField): Estado del cliente.
        score (PositiveBigIntegerField): Puntaje del cliente.
        preapproved_at (DateTimeField): Fecha y hora de preaprobación del cliente.
    """
class customer(models.Model):
    id = models.IntegerField(primary_key=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)  
    status = models.PositiveIntegerField(default=0)
    score =  models.PositiveBigIntegerField(default=0)
    preapproved_at = models.DateTimeField()

"""
    Modelo para representar un préstamo.

    Atributos:
        id (IntegerField): ID único del préstamo.
        created_at (DateTimeField): Fecha y hora de creación del préstamo.
        updated_at (DateTimeField): Fecha y hora de última actualización del préstamo.
        external_id (CharField): Identificador externo único del préstamo.
        amount (IntegerField): Monto del préstamo.
        status (PositiveIntegerField): Estado del préstamo.
        customer_id (ForeignKey): Relación con el cliente al que pertenece el préstamo.
        outstanding (IntegerField): Monto pendiente del préstamo.
    """
class loan(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)  
    amount = models.IntegerField(default=0)
    status = models.PositiveIntegerField(default=0)
    #contract_version = models.CharField(max_length=30)
    #maximum_payment_date = models.DateTimeField()
    #taken_at = models.DateTimeField()
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE, default=0, to_field='external_id')
    outstanding = models.IntegerField(default=0)

"""
    Modelo para representar un pago.

    Atributos:
        id (IntegerField): ID único del pago.
        created_at (DateTimeField): Fecha y hora de creación del pago.
        updated_at (DateTimeField): Fecha y hora de última actualización del pago.
        external_id (CharField): Identificador externo único del pago.
        total_amount (IntegerField): Monto total del pago.
        status (PositiveIntegerField): Estado del pago.
        paid_at (DateTimeField): Fecha y hora en que se realizó el pago.
        customer_id (ForeignKey): Relación con el cliente al que pertenece el pago.
    """
class payment(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60) 
    total_amount = models.IntegerField(default=0)
    status = models.PositiveIntegerField(default=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE, default=0, to_field='external_id')

"""
    Modelo para representar el detalle de un pago.

    Atributos:
        id (IntegerField): ID único del detalle de pago.
        created_at (DateTimeField): Fecha y hora de creación del detalle de pago.
        updated_at (DateTimeField): Fecha y hora de última actualización del detalle de pago.
        amount (IntegerField): Monto del pago.
        loan_id (ForeignKey): Relación con el prestamo al que pertenece el detalle de pago.
        payment_id (ForeignKey): Relación con el pago al que pertenece el detalle de pago.
    """
class paymentdetail(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    loan_id = models.ForeignKey(loan, on_delete=models.CASCADE, default=0)
    payment_id = models.ForeignKey(payment, on_delete=models.CASCADE)