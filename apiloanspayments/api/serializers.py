from .models import loan, payment, customer, paymentdetail
from rest_framework import serializers

"""
    Serializador para la clase 'customer'.

    Este serializador se utiliza para convertir instancias de la clase 'customer' en datos JSON
    y viceversa. Define qué campos y modelos deben incluirse o excluidos al serializar o
    deserializar objetos de la clase 'customer'.

    Atributos:
        Meta: Clase anidada que define los metadatos del serializador, incluido el modelo 'customer'
              y los campos que se incluirán en la serialización/deserialización.

    """
class customerserializer(serializers.ModelSerializer):
  class Meta:
    model = customer
    fields = ['external_id', 'status', 'score', 'preapproved_at']

"""
    Serializador para la clase 'loan'.

    Este serializador se utiliza para convertir instancias de la clase 'loan' en datos JSON y viceversa.
    Define qué campos y modelos deben incluirse o excluidos al serializar o deserializar objetos de la clase 'loan'.
    Se define una subclase Meta que define los metadatos del serializador

    """
class loanserializer(serializers.ModelSerializer):
  class Meta:
    model = loan
    fields = ['external_id', 'customer_id', 'amount', 'outstanding', 'status']
   
"""
    Serializador para la clase 'payment'.

    Este serializador se utiliza para convertir instancias de la clase 'payment' en datos JSON
    y viceversa. Define qué campos y modelos deben incluirse o excluidos al serializar o
    deserializar objetos de la clase 'payment'.
    Se define una subclase Meta que define los metadatos del serializador

    """
class paymentserializer(serializers.ModelSerializer):
  class Meta:
    model = payment
    fields = ['external_id','customer_id', 'total_amount']

"""
    Serializador para la clase 'paymentdetail'.

    Este serializador se utiliza para convertir instancias de la clase 'paymentdetail' en datos JSON
    y viceversa. Define qué campos y modelos deben incluirse o excluidos al serializar o
    deserializar objetos de la clase 'paymentdetail'.
    Se define una subclase Meta que define los metadatos del serializador


    """
class paymentdetail_serializer(serializers.ModelSerializer):
  class Meta:
    model = paymentdetail
    fields = ['loan_id', 'amount', 'payment_id']