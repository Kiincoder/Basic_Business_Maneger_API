from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.models import Materiais
from app.models import Departamento
from app.utils.utils import verifica_campo_faltante

import json


@csrf_exempt
@require_http_methods(["GET"])
def listar_materiais(request):
  materias = Materiais.objects.all()
  temp_list = []
  for material in materias:
    temp_list.append({
      "cod": material.cod_item,
      "nome": material.nome_item,
      "quantidade": material.quantidade,
      "status_solictacao": material.solicitacao,
      "cod_departamento": material.cod_departamento
    })
    
  return JsonResponse({"data": temp_list}, status=200)




@csrf_exempt
@require_http_methods(["POST"])
def criar(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body.decode('utf-8'))

      if verifica_campo_faltante(data, ["nome", "quantidade", "cod_departamento"]):
          return JsonResponse({"message": "Dados inválidos ou incompletos!"}, status=400)

      try:
          departamento = Departamento.objects.get(nome=data.get("cod_departamento"))
      except Departamento.DoesNotExist:
          return JsonResponse({"message": "Departamento não encontrado!"}, status=404)

      Materiais.objects.create(
        nome_item=data.get("nome"),
        quantidade=data.get("quantidade"),
        cod_departamento=departamento
      )

      return JsonResponse({"message": "Material criado com sucesso!"}, status=201)
    except Exception as e:
      return JsonResponse({"message": f"Erro ao criar material: {str(e)}"}, status=500)
    
  return JsonResponse({"message": "Método inválido!"}, status=405)



@csrf_exempt
@require_http_methods(["PATCH"])
def atualizar_qtd(request):
  material = Materiais.objects.get(cod_item=json.loads(request.body.decode("utf-8")).get("cod_item"))
  material.quantidade = material.quantidade + 1
  material.save()

  return JsonResponse({"a":"das"}, status=200)

@csrf_exempt
@require_http_methods(["DELETE"])
def remover(request):
  if request.method == "DELETE":
    data = json.loads(request.body.decode("utf-8"))
    cod_item = data.get("cod_item")
    
    try:
      material = Materiais.objects.get(cod_item= cod_item)
      material.delete()
      return JsonResponse({"message":"Item deletado!"}, status=200)
    
    except Exception as e:
      return JsonResponse({"message": f"Erro ao deletar: {str(e)}"}, status=500)