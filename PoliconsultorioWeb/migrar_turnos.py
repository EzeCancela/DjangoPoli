# Ejecutar para migrar turnos automaticamente de prueba a la base de datos
import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PoliconsultorioWeb.settings")
django.setup()

# Importar el modelo y ejecutar la migración de registros iniciales
from AppPoliconsultorio.models import Medico
from AppPoliconsultorio.models import Turno

Turno.migrar_registros_iniciales()
