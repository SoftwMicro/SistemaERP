from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=18, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    ativo = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["cpf_cnpj"]),
        ]

    def __str__(self):
        return f"{self.nome} ({self.cpf_cnpj})"

class Produto(models.Model):
    sku = models.CharField(max_length=30, unique=True, db_index=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["nome"]),
        ]

    def __str__(self):
        return f"{self.nome} ({self.sku})"

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADO", "Confirmado"),
        ("SEPARADO", "Separado"),
        ("ENVIADO", "Enviado"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADO", "Cancelado"),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="pedidos")
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDENTE", db_index=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    idempotency_key = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["data_criacao"]),
        ]

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"

class OrderItem(models.Model):
    pedido = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("pedido", "produto")

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"

class OrderStatusHistory(models.Model):
    pedido = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="historico_status")
    data_hora = models.DateTimeField(auto_now_add=True)
    status_anterior = models.CharField(max_length=20)
    novo_status = models.CharField(max_length=20)
    usuario = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.pedido.id}: {self.status_anterior} -> {self.novo_status}"
