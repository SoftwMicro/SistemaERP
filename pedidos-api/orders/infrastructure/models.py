from django.db import models

class Order(models.Model):
    customer = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.customer} - {self.status}"