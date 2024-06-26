from django.views import View
from django.shortcuts import render
from django.contrib import messages 

######################### Vista Base ###########################


class BaseListView(View):
    form_class = None
    model = None
    lista_objetos = None
    template_name = ''
    redirige = ''
    context_object_name = 'lista'
    title = ''
    encabezados = []
    campos = []

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(post_data=request.POST, files=request.FILES, peticion=request)
        return render(request, self.template_name, context)

    def get_context_data(self, post_data=None, files=None, peticion= None):
        context = {}
        if post_data:
            if 'save' in post_data:
                print(f"Se entro en SAVE")
                pk = post_data.get('save')
                if not pk:
                    form = self.form_class(post_data, files)
                    if form.is_valid():
                        form.save()
                        form = self.form_class()
                        #return redirect(reverse(self.redirige, post_data, files))
                    #form = self.form_class()
                else:
                    print(f"Se entro el id = {pk}")
                    objeto = self.model.objects.get(id=pk)
                    form = self.form_class(post_data, files, instance=objeto)
                    if form.is_valid():
                        form.save()
                        #return redirect(reverse(self.redirige))
                    else:
                        messages.warning(peticion, f"Fallo el guardado por: {form.errors}")
                
            elif 'delete' in post_data:
                pk = post_data.get('delete')
                objeto = self.model.objects.get(pk=pk)
                objeto.delete()
                form = self.form_class() 
            elif 'edit' in post_data:
                pk = post_data.get('edit')
                objeto = self.model.objects.get(pk=pk)
                form = self.form_class(instance=objeto)
        else:
            form = self.form_class()

        context['lista'] = self.lista_objetos if self.lista_objetos is not None else self.model.objects.all()
        context['form'] = form 
        context['titulo'] = self.title
        context['encabezados'] = self.encabezados
        context['campos'] = self.campos
        context['redirige'] = self.redirige
        return context