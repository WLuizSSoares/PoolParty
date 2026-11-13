from django.contrib import admin
from .models import Casa
from .models import Cliente
from .models import Reserva

admin.site.register(Casa)
admin.site.register(Cliente)
admin.site.register(Reserva)