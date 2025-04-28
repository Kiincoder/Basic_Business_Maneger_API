from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from app.models import Despesas, Departamento  

from app.utils.utils import verifica_campo_faltante
import datetime
from django.db.models import Sum, Max, Min, Avg



@csrf_exempt
@require_http_methods(["POST"])
def baixa_despesa(request):
  if request.method == "POST":
    data = json.loads(request.body.decode("utf-8"))
  
    if verifica_campo_faltante(data=data, campo_requerido=["nome", "valor", "cod_departamento"]):
      return JsonResponse({"message": "Campo faltante!"}, status=400)

    try:
      departamento = Departamento.objects.get(nome=data.get("cod_departamento"))

      Despesas.objects.create(
        nome=data.get("nome"),
        valor=data.get("valor"),
        data_pagamento=datetime.date.today(),
        cod_departamento=departamento
      )

      return JsonResponse({"message": "Despesa criada com sucesso!"}, status=201)
    
    except Departamento.DoesNotExist:
      return JsonResponse({"message": "Departamento não encontrado!"}, status=404)

    except Exception as e:
      return JsonResponse({"message": f"Erro ao criar empregado: {str(e)}"}, status=500)

  
  return JsonResponse({"message": "Método inválido!"}, status = 405)



@csrf_exempt
@require_http_methods(["GET"])
def listar_despesas(request):
  if request.method == "GET":

    despesas = Despesas.objects.all()
    
    lista_temp = []

    for despesa in despesas:
      lista_temp.append({
        "nome":despesa.nome,
        "valor":despesa.valor,
        "data_pagamento":despesa.data_pagamento,
        "cod_departamento":despesa.cod_departamento.nome
      })
    return JsonResponse(lista_temp, safe=False, status=200)

  return JsonResponse({"message": "Método inválido!"}, status=405)

@csrf_exempt
@require_http_methods(["GET"])
def listar_despesa_por_dpto(request, id):
  try:
    despesas = Despesas.objects.filter(cod_departamento__nome=id)
    
    if not despesas.exists():
      return JsonResponse({"message": "Nenhuma despesa encontrada para este departamento!"}, status=404)

    lista_temp = []
    for despesa in despesas:
      lista_temp.append({
        "nome": despesa.nome,
        "valor": despesa.valor,
        "data_pagamento": despesa.data_pagamento,
        "cod_departamento": despesa.cod_departamento.nome
      })

    return JsonResponse(lista_temp, safe=False, status=200)

  except Exception as e:
    return JsonResponse({"message": f"Erro ao listar despesas: {str(e)}"}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def listar_metricas_por_dpto(request, id):
  try:
    despesas = Despesas.objects.filter(cod_departamento__nome=id)
    
    if not despesas.exists():
      return JsonResponse({"message": "Nenhuma despesa encontrada para este departamento!"}, status=404)

    despesas_por_mes = despesas.values('data_pagamento__year', 'data_pagamento__month').annotate(
      total=Sum('valor')
    )

    total_valores = despesas.aggregate(
      min=Min('valor'),
      max=Max('valor'),
      media_total=Avg('valor')
    )

    media_mensal = despesas_por_mes.aggregate(media_mensal=Avg('total'))['media_mensal']
    media_anual = despesas.values('data_pagamento__year').annotate(
      total_anual=Sum('valor')
    ).aggregate(media_anual=Avg('total_anual'))['media_anual']

    mes_mais_gasto = max(despesas_por_mes, key=lambda x: x['total'], default=None)
    mes_menos_gasto = min(despesas_por_mes, key=lambda x: x['total'], default=None)

    despesa_mais_cara = despesas.order_by('-valor').first()

    response = {
      "min": total_valores['min'],
      "max": total_valores['max'],
      "media_total": total_valores['media_total'],
      "media_mensal": media_mensal,
      "media_anual": media_anual,
      "mes_mais_gasto": {
        "ano": mes_mais_gasto['data_pagamento__year'],
        "mes": mes_mais_gasto['data_pagamento__month'],
        "total": mes_mais_gasto['total']
      } if mes_mais_gasto else None,
      "mes_menos_gasto": {
        "ano": mes_menos_gasto['data_pagamento__year'],
        "mes": mes_menos_gasto['data_pagamento__month'],
        "total": mes_menos_gasto['total']
      } if mes_menos_gasto else None,
      "despesa_mais_cara": {
        "nome": despesa_mais_cara.nome,
        "valor": despesa_mais_cara.valor,
        "data_pagamento": despesa_mais_cara.data_pagamento,
        "cod_departamento": despesa_mais_cara.cod_departamento.nome
      } if despesa_mais_cara else None,
    }

    return JsonResponse(response, safe=False, status=200)

  except Exception as e:
    return JsonResponse({"message": f"Erro ao listar despesas: {str(e)}"}, status=500)