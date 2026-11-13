from django.core.exceptions import ValidationError
from django.db import models

class Casa(models.Model):

    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.PositiveIntegerField()
    ativa = models.BooleanField(default=True)
    motivo_inativacao = models.TextField(blank=True)
    permite_noturno = models.BooleanField(default=False)


    def __str__(self):
        return self.nome

class Cliente(models.Model):

    class Origem(models.TextChoices):
        INSTAGRAM = 'instagram', 'Instagram'
        INDICACAO = 'indicacao', 'Indicação'
        WHATSAPP = 'whatsapp', 'Whatsapp'
        GOOGLE = 'google', 'Google'
        RECORRENTE = 'recorrente', 'Cliente recorrente'
        OUTROS = 'outros', 'Outros'


    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    origem = models.CharField(max_length=30,
                              choices=Origem.choices,
                              blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADA = 'confirmada', 'Confirmada'
        CONCLUIDA = 'concluida', 'Concluída'
        CANCELADA = 'cancelada', 'Cancelada'
        REMARCADA = 'remarcada', 'Remarcada'

    status = models.CharField(max_length=15,
                              choices=Status.choices,
                              default=Status.PENDENTE, )

    class Modalidade(models.TextChoices):
        DIURNA = 'diurna', 'Diurna'
        NOTURNA = 'noturna', 'Noturna'
        DIA_NOITE = 'dia_noite', 'Dia + Noite'

    modalidade = models.CharField(
        max_length=15,
        choices=Modalidade.choices,
    )



    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='reservas',

    )

    casa = models.ForeignKey(
        Casa,
        on_delete=models.PROTECT,
        related_name='reservas',
    )

    valor_tabela = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    valor_final = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'Reserva #{self.id} - {self.casa.nome} ({self.data_inicio}) a '
            f'{self.data_fim}'
        )

    # Método utilizado para validar os dados do modelo.
    def clean(self):
        #Validade do período
        if self.data_inicio and self.data_fim:
            if self.data_fim <= self.data_inicio:
                raise ValidationError(
                    'O término da reserva deve ser posterior ao início.'
                )
        #Validade de Casa ativa
        if self.casa_id and not self.casa.ativa:
            raise ValidationError (
                f'A casa não está ativa devido {self.casa.motivo_inativacao}.'
            )

        if self.casa and not self.casa.permite_noturno:
            if (self.modalidade == Reserva.Modalidade.NOTURNA
                    or self.modalidade == Reserva.Modalidade.DIA_NOITE):
                raise ValidationError (
                    'A casa não permite esse tipo de modalidade.'
                )

