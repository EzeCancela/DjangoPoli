from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime
from .models import *

####
class EspecialidadForm(forms.ModelForm):
       class Meta:
           model = Especialidad
           fields = ['descripcion', 'codigo']

####




class AltaMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'
        exclude = ['pacientes']


class ConsultaMedicosForm(forms.Form):
    # Definir campos
    # nombre = forms.CharField(label="Nombre", required=True)
    # especialidad = forms.Select(label="Especialidad", required=False)
    #listado_especialidades = lista_especialidades()
    especialidad = forms.ChoiceField(choices=Especialidad.lista_especialidades(), required=True, widget=forms.Select)
    medico = forms.CharField(label="Médico", widget=forms.TextInput(attrs={'class': 'medico'}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})),


class ConsultaPacientesForm(forms.Form):
    especialidad = forms.ChoiceField(choices=Especialidad.lista_especialidades(), required=True, widget=forms.Select)
    medico = forms.CharField(label="Médico", widget=forms.TextInput(attrs={'class': 'medico'}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})),


class AltaTurnoForm(forms.Form):

    listado_especialidad = Especialidad.lista_especialidades()

    paciente = forms.CharField(label="pacientex:", max_length=8, min_length=7 ,required=True, validators=[RegexValidator(
                '^[0-9]+$',
                message="Debe contener solo números")],
        widget=forms.TextInput(attrs={"class": "form-control", "id":"paciente","size": 12, "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    especialidad = forms.ChoiceField(label="especialidadx:",required=False, choices = listado_especialidad,
        widget=forms.Select(attrs={"class": "form-control", "id":"especialidad"}))
    medico = forms.ChoiceField(label="medicox:", required=False,
        widget=forms.Select(attrs={"class": "form-control", "id":"medico"}))


    def __init__(self, *args, **kwargs):
        codigo_especialidad = kwargs.pop('especialidad', None)
        super().__init__(*args, **kwargs)
        self.fields['medico'].choices = self.get_medicos_choices(codigo_especialidad)

    def get_medicos_choices(self, codigo_especialidad):
        choices = [('Z', 'Seleccione un médico')]
        if codigo_especialidad != None:
            especialidad = Especialidad.objects.get(codigo=codigo_especialidad)
            medicos = Medico.objects.filter(especialidad=especialidad)
            for medico in medicos:
                choice = (str(medico.id), f"{medico.nombre} {medico.apellido} ({medico.especialidad.descripcion})")
                choices.append(choice)
        return choices


    fecha = forms.DateField(label="fechax:",required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "id":"fecha",'type': 'date'}))

    def clean_medico(self):
        especialidad_codigo = self.cleaned_data['especialidad']
        medico_id = self.cleaned_data.get('medico')

        if especialidad_codigo != 'Z':
            self.fields['medico'].choices = self.get_medicos_choices(especialidad_codigo)
            medico_id = self.cleaned_data['medico']
            choices = self.get_medicos_choices(especialidad_codigo)
            # Verificar si el ID del médico seleccionado está en las opciones disponibles
            if medico_id not in [choice[0] for choice in choices]:
                raise forms.ValidationError("Selecciona un médico válido.")

        return medico_id
    
    def clean_paciente(self):
        data = self.cleaned_data["paciente"]
        print("los datos de paciente ingresado son:", data)
        longitud = len(data)
        if longitud > 8 or longitud < 7:
            raise ValidationError("Ingrese entre 7 y 8 dígitos de su número de documento")
        return data

    def clean_fecha(self):
        fecha_elegida = self.cleaned_data['fecha']
        print('la fecha que eligieron: ',fecha_elegida)
        if fecha_elegida != None:
            if fecha_elegida <= datetime.date.today():
                raise forms.ValidationError("La fecha debe ser mayor al día de Hoy!")
            dia_elegido = datetime.date.weekday(fecha_elegida)
            print('El dia elegido tiene el nro: ',dia_elegido)
            if dia_elegido >= 5:
                raise forms.ValidationError("La fecha no puede ser Sábado ni Domingo!")
        return fecha_elegida

    def clean(self):
        print("entro al clean")
        cleaned_data = super().clean()
        medico_id = cleaned_data.get('medico')
        print("Medico id:", medico_id)
        return self


def funcion_de_guardado_de_turno(accion,id,medico,fecha,hora):
    if accion == 'actualizar':
        print("ingreso a actualizar") 
        actualizacion = Turno.asignar_turno(id,medico,fecha,hora)
        if actualizacion:
            print("Turno fue registrado correctamente!!!")
        else:
            print("Hay un problema en el guardado del turno")

    if accion == 'consultar':
        id_paciente = Paciente.Obtener_id_Paciente_por_dni(id)
        print("el id del paciente es: ", id_paciente)
        print("el id del medico es el nro:", medico)
        print("la fecha tiene el valor siguiente:", fecha)
        print("ingreso a consultar")
        listado_de_turnos = Turno.obtener_turnos(medico,fecha)
        print("LISTA NUEVITA DE TURNOS! --> :",listado_de_turnos)
        return listado_de_turnos

    if accion == 'anular':
        print("Ingreso a anular") 
        actualizacion = Turno.desasignar_turno(id)
        if actualizacion:
            print("Turno fue anulado correctamente!!!")
        else:
            print("Hay un problema en el anulado del turno")


class BajaTurnoForm(forms.Form):          
    dni = forms.IntegerField(label="Paciente:", initial="" , error_messages={'required': 'Ingrese el dni del paciente'} ,
            widget=forms.TextInput(attrs={"class": "form-paciente paciente_recuadro", "id":"paciente", "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    
    # nombre_completo = forms.Field(required=False , disabled=True)  -- no hace falta colocarlo aquí, ,porque lo estoy pasando por el context
    
  
    def clean_dni(self):
        
        data = self.cleaned_data["dni"]      
       
        if Paciente.objects.filter(dni=self.cleaned_data["dni"]).exists():
            pass                               
              
        else:
            print("NO encontró el dni en la tabla")
            raise ValidationError("Paciente inexistente")
       
        return data
       

class BajaTurnoDetalleForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(label="Horario", required=True)       
    medico = forms.CharField(label=' Médico', widget=forms.TextInput(attrs={'class': 'paciente'}))
    especialidad = forms.CharField(label=' Especialidad')


class ConsultaTurnosForm(forms.Form):
    # Definir campos
    def fecha(desde,cuantos_dias):
        if desde == 'h':
            hasta = datetime.date.today() + datetime.timedelta(days=cuantos_dias)
        else:
            pass
        return hasta.strftime('%Y-%m-%d')

    paciente = forms.CharField(label="Paciente:", max_length=8, min_length=6 ,required=False, validators=[RegexValidator(
                '^[0-9]+$',
                message="Debe contener solo números")],
        widget=forms.TextInput(attrs={"class": "form-control", "id":"paciente","size": 12, "title":"Ingrese entre 6 y 8 dígitos de su número de documento"}))
    especialidad = forms.ChoiceField(label=' Especialidad', choices=Especialidad.lista_especialidades(), required=False, widget=forms.Select)
    medico = forms.ChoiceField(label=' Médico', choices=Medico.lista_medicos(), required=False, widget=forms.Select)
    fechaDesde = forms.DateField(label=' Fecha Desde',widget=forms.DateInput(attrs={'type': 'date'}), required=False, initial=fecha('h',0))
    fechaHasta = forms.DateField(label=' Fecha Hasta',widget=forms.DateInput(attrs={'type': 'date'}), required=False, initial=fecha('h',60))

    def clean_paciente(self):
        data = self.cleaned_data["paciente"]
        if data != '':
            if not Paciente.objects.filter(dni = int(data)).exists():
                raise ValidationError("Debe ingresar un DNI de paciente válido o dejarlo en blanco")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        dataD = cleaned_data.get("fechaDesde")
        dataH = cleaned_data.get("fechaHasta")

        if dataD is not None and dataH is not None and dataD > dataH:
            raise ValidationError("Debe ingresar un rango de fechas correcto, Fecha Desde <= Fechas Hasta")

        return cleaned_data


class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto:", max_length=5, required=True,
        widget=forms.TextInput(attrs={"class": "special", "id":"44"}))
    apellido = forms.CharField(label="Apellido de contacto", required=True)
    email = forms.EmailField(required=True)
