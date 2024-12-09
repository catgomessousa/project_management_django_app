# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from treebeard.mp_tree import MP_Node
from django.db import models
from django_model_to_dict.mixins import ToDictMixin
from django.urls import reverse

class cliente(models.Model):
    codigo_cliente= models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.codigo_cliente

class fornecedor(models.Model):
    nome_fornecedor= models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome_fornecedor

    class Meta:
        verbose_name_plural = 'fornecedores'


class Project(ToDictMixin, models.Model):
    resumo = models.CharField(max_length=200)
    Estados = (
        ('Aceite', 'Aceite'),
        ('Rejeitada', 'Rejeitada'),
        ('Ongoing', 'Ongoing'),
    )
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    data_entrega = models.DateField()
    quantidade = models.IntegerField()
    estado = models.CharField(max_length=20, choices=Estados)
    ordem_fabrico = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{}".format(self.resumo)

    @property
    def get_html_url(self):
        url = reverse('home')
        id= str(self.id)
        url = url + '?id=' + id
        return f'<a href="{url}"> {self.resumo} </a>'

class Task(MP_Node, ToDictMixin):
    Estados = (
        ('Confirmada', 'Confirmada'),
        ('Planeada', 'Planeada'),
    )
    #Tipos = (
        #('Malha', 'Malha'),
        #('Estampar_metro', 'Estampar ao metro'),
        #('Corte', 'Corte'),
        #('Confecao', 'Confecao'),
        #('Embalagem', 'Embalagem'),
        #('Estamparia', 'Estamparia'),
        #('Bordador', 'Bordador'),
        #('Tinto peca', 'Tinto em peca'),
        #('Lavagem', 'Lavagem'),
        #('Bordar etiqueta metalica', 'Bordar etiqueta metalica'),
        #('Casear botoes', 'Casear botoes'),
        #('Aplicar transferes', 'Aplicar transferes'),
        #('Pregar molas', 'Pregar molas'),
    #)
    name = models.CharField(max_length=200, verbose_name="Tipo") #choices=Tipos,
    project = models.ForeignKey("Project", related_name="tasks",
                                blank=True, on_delete=models.CASCADE, verbose_name="Encomenda")
    start = models.DateField(verbose_name="Data inicio")
    end = models.DateField(verbose_name="Data Fim")
    progress = models.PositiveIntegerField(default=0, verbose_name="Progresso")
    fornecedor = models.ForeignKey('fornecedor', to_field= 'nome_fornecedor', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    estado = models.CharField(max_length=20, choices=Estados)
    subcontrato=models.CharField(max_length=20,  null=True, blank=True)


    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{}".format(self.name)

