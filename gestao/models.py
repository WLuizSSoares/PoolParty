from django.db import models

class Casa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.PositiveIntegerField()
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

