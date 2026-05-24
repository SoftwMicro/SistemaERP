from rest_framework import serializers

class ProdutoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sku = serializers.CharField(max_length=30)
    nome = serializers.CharField(max_length=100)
    descricao = serializers.CharField()
    preco = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = serializers.IntegerField()
    ativo = serializers.BooleanField(default=True)
