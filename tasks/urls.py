
from django.urls import path, include
from . import views

urlpatterns = [
    path('encomendas/', views.encomendas, name='programa-encomendas'),
    path('encomendas/inserir/', views.inserir, name='programa-inserir'),
    path('encomendas/<str:pk>/update/', views.update, name='programa-update'),
    path('encomendas/<str:pk>/delete/', views.delete, name='programa-delete'),
    path('encomendas/<str:pk>/planear/', views.planear, name='programa-planear'),
    path('encomendas/<str:pk>/planear/inserir_ordem/', views.inserir_ordem, name='programa-inserir_ordem'),
    path('encomendas/<str:pk>/planear/update_ordem/<str:id>/', views.update_ordem, name='programa-update_ordem'),
    path('encomendas/<str:pk>/planear/delete_ordem/<str:id>/', views.delete_ordem, name='programa-delete_ordem'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),

]