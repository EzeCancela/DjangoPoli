# Policonsultorio-Grupo-7
#
# 02-05-2023 (FR)
# En alta de turno se agregaron validaciones en el campo paciente de los siguientes tipos:
# Validación de cantidad de caracteres MAX y MIN en la generación del campo
# Validación con REGEX, unicamente se permiten caracteres numericos.
# Añadido Tooltip al campo paciente.
# Muestra de mensajería en Rojo (La que viene de la vista y la que viene del Form). Agregado de Filtro para mayuscula.
# 
# Agregado de funciones para registrar el alta del turno(actualizacion de registro) y con la misma funcion bajo otro parametro la 
# consulta de turnos.
# En la consulta de turnos ahora se muestran los turnos (Horario / disponibilidad) en una tabla (usando la funcion descripta arriba).
# En la consulta de turnos se arreglaron estilos.
#
#-------------------------------------------------------------------------------------------
#
# 20-05-2023 (FR)
# Agregado de Modelo "Nomenclaturas en singular"  (Usuario de la base: admin / password: admin)
#
# Recordar que:
# #para crear y migrar
# python manage.py makemigrations AppPoliconsultorio  
# # esta linea de arriba solo creo el archivo en migrate, luego lo tenes que migrar...
# con esta linea lo crea en la base...   
# python manage.py migrate AppPoliconsultorio
#
# Fin recordar..
#
# Dentro del modelo hay funciones que permiten generar datos de prueba, las cuales se ejecutan directamente desde:
# Pararse donde esta el archivo "manage.py"
# Ejecutar lo siguiente desde un CMD.exe: 
# "migrar_especialidades.py"   (realizar lo mismo con Pacientes, Medicos, Turnos (en ese orden)!
#
# IMPORTANTE:
# Pasos para incorporar el modelo con los datos:
# Correr lo descripto en "Recordar" que esta mas arriba, 1ero el makemigrations y luego el migrate.
# Si da error seguramente les puede pasar lo mismo que a mi, porque ya tenian en la base otras tablas que ahora no coinciden.
# Luego de luchar con los errores, modificando los nombres y demas, llegue hasta borrar la base y crearla, pero no se me re-generaban.
# Para solucionar los problemas que me aparecian realice lo siguiente:
# Deje el proyecto solo con el modelo, en la url solo el index y en la vista tambien solo el index. 
# (esto es porque cuando queres hacer cambios con makemigratios y migrate, django recorre todo lo que tenes previamente en tu views, 
# forms y demas código.
# No aconsejo muchos cambios en el modelo, yo borre toda la base, y luego de mucho tiempo..., comente todo para que quede solo index
# y quite los archivos de migrations, de esta manera regenere con makemigrations, 
# me creo un nuevo archivo y lo migre, luego corri lo de las funciones que explico mas arriba que generan los datos de prueba.
#
# Fin modelo...
# 
# Validaciones en el alta:
# Si bien las validaciones fueron terminadas siguiendo los pasos del alta, cuando agregamos el modelo y lo asociamos al mismo
# para traer los datos de la base algunas de las validaciones dejaron de funcionar (Esto queda pendiente)...
#
# Alta de turno: (22-05-2023)
# En el alta de turnos, el turno viene de la BD y se guarda en la BD.
#
# Baja de Turno: 12-06-2023
# Ahora la baja de turno registra el cambio en la base de datos.
# El mensaje de baja no se visualiza duplicado(Corregido)
# Modelo: El modelo ahora tiene una FK en Persona sobre el modelo por defecto de django de Usuario.
# Las personas son usuario tambien en este modelo.
#
#
