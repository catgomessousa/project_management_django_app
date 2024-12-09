from django.forms import ModelForm, DateInput
from django import forms
from .models import Project, Task
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

class AdminTask(TreeAdmin):
    list_display = ("name", "progress", "start","end", 'project')
    list_editable = ("progress", 'start','end', 'project')
    list_filter = ("project",)
    form = movenodeform_factory(Task)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'resumo': forms.TextInput(attrs={'class': 'form-control', 'size': 5}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_entrega': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'ordem_fabrico': forms.TextInput(attrs={'class': 'form-control'}),

        }


class TaskForm(MoveNodeForm):
    class Meta:
        model = Task
        exclude = ('path', 'depth', 'numchild')
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'progress': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),


         }
