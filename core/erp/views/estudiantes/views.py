from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import EstudianteForm
from core.erp.models import Estudiante

class EstudiantesListView(ListView):
    model = Estudiante
    template_name = 'estudiantes/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Estudiante.objects.all():
                    data.append(i.toJSON())
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Estudiantes'
        context['create_url'] = reverse_lazy('erp:estudiante_create')
        context['list_url'] = reverse_lazy('erp:estudiante_list')
        context['entity'] = 'Estudiantes'
        return context
    


class EstudiantesCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiantes/create.html'
    success_url = reverse_lazy('erp:estudiante_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Estudiante'
        context['entity'] = 'Estudiantes'
        context['list_url'] = reverse_lazy('erp:estudiante_list')
        context['action'] = 'add'
        return context

class EstudiantesUpdateView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiantes/create.html'
    success_url = reverse_lazy('erp:estudiante_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Estudiante'
        context['entity'] = 'Estudiantes'
        context['list_url'] = reverse_lazy('erp:estudiante_list')
        context['action'] = 'edit'
        return context

class EstudiantesDeleteView(DeleteView):
    model = Estudiante
    template_name = 'estudiantes/delete.html'
    success_url = reverse_lazy('erp:estudiante_list')
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Estudiante'
        context['entity'] = 'Estudiantes'
        context['list_url'] = reverse_lazy('erp:estudiante_list')
        return context
