from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required,permission_required
from .models import Especialidad



from .forms import *
from .models import *

from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    context = {}
    return render(request, "AppPoliconsultorio/index.html", context)


def acerca(request):
    context = {}
    return render (request,"AppPoliconsultorio/acerca.html", context)


def especialidades(request):
    context = {}
    return render (request,"AppPoliconsultorio/especialidades.html", context)


def alta_especialidad(request):
       if request.method == 'POST':
           form = EspecialidadForm(request.POST)

           if form.is_valid():
               form.save()
               return redirect('especialidades')
       else:
           form = EspecialidadForm()
       context = {'form': form}
       return render(request, 'AppPoliconsultorio/alta_especialidad.html', context)

def baja_especialidad(request):
    especialidad_eliminada = False
    
    if request.method == 'POST':
        codigo_especialidad = request.POST.get('codigo_especialidad')
        especialidad = get_object_or_404(Especialidad, codigo=codigo_especialidad)
        especialidad.delete()
        especialidad_eliminada = True
        
    context = {'especialidad_eliminada': especialidad_eliminada}
    return render(request, 'AppPoliconsultorio/baja_especialidad.html', context)

#def baja_especialidad(request, especialidad_id):
#       especialidad = get_object_or_404(Especialidad, id=especialidad_id)
#       if request.method == 'POST':
#           especialidad.delete()
#           return redirect('especialidades')
#       context = {'especialidad': especialidad}
#       return render(request, 'baja_especialidad.html', context)


def listar_especialidad(request):
    context = {}

    listado = Especialidad.objects.all()

    context['lista_especialidades'] = listado
    return render (request,"AppPoliconsultorio/listar_especialidad.html", context)

#@login_required
#def alta_especialidad(request):
#    if request.method == 'POST':
#        descripcion = request.POST.get('descripcion')
#        codigo = request.POST.get('codigo')
#        Especialidad.crear_especialidad(descripcion, codigo)
#        return redirect('listar_especialidad')
#    return render(request, "AppPoliconsultorio/alta_especialidad.html")


#@login_required
#def baja_especialidad(request):
#    if request.method == 'POST':
#        codigo = request.POST.get('codigo')
#        Especialidad.eliminar_especialidad(codigo)
#        return redirect('listar_especialidad')
#    return render(request, "AppPoliconsultorio/baja_especialidad.html")

def listar_especialidad(request):
    context = {}
    listado = Especialidad.objects.all()
    context['lista_especialidades'] = listado
    return render(request, "AppPoliconsultorio/listar_especialidad.html", context)



@permission_required('AppPoliconsultorio.add_medico')
def alta_medico(request):
    # Alta de un Médico
    context = {}
    if request.method == 'POST':
        form = AltaMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Médico incorporado con éxito')
            return redirect('listar_medicos')
    else:
        form = AltaMedicoForm()

    context['form'] = form
    return render(request, "AppPoliconsultorio/alta_medico.html", context)


@login_required
def baja_medico(request):
    # Baja de un Médico
    context = {}
    return render(request, "AppPoliconsultorio/baja_medico.html", context)


@login_required
def consulta_medicos(request):
    # Prepara los combos
    listado_especialidad = Especialidad.lista_especialidades()
    listado_medicos = Medico.lista_medicos()

    if request.method == "POST":
        consulta_medicos_form = ConsultaMedicosForm(request.POST)
    else:
        consulta_medicos_form = ConsultaMedicosForm()

    context = {
        "listado_especialidad": listado_especialidad,
        "listado_medicos": listado_medicos,
        "form": consulta_medicos_form,
    }
    return render(request, "AppPoliconsultorio/consulta_medicos.html", context)


class listar_medicos(ListView):
    model = Medico
    context_object_name = "medicos"
    template_name = "AppPoliconsultorio\listar_medicos.html"
    ordering = ['apellido', 'nombre']


@login_required
def alta_paciente(request):
    # Alta de un Paciente
    context = {}
    return render(request, "AppPoliconsultorio/alta_paciente.html", context)


@login_required
def baja_paciente(request):
    # Baja de un Médico
    context = {}
    return render(request, "AppPoliconsultorio/baja_paciente.html", context)


@login_required
def consulta_pacientes(request):
    # Prepara los combos
    listado_pacientes = Paciente.lista_pacientes()

    if request.method == "POST":
        consulta_pacientes_form = ConsultaPacientesForm(request.POST)
    else:
        consulta_pacientes_form = ConsultaPacientesForm()

    context = {
        "listado_pacientes": listado_pacientes,
        "form": consulta_pacientes_form,
    }
    return render(request, "AppPoliconsultorio/consulta_pacientes.html", context)


@login_required
def listar_pacientes(request):
    context = {}

    listado = Paciente.objects.all()

    context['listar_pacientes'] = listado
    return render(request, 'Apppoliconsultorio/listar_pacientes.html', context) 


#@login_required
@permission_required(['AppPoliconsultorio.change_turno','AppPoliconsultorio.delete_turno'])
def turno_medico(request):

    listado_especialidad = Especialidad.lista_especialidades()

    listado_medicos = Medico.lista_medicos()

    listado_disp_medicos = []

    context = {
        "listado_especialidad":listado_especialidad,
        "listado_medicos":listado_medicos,
        "listado_disp_medicos":listado_disp_medicos,
    }

    paciente_ya_se_valido = False
    buscar_turnos_ya_se_valido = False
    especialidad_ya_se_valido = True
    #estado_boton_buscar_turnos = 'disabled'
    #estado_boton_guardar_turno = 'disabled'

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        print("en el post la especialidad vuelve: ",request.POST['especialidad'])
        print("en el post la fecha vuelve: ",request.POST['fecha'])
        if request.POST['especialidad'] != 'Z':
            alta_turno_form = AltaTurnoForm(request.POST, especialidad=request.POST['especialidad'])
        if request.POST['especialidad'] == 'Z':
            alta_turno_form = AltaTurnoForm(request.POST)

        # Valido y proceso los datos.
        print(request.POST)

        if alta_turno_form.is_valid():
            if 'validar_paciente' in request.POST:
                #paciente = request.POST.get('paciente', None)
                paciente_consulto_su_existencia = Paciente.buscar_por_dni(request.POST.get('paciente', None))
                #if paciente == '11111111':
                if paciente_consulto_su_existencia != 'No-existe':
                    #paciente = 'Julia Zenko'
                    paciente = paciente_consulto_su_existencia
                    alta_turno_form.fields['paciente'].widget.attrs['readonly'] = True
                    alta_turno_form.fields['paciente'].widget.attrs['disabled'] = True
                    if request.POST.get('validar_paciente') == 'Paciente validado':
                        paciente_ya_se_valido = True
                    print('es el valor que le veo al boton de paciente antes del cambio: ',request.POST.get('validar_paciente'))
                    request.POST = request.POST.copy()
                    request.POST['validar_paciente'] = 'disabled'
                    #alta_turno_form.fields['validar_paciente'].widget.attrs['disabled'] = True
                    print('es el valor que le veo al boton de paciente: ',request.POST.get('validar_paciente'))
                    if paciente_ya_se_valido == False:
                        return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled'})
                else:
                    #return HttpResponse('Paciente no válido')
                    messages.add_message(request, messages.WARNING, 'Paciente Inexistente', extra_tags="tag1")
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'estado_boton_buscar_medicos': 'disabled', 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled'})

            # Nuevo para especialidad
            if alta_turno_form.cleaned_data['especialidad'] == 'Z':
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                # Le voy a cambiar a uno de los datos algo
                #paciente = 'Mabel Gandulfo' # luego comentar ya que lo va a seguir...
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
                messages.add_message(request, messages.WARNING, 'Debe elegir una Especialidad!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
                #Redirect to a new url:
                #return HttpResponseRedirect('/AppPoliconsultorio/turno_medico/')
                #Poner el mensaje falta elegir la fecha
            else:
                #Poner el mensaje falta elegir el turno
                #Hacer todo aqui porque si esta bien ok :)
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                print(request.POST)
                print('horario: ',request.POST.get("horario"))                
                alta_turno_form.fields['especialidad'].widget.attrs['readonly'] = True
                alta_turno_form.fields['especialidad'].widget.attrs['disabled'] = True
                if request.POST.get('validar_especialidad') != 'Especialidad validada':
                    especialidad_ya_se_valido = True
                if request.POST.get('validar_especialidad') == 'Especialidad validada':
                    especialidad_ya_se_valido = False
                print('es el valor que le veo al boton de validar la epecialidad antes del cambio: ',request.POST.get('validar_especialidad'))
                request.POST = request.POST.copy()
                request.POST['validar_especialidad'] = 'disabled'
                #alta_turno_form.fields['validar_paciente'].widget.attrs['disabled'] = True
                print('es el valor que le veo al boton de validar la especialidad: ',request.POST.get('validar_especialidad'))
                if especialidad_ya_se_valido != False:
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'enabled',  'estado_boton_guardar_turno': 'disabled'})
                #no se si poner un else aqui...

            # Fin nuevo para especialidad

            if alta_turno_form.cleaned_data['fecha'] is None or alta_turno_form.cleaned_data['medico'] == 'Z':
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                # Le voy a cambiar a uno de los datos algo
                #paciente = 'Mabel Gandulfo' # luego comentar ya que lo va a seguir...
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
                messages.add_message(request, messages.WARNING, 'Debe elegir un Médico y fecha!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_guardar_turno': 'disabled' })
                #Redirect to a new url:
                #return HttpResponseRedirect('/AppPoliconsultorio/turno_medico/')
                #Poner el mensaje falta elegir la fecha
            else:
                #Poner el mensaje falta elegir el turno
                #Hacer todo aqui porque si esta bien ok :)
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #print(request.POST)
                print('horario: ',request.POST.get("horario"))                
                alta_turno_form.fields['medico'].widget.attrs['readonly'] = True
                alta_turno_form.fields['medico'].widget.attrs['disabled'] = True
                alta_turno_form.fields['fecha'].widget.attrs['readonly'] = True
                alta_turno_form.fields['fecha'].widget.attrs['disabled'] = True  
                if request.POST.get('buscar_turnos') == 'busqueda validada':
                    buscar_turnos_ya_se_valido = True
                print('es el valor que le veo al boton de buscar turno antes del cambio: ',request.POST.get('buscar_turnos'))
                request.POST = request.POST.copy()
                request.POST['buscar_turnos'] = 'disabled'
                #alta_turno_form.fields['validar_paciente'].widget.attrs['disabled'] = True
                print('es el valor que le veo al boton de buscar turnos: ',request.POST.get('buscar_turnos'))
                if buscar_turnos_ya_se_valido == False:
                    print("el medico tiene el valor: ",alta_turno_form.cleaned_data['medico'])
                    #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar','','',''),'estado_boton_guardar_turno': 'enabled'})
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],''),'estado_boton_guardar_turno': 'enabled'})
                #no se si poner un else aqui...


            if alta_turno_form.cleaned_data['fecha'] is not None and request.POST.get("horario") is None:
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #print(request.POST)
                print('horario: ',request.POST.get("horario"))
                #paciente = 'Mabel Gandulfox'
                messages.add_message(request, messages.WARNING, 'Debe elegir un horario!', extra_tags="tag1")
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar','','','')})
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],''), 'estado_boton_guardar_turno': 'enabled'})


            if request.POST.get("horario") is not None:
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #paciente = 'Mabel Gandulfoz'
                print('registro el alta del turno')
                funcion_de_guardado_de_turno('actualizar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],request.POST.get("horario"))
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'alta_turno_form3': alta_turno_form3, 'paciente': paciente})
                return render(request,"AppPoliconsultorio/thanks.html")  
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'alta_turno_form3': alta_turno_form3, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
        else:
            #messages.add_message(request, messages.WARNING, alta_turno_form.errors, extra_tags="tag1")
            #print(alta_turno_form.errors)
            error_formulario = alta_turno_form.errors
            print('el error que viene de validar form: ',error_formulario)
            if 'paciente' in error_formulario:
                #alta_turno_form = AltaTurnoForm() # lo comente porque estoy pasandolo al fomr... 13-05-2023
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'error_formulario' : error_formulario, 'estado_boton_buscar_medicos': 'disabled', 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
            if 'fecha' in error_formulario:
                paciente = Paciente.buscar_por_dni(request.POST.get('paciente', None))
                #paciente = 'Julia Zenko'
                #especialidad = 'D'  #falta ubicar el valor...
                alta_turno_form.fields['paciente'].widget.attrs['disabled'] = True
                alta_turno_form.fields['especialidad'].widget.attrs['disabled'] = True
                request.POST = request.POST.copy()
                request.POST['validar_paciente'] = 'disabled'
                request.POST['validar_especialidad'] = 'disabled'
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'error_formulario' : error_formulario, 'estado_boton_buscar_turnos': 'enabled', 'estado_boton_guardar_turno': 'disabled' })

    else:
        # Creo el formulario vacío con los valores por defecto
        alta_turno_form = AltaTurnoForm()
    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'estado_boton_buscar_medicos': 'disabled' ,'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
    #return render(request,"AppPoliconsultorio/turnos.html",context)


@login_required
def baja_turno(request):
    listado_turnos = []
    errores = []

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        bajaturno_form = BajaTurnoForm(request.POST)
      
        if bajaturno_form.is_valid():
            dni = int(request.POST['dni'])    
            seleccionado = (request.POST.get('selectbajaturno'))
            todo = request.POST
            print(todo)
            print('selecciono el que voy a bajar: ', seleccionado)
            if seleccionado is None :    
                pacientes = Paciente.objects.filter(dni=dni)
                turnos_tabla = Turno.objects.filter(paciente=dni )                
                nombre = pacientes[0].nombre
                apellido= pacientes[0].apellido
                nombre_completo = f"{ apellido}, {nombre}"
                id = turnos_tabla[0].id
                # aca genero el listado_turnos: gte= mayor o igual a hoy                        
                listado_turnos = Turno.objects.filter(fecha__gte=date.today(), paciente=dni).order_by('fecha')
                return render(request, "AppPoliconsultorio/baja_turno.html", {'bajaturno_form': bajaturno_form, 'pacientel': nombre_completo, 'listado_turnos': listado_turnos  })
            else:
                turno = Turno.objects.filter(id=seleccionado)
                print('turno1: ', turno)
                funcion_de_guardado_de_turno('anular',request.POST.get('selectbajaturno'),'','','')
                # turno.save()
                
            # revisar los mensajes
                # turno.hora = ""
                
                                
                messages.add_message(request, messages.WARNING, 'Turno eliminado', extra_tags="tag1")

                context = {                        
                    "bajaturno_form": BajaTurnoForm,
                    "errores": errores,
                }

                return render(request, "AppPoliconsultorio/baja_turno.html", context)

    else: 
                
        bajaturno_form = BajaTurnoForm()
 
    context = {
        "listado_turnos": listado_turnos,
        "bajaturno_form": BajaTurnoForm,
        "errores": errores,
    }
    return render(request, "AppPoliconsultorio/baja_turno.html", context)

    #return HttpResponseRedirect('/AppPoliconsultorio/thanks/')

def eliminar_turno(request,id):
    print ("request", request)

    print ('request.id', request.id)
    print ('id', id)

    return redirect('/')

    # return render(request, 'Apppoliconsultorio/baja_turnos.html')  

@login_required
def consulta_turnos(request):
    listado_turnos = []
    errores = []
    nombre_completo = ""
    
    if request.method == "POST":
        consulta_turnos_form = ConsultaTurnosForm(request.POST)
        if consulta_turnos_form.is_valid():
            filtro_paciente = ""
            filtro_especialidad = ""
            filtro_medico = ""
            filtro_fechaDesde = ""
            filtro_fechaHasta = ""

            # Filtro por Paciente
            paciente_form = request.POST['paciente']
            if paciente_form != '':
                paciente = Paciente.objects.filter(dni = paciente_form)
                filtro_paciente = paciente[0].dni
                nombre_completo = paciente[0].nombre_completo

            # Filtro por Especialidad
            especialidad_form = request.POST['especialidad']
            if especialidad_form != 'Z':
                filtro_especialidad = especialidad_form

            # Filtro por Medico
            medico_form = request.POST['medico']
            if medico_form != 'Z':
                filtro_medico = int(medico_form)

            # Filtro por Fechas
            filtro_fechaDesde = request.POST['fechaDesde']
            filtro_fechaHasta = request.POST['fechaHasta']

            # Preparo el listado de turnos según los filtros cargados
            listado_turnos = Turno.lista_turnos(filtro_fechaDesde, filtro_fechaHasta, filtro_paciente, filtro_especialidad, filtro_medico)

        else:
            errores = consulta_turnos_form.errors
    else:
        consulta_turnos_form = ConsultaTurnosForm()

    context = {
        "listado_turnos": listado_turnos,
        "consulta_turnos_form": consulta_turnos_form,
        "errores": errores,
        "nombre_completo": nombre_completo,
    }
    return render(request, "AppPoliconsultorio/consulta_turno.html", context)


@login_required
def listar_turnos(request):
    context = {}

    turnos = Turno.objects.all()
    resultado = []
    for turno in turnos:
        item = {
            'dia': turno.fecha,
            'horario': turno.hora,
            'medico': (
                f"{turno.medico.nombre} {turno.medico.apellido} ({turno.medico.especialidad.descripcion})"
                if turno.medico is not None else ''
            ),
            'paciente': (
                f"{turno.paciente.nombre} {turno.paciente.apellido} (DNI: {turno.paciente.dni})"
                if turno.paciente is not None else ' SIN PACIENTE'
            )
        }
        resultado.append(item)

    context['listado_turnos'] = resultado
    return render(request, 'Apppoliconsultorio/listar_turnos.html', context)  


def usuarios(request):
    context = {}
    return render (request,"AppPoliconsultorio/usuarios.html", context)


def contactenos(request):
    context = {}
    return render (request,"AppPoliconsultorio/contactenos.html", context)


def contacto(request):
    if request.method == "POST":
    # Creo la instancia del formulario con los datos cargados en pantalla
        contacto_form = ContactoForm(request.POST)
        # Valido y proceso los datos.
        if contacto_form.is_valid():
            #Process the data in form.cleaned_data as required # ...
            # De esta manera veo los datos que fueron completados en el formulario
            print('Nombre: ',contacto_form.cleaned_data['nombre'])
            print('Apellido: ',contacto_form.cleaned_data['apellido'])
            print('Email: ',contacto_form.cleaned_data['email'])
            #Redirect to a new url:
            return HttpResponseRedirect('/AppPoliconsultorio/thanks/')
    else:
        # Creo el formulario vacío con los valores por defecto
        contacto_form = ContactoForm()
    return render(request, "AppPoliconsultorio/contacto.html", {'contacto_form': contacto_form})
    

def thanks(request): #new
    context = {}
    return render(request,"AppPoliconsultorio/thanks.html",context)


def turnos(request):
    context = {}
    return render (request,"AppPoliconsultorio/turnos.html", context)
