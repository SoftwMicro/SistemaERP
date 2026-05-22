from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    produto = serializers.CharField()
    quantidade = serializers.IntegerField()
    preco_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)

class OrderStatusHistorySerializer(serializers.Serializer):
    data_hora = serializers.DateTimeField()
    status_anterior = serializers.CharField()
    novo_status = serializers.CharField()
    usuario = serializers.CharField()
    observacoes = serializers.CharField(allow_blank=True, required=False)

class OrderSerializer(serializers.Serializer):
    numero = serializers.IntegerField()
    data_criacao = serializers.DateTimeField()
    cliente = serializers.CharField()
    status = serializers.CharField()
    valor_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    observacoes = serializers.CharField(allow_blank=True, required=False)
    itens = OrderItemSerializer(many=True)
    historico_status = OrderStatusHistorySerializer(many=True)
