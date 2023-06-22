from django.db import models
from datetime import timedelta, date
from django.utils.dateparse import parse_date
from django.contrib import admin
from django.contrib.auth.models import User

class Persona(models.Model):
    nombre = models.CharField(max_length=25, blank=False, verbose_name='Nombre')
    apellido = models.CharField(max_length=25, blank=False, verbose_name='Apellido')
    telefono = models.CharField(max_length=50, verbose_name='Telefono')
    mail = models.EmailField(max_length=150, verbose_name='Email')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def nombre_completo(self):
        return f"{self.apellido}, {self.nombre}"


class Especialidad(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='Descripcion')
    codigo = models.CharField(max_length=2, verbose_name='Codigo')

    class Meta:

        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

        constraints = [
            models.UniqueConstraint(
                fields=['codigo', 'descripcion'], name='unique_codigo_descripcion_combination'
            )
            ]
    
    
    @classmethod
    def crear_especialidad(cls, descripcion, codigo):
        obj, created = cls.objects.get_or_create(descripcion=descripcion, codigo=codigo)
        if created:
            print(f"Se creó la especialidad: {obj}")

    @classmethod
    def eliminar_especialidad(cls, codigo):
        try:
            especialidad = cls.objects.get(codigo=codigo)
            especialidad.delete()
            print("Especialidad eliminada con éxito.")
        except cls.DoesNotExist:
            print(f"No se encontró la especialidad con código {codigo}.")    



    def __str__(self):
        return self.descripcion

    def lista_especialidades():
        opciones_especialidades = [('Z', 'Seleccione una especialidad')]
        opciones_especialidades += [(esp.codigo, esp.descripcion) for esp in Especialidad.objects.all().order_by('descripcion')]
        return opciones_especialidades

    @classmethod
    def migrar_registros_iniciales(cls):
        especialidades_lst = [
            {'descripcion': 'Cardiología', 'codigo': 'C'},
            {'descripcion': 'Dermatología', 'codigo': 'D'},
            {'descripcion': 'Neurología', 'codigo': 'N'},
            {'descripcion': 'Oftalmología', 'codigo': 'O'},
            {'descripcion': 'Pediatría', 'codigo': 'P'},
        ]
        for especialidad in especialidades_lst:
            obj, created = cls.objects.get_or_create(**especialidad)
            if created:
                print(f"Se creó la especialidad: {obj}")

        print("Registros iniciales de especialidades migrados con éxito.")

    
class Paciente(Persona):
    GENEROS = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otro'),
    ]
    dni = models.IntegerField(blank=False, verbose_name='DNI', primary_key=True)
    fecha_nacimiento = models.DateField(null= True, verbose_name='Fecha Nacimiento')
    genero = models.CharField(max_length=1, choices=GENEROS, verbose_name='Genero', null = True)
    obra_social = models.CharField(max_length=128, verbose_name="Obra_social", null = True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dni'], name='unique_dni_combination'
            )
        ]

    def __str__(self):
        return f"{self.nombre_completo} - DNI: {self.dni}"

    def lista_pacientes():
        pacientes = Paciente.objects.all().order_by('apellido','nombre')
        listado_pacientes = [('Z','Seleccione un paciente')]
        for paciente in pacientes:
                listado_pacientes.append(paciente.dni, paciente.nombre_completo)
            
        return listado_pacientes 
    
    @classmethod
    def migrar_registros_iniciales(cls):
        pacientes = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'telefono': '123456789', 'mail': 'juan@example.com', 'dni': 11111111, 'fecha_nacimiento': date(1981,7,15), 'genero': 'M', 'obra_social': 'Obra Social A'},
            {'nombre': 'María', 'apellido': 'López', 'telefono': '987654321', 'mail': 'maria@example.com', 'dni': 22222222, 'fecha_nacimiento': date(1968,3,30), 'genero': 'F', 'obra_social': 'Obra Social B'},
            {'nombre': 'Carlos', 'apellido': 'González', 'telefono': '555555555', 'mail': 'carlos@example.com', 'dni': 33333333, 'fecha_nacimiento': date(2002,6,21), 'genero': 'M', 'obra_social': 'Obra Social C'},
        ]
        for paciente in pacientes:
            obj, created = cls.objects.get_or_create(**paciente)
            if created:
                print(f"Se creó el paciente: {obj}")

        print("Registros iniciales de pacientes migrados con éxito.")


    @classmethod
    def buscar_por_dni(cls, dni):
        try:
            paciente = cls.objects.get(dni=dni)
            nombre_completo = f"{paciente.nombre} {paciente.apellido}"
            return nombre_completo
        except cls.DoesNotExist:
            return "No-existe"

    @classmethod
    def Obtener_id_Paciente_por_dni(cls, dni):
        try:
            paciente = cls.objects.get(dni=dni)
            return paciente.pk
        except cls.DoesNotExist:
            return None


class Medico(Persona):
    matricula = models.IntegerField(blank=False, null=True, verbose_name='Matricula')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    pacientes = models.ManyToManyField(Paciente, through='Turno')


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['matricula'], name='unique_matricula_combination'
            )
        ]

    def __str__(self):
        return f"{self.nombre_completo} - ({self.especialidad})"

    def lista_medicos():
        medicos = Medico.objects.all().order_by('apellido','nombre')
        listado_medicos = [('Z','Seleccione un medico')]
        for medico in medicos:
            listado_medicos.append((medico.id, f"{medico.nombre_completo} ({medico.especialidad.descripcion})"))
        return listado_medicos

    @classmethod
    def migrar_registros_iniciales(cls):
        
        medicos = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'telefono': '123456789', 'mail': 'correo1@example.com', 'matricula': 123456, 'especialidad': 'Cardiología'},
            {'nombre': 'María', 'apellido': 'González', 'telefono': '987654321', 'mail': 'correo2@example.com', 'matricula': 234561, 'especialidad': 'Dermatología'},
            {'nombre': 'Celeste', 'apellido': 'Romero', 'telefono': '987616321', 'mail': 'correo3@example.com', 'matricula': 345612, 'especialidad': 'Dermatología'},
            {'nombre': 'Luis', 'apellido': 'Sánchez', 'telefono': '456789123', 'mail': 'correo4@example.com', 'matricula': 456123, 'especialidad': 'Neurología'},
            {'nombre': 'Ana', 'apellido': 'Rodríguez', 'telefono': '178954987', 'mail': 'correo5@example.com', 'matricula': 561234, 'especialidad': 'Oftalmología'},
            {'nombre': 'Mabel', 'apellido': 'Manzotti', 'telefono': '176954987', 'mail': 'correo6@example.com', 'matricula': 612345, 'especialidad': 'Oftalmología'},
            {'nombre': 'Jacinta', 'apellido': 'Lee', 'telefono': '174954987', 'mail': 'correo7@example.com', 'matricula': 654321, 'especialidad': 'Oftalmología'},
            {'nombre': 'Pedro', 'apellido': 'López', 'telefono': '321654987', 'mail': 'correo8@example.com', 'matricula': 543216, 'especialidad': 'Pediatría'},
        ]

        for medico in medicos:
            especialidad = Especialidad.objects.get(descripcion=medico['especialidad'])
            obj, created = cls.objects.get_or_create(
                nombre=medico['nombre'],
                apellido=medico['apellido'],
                telefono=medico['telefono'],
                mail=medico['mail'],
                #matricula=medico['matricula'],
                especialidad=especialidad,
            )
            if created:
                print(f"Se creó el médico: {obj}")

        print("Registros iniciales de médicos migrados con éxito.")


class Turno(models.Model):
    HORARIOS = [
        ('10:00','10:00'),
        ('11:00','11:00'),
        ('12:00','12:00'),
        ('15:00','15:00'),
        ('16:00','16:00'),
        ('17:00','17:00'),
    ]
    fecha = models.DateField(verbose_name='Fecha')

    hora = models.CharField(max_length=128, choices=HORARIOS ,verbose_name='Horario_turno')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    # hora = models.TimeField(verbose_name='Hora')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['medico', 'fecha', 'hora'], name='unique_medico_fecha_hora_combination'
            )
        ]

    def __str__(self):
        return f"{self.fecha} - {self.hora} - Médico: {self.medico} - Paciente: {self.paciente}"

    def lista_turnos(filtro_fechaDesde=date.today(), filtro_fechaHasta=date.today(), filtro_paciente='', filtro_especialidad='', filtro_medico=''):
        turnos = Turno.objects.filter(fecha__range=(parse_date(filtro_fechaDesde),parse_date(filtro_fechaHasta)))
        if filtro_paciente != '':
            turnos = turnos.filter(paciente__dni__exact=filtro_paciente)
        if filtro_especialidad != '':
            turnos = turnos.filter(medico__especialidad__codigo__exact=filtro_especialidad)
        if filtro_medico != '':
            turnos = turnos.filter(medico__id = filtro_medico)
        turnos = sorted(turnos, key=lambda turno: (str(turno.fecha) + turno.hora))
        return turnos

    @classmethod
    def migrar_registros_iniciales(cls):
        fecha_inicial = date.today()
        fecha_final = fecha_inicial + timedelta(days=90)

        horas = ['10:00', '11:00', '12:00', '15:00', '16:00', '17:00']

        medicos = Medico.objects.all()

        for medico in medicos:
            for fecha in daterange(fecha_inicial, fecha_final):
                for hora in horas:
                    obj, created = cls.objects.get_or_create(
                        paciente=None,
                        medico=medico,
                        fecha=fecha,
                        hora=hora,
                    )
                    if created:
                        print(f"Se creó el turno: {obj}")

        print("Registros iniciales de turnos migrados con éxito.")

    @classmethod
    def obtener_turnos(cls, id_medico, fecha_param):
        turnos = cls.objects.filter(medico__id=id_medico, fecha=fecha_param) 
        resultados = []
        for turno in turnos:
            resultado = {
                'ID': turno.hora,
                'horario' : turno.hora,
                'descr_disponible': 'No disponible' if turno.paciente else 'Disponible',
                'flag': 'disabled' if turno.paciente else 'enabled',
            }
            resultados.append(resultado)
        return resultados


    @classmethod
    def asignar_turno(cls, id_paciente, id_medico, fecha_turno, hora_param):
        if id_paciente is not None:
            paciente = Paciente.objects.get(dni=id_paciente)
        else:
            paciente = id_paciente
        turno = cls.objects.filter(medico__id=id_medico, fecha=fecha_turno, hora=hora_param).first()
        if turno:
            turno.paciente = paciente
            turno.save()
            return True
        return False

    @classmethod
    def desasignar_turno(cls,id_turno):
        turno = cls.objects.filter(id=id_turno).first()
        if turno:
            turno.paciente = None
            turno.save()
            return True
        return False

    def __str__(self):
        return f"{self.fecha} - {self.hora} - Medico: {self.medico} - Paciente: {self.paciente}"

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

