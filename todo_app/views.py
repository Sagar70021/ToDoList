from django.shortcuts import render,redirect
from django.views.generic import FormView,DeleteView,UpdateView,CreateView,DetailView,ListView,TemplateView
from todo_app import models
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todo_app:list')

class Registerpage(FormView):
    template_name = 'todo_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todo_app:list')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(Registerpage,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('todo_app:list')

        return super(Registerpage,self).get(*args,**kwargs)


# Create your views here.

#class IndexView(TemplateView):
#    template_name = 'todo_app/task_base.html'



class TaskList(LoginRequiredMixin,ListView):
    context_object_name = 'tasks'
    model = models.Task

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = models.Task
    template_name = 'todo_app/task_detail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = models.Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('todo_app:list')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = models.Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('todo_app:list')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = models.Task
    success_url = reverse_lazy('todo_app:list')
