from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.utils.utils import verifica_campo_faltante

import datetime
import json

from app.models import Empregado
from app.models import Materiais  
from app.models import Solitacoes_de_compras


@csrf_exempt
@require_http_methods(["GET"])
def status(request, id):
  solicitacao = Solitacoes_de_compras.objects.get(cod_solicitacao=id)

  return JsonResponse({
  "status":solicitacao.status,
  }, status=200)


@csrf_exempt
@require_http_methods(["PATCH"])
def aprovar(request, id):
  if request.method == "PATCH":    
    try:
      solicitacao = Solitacoes_de_compras.objects.get(cod_solicitacao=id)
      solicitacao.status = "Aprovada"
      solicitacao.save()

      return JsonResponse({"message":f"Solicitação {id} aprovada!"}, status=200)
    
    except Exception as e:
      return JsonResponse({"message": f"Erro ao rejeitar: {str(e)}"}, status=500)



@csrf_exempt
@require_http_methods(["PATCH"])
def rejeitar(request, id):
  if request.method == "PATCH":    
    try:
      solicitacao = Solitacoes_de_compras.objects.get(cod_solicitacao=id)
      solicitacao.status = "Rejeitado"
      solicitacao.save()

      return JsonResponse({"message":f"Solicitação {id} rejeitada!"}, status=200)
    
    except Exception as e:
      return JsonResponse({"message": f"Erro ao rejeitar: {str(e)}"}, status=500)



@csrf_exempt
@require_http_methods(["DELETE"])
def finalizar(request, id):
  if request.method == "DELETE":    
    try:
      solicitacao = Solitacoes_de_compras.objects.get(cod_solicitacao=id)
      material = Materiais.objects.get(cod_item=solicitacao.cod_item.cod_item)
      
      material.solicitado = False
      material.save()

      solicitacao.delete()
      return JsonResponse({"message":f"Solicitação {id} deletado!"}, status=200)
    
    except Exception as e:
      return JsonResponse({"message": f"Erro ao deletar: {str(e)}"}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def solicitar(request):
  if request.method == "POST":
    data = json.loads(request.body.decode("utf-8"))
  
    if verifica_campo_faltante(data=data, campo_requerido=["nome_do_item", "nome_do_empregado", "quantidade"]):
      return JsonResponse({"message": "Campo faltante!"}, status=400)

    try:
      material = Materiais.objects.get(nome_item=data.get("nome_do_item"))
      empregado = Empregado.objects.get(nome=data.get("nome_do_empregado"))

      Solitacoes_de_compras.objects.create(
        cod_item = material,
        quantidade = data.get("quantidade"),
        cod_empregado = empregado,
        data_solicitacao = datetime.date.today(),
        status = "Pendente"
      )

      material.solicitado = True
      material.save()

      return JsonResponse({"message": "Solicitacao criada com sucesso!"}, status=201)
    
    except Materiais.DoesNotExist:
      return JsonResponse({"message": "Item não encontrado!"}, status=404)
    
    except Empregado.DoesNotExist:
      return JsonResponse({"message": "Empregado não encontrado!"}, status=404)

    except Exception as e:
      return JsonResponse({"message": f"Erro ao criar solicitacao: {str(e)}"}, status=500)

  
  return JsonResponse({"message": "Método inválido!"}, status = 405)

