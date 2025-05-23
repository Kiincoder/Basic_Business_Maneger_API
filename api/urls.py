from django.contrib import admin
from django.urls import path
from app.controllers.EmployesController import *
from app.controllers.ExpensesController import *
from app.controllers.MaterialsController import *
from app.controllers.RequestsController import *

urlpatterns = [
    path('api/empregados/', list_all), # Lista tods empregados
    path('api/empregados/criar/', create), # Cria um empregado
    path('api/empregados/informacao/', information_by_name), # Retorna informações de um empregado
    path('api/empregados/atualizar/', update), # Atualiza um empregado
    path('api/empregados/atualizarcampo/', update_field), # Atualiza um campo de um empregado
    path('api/empregados/deletar/', delete), # Deleta um empregado

    path('api/despesas/', listar_despesas), # Lista todas despesas
    path('api/despesas/criar', baixa_despesa), # Cria uma despesa no sistema
    path('api/despesas/<str:id>/', listar_despesa_por_dpto), # Lista despesas de um setor
    path('api/despesas/<str:id>/metricas/', listar_metricas_por_dpto), # Lista despesas de um setor com métricas

    path('api/materiais/', listar_materiais), # Lista todos materiais
    path('api/materiais/acrescentar/', acrescentar_qtd), # Acresce quantidade
    path('api/materiais/decrescentar/', decrescer_qtd), # Decresce quantidade
    path('api/materiais/remover/', remover), # Remove um material
    path('api/materiais/criar/', criar), # Cria um novo material


    path('api/solicitacoes/<int:id>/status', status), # Retorna o status de uma solicitação
    path('api/solicitacoes/<int:id>/aprovar', aprovar), # Aprova uma solicitação de compra
    path('api/solicitacoes/<int:id>/rejeitar', rejeitar), # Rejeita uma solicitação de compra
    path('api/solicitacoes/<int:id>/finalizar', finalizar), # Finaliza uma determinada solicitação
    path('api/solicitacoes/solicitar', solicitar) # Cria uma solicitação de compra 
]
