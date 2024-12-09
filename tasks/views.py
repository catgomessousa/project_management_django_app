# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from tasks.models import Task, Project, fornecedor
import json
from .forms import ProjectForm, TaskForm

from datetime import datetime, date
from datetime import timedelta
import calendar
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar


class TaskView(TemplateView):
    template_name ="index.html"

    def process(self, t):
        task = t.to_dict()
        for i in ('path', 'depth', 'path', 'numchild','project'):
            if i in task:
                del task[i]
        task['id'] = str(task['id'])
        childrens = [c.id for c in t.get_children()]
        task["dependencies"] = ",".join([str(i) for i in childrens])

        return task

    def get_context_data(self, **kwargs):
        ctx = super(TaskView, self).get_context_data(**kwargs)
        id = self.request.GET.get("id",None)

        if not id:
            tasks = Task.objects.none()
        else:
            tasks = Task.objects.filter(project__id=id)

        ctx["id"] = id
        ctx["projects"] = Project.objects.all().order_by('data_entrega') # todas as encomendas por ordem de entrega
        date_min= datetime.today() - timedelta(days=7) #data min data atual -7 dias
        date_max= '2050-01-31' #data maxima
        ctx["projects"] = Project.objects.filter(data_entrega__range= (date_min, date_max)).order_by('data_entrega') #filtrar as datas entre a min e max
        ctx["tasks_count"] = tasks.count()
        ctx["tasks"] = json.dumps([ self.process(t) for t in tasks])
        return ctx




def encomendas(request):
    data= {}
    data['encomendas'] = Project.objects.all().order_by('data_entrega')
    date_min = datetime.today() - timedelta(days=7)  # data min data atual -7 dias
    date_max = '2050-01-31'  # data maxima
    data["encomendas"] = Project.objects.filter(data_entrega__range=(date_min, date_max)).order_by('data_entrega')
    return render(request, 'tasks/encomendas.html', data)

def inserir(request):
    data ={}
    form= ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('programa-encomendas')

    data['form']= form
    return render(request, 'tasks/inserir.html', data)


def planear(request, pk):
    data={}
    data['ordens'] =Task.objects.filter(project_id=pk)
    Encomenda = Project.objects.get(pk=pk)
    data['encomenda'] = Encomenda
    return render(request, 'tasks/planear.html', data)


def update(request, pk):
    data= {}
    Encomenda = Project.objects.get(pk=pk)
    form = ProjectForm(request.POST or None, instance=Encomenda)

    if form.is_valid():
        form.save()
        return redirect('programa-encomendas')

    data['form']= form
    data['obj']= Encomenda
    return render(request, 'tasks/inserir.html', data)

def delete(request, pk):
    Encomenda = Project.objects.get(pk=pk)
    Encomenda.delete()
    return redirect('programa-encomendas')


def inserir_ordem(request, pk):
    data ={}
    form: TaskForm= TaskForm(request.POST or None)
    form.fields["project"].queryset = Project.objects.filter(pk=pk)
    #form.fields["node"].queryset = Task.objects.filter(project_id=pk)
    Encomenda = Project.objects.get(pk=pk)
    data['encomenda'] = Encomenda

    if form.is_valid():
        form.save()
        url = reverse('home')
        id = str(Encomenda.id)
        url = url + '?id=' + id
        return redirect(url)

    data['form']= form
    return render(request, 'tasks/inserir_ordem.html', data)

def update_ordem(request,pk, id):
    data= {}
    Ordem = Task.objects.get(pk=id)
    form = TaskForm(request.POST or None, instance=Ordem)
    form.fields["project"].queryset = Project.objects.filter(pk=pk) #so se pode escolher aquela encomenda ja selecionada
    Encomenda = Project.objects.get(pk=pk)
    data['encomenda'] = Encomenda
    if form.is_valid():
        form.save()
        url = reverse('home')
        id = str(Encomenda.id)
        url = url + '?id=' + id
        return redirect(url)

    data['form']= form
    data['obj']= Ordem
    return render(request, 'tasks/inserir_ordem.html', data)

def delete_ordem(request,pk, id):
    Ordem = Task.objects.get(pk=id)
    Ordem.delete()
    Encomenda = Project.objects.get(pk=pk)
    url = reverse('home')
    id = str(Encomenda.id)
    url = url + '?id=' + id
    return redirect(url)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(generic.ListView):
    model = Project
    template_name = 'tasks/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

