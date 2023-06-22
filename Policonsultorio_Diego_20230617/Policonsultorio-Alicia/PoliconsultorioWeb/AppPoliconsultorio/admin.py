from django.contrib import admin
from .models import Especialidad,Paciente,Medico,Turno


class MedicoAdmin(admin.ModelAdmin):
    empty_value_display = '---'


class PacienteAdmin(admin.ModelAdmin):
    empty_value_display = '---'


class TurnoAdmin(admin.ModelAdmin):
    empty_value_display = '---'


# Register your models here.
admin.site.register(Especialidad)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Turno, TurnoAdmin)
