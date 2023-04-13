from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.forms import inlineformset_factory

from django.urls import reverse_lazy, reverse
from django.http import  HttpResponseRedirect

from .models import Task, TaskStep

from .forms import TaskForm, RegisterUserForm, LoginUserForm, TaskFormSet

from django.db.models import Q
from django.db import models
from django.utils import timezone
from datetime import timedelta
from datetime import date

# Create your views here.


def index(request):
    return render(request, 'core/base.html')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'core/task_list.html'
    login_url = '/login/'

    # result = Task.objects.aggregate(
    # today=models.Count('id', filter=models.Q(created__date=now.date())),
    # last_3_days=models.Count('id', filter=models.Q(created__date__gte=(now - timedelta(days=3)).date())),
    # last_7_days=models.Count('id', filter=models.Q(created__date__gte=(now - timedelta(days=7)).date())),
    # )
    # context = {'result': result}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
       
        #3days/today 
        # last_3_days = Task.objects.filter(user_date__lte=(now + timedelta(days=3)))
        last_3_days = Task.objects.filter(user_date__gte=(now - timedelta(days=3)))
        # today = Task.objects.filter(user_date__lte=(now + timedelta(days=1)))
        today = Task.objects.filter(user_date__lte=(now + timedelta(days=1)))
     
        overdue = Task.objects.filter(user_date__lte=(now))
        all_tasks = Task.objects.all()

        steps = TaskStep.objects.filter()

        context = {
        'today': today,
        'last_3_days': last_3_days,
        'overdue': overdue,
        'all_tasks': all_tasks,
        'steps': steps,
        }
        return context
    
# class TaskDetail(DetailView):
#     model = Task
#     template_name = 'core/task_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

def detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'core/task_detail.html', {'task': task})


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy('tasks') 
    template_name = 'core/task_form.html'
    form_class = TaskForm

    def get_context_data(self, user_id=None, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        
        context['form'] = TaskForm()
        context['formset'] = TaskFormSet(prefix='fs1')
        context['user'] =  self.request.user
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        task_step_formset = TaskFormSet(self.request.POST, prefix='fs1')

        if form.is_valid() and task_step_formset.is_valid():
            return self.form_valid(form, task_step_formset)
        else:
            return self.form_invalid(form, task_step_formset)
        
    def form_valid(self, form, task_step_formset):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        task_step = task_step_formset.save(commit=False)
        for i in task_step:
            i.task = self.object
            i.save()
        return redirect(reverse("tasks"))
    
    def form_invalid(self, form, task_step_formset):
        print('invalid')
        return self.render_to_response(self.get_context_data(form=form, task_step_formset=task_step_formset))
        

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    context_object_name = 'task'
    template_name = 'core/task_confirm_delete.html'

def logoutUser(request):
    logout(request)
    return redirect('tasks')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('tasks')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('tasks')
