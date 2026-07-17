from django.urls import path
from quiz import views

urlpatterns = [
    path('', views.iniciar, name='quiz_inicio'),
    path('prova/<int:prova_id>/questao/<int:ordem>/', views.responder, name='quiz_responder'),
    path('prova/<int:prova_id>/resultado/', views.resultado, name='quiz_resultado'),
    path('prova/<int:prova_id>/pdf/', views.pdf, name='quiz_pdf'),
]
