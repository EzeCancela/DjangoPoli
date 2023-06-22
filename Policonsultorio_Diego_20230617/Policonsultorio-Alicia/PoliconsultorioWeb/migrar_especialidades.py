# Ejecutar para migrar las Especialidades "de prueba" a la base de datos
import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PoliconsultorioWeb.settings")
django.setup()

# Importar el modelo y ejecutar la migración de registros iniciales
from AppPoliconsultorio.models import Especialidad
Especialidad.migrar_registros_iniciales()
