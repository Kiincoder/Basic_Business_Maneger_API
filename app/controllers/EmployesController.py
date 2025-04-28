from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.utils.utils import verifica_campo_faltante

import json

from app.models import Empregado
from app.models import Departamento  

@csrf_exempt
@require_http_methods(["GET"])
def list_all(request):
  if request.method == "GET":
    empregados = Empregado.objects.all()
    empregados_list = []
    for empregado in empregados:
      empregados_list.append({
        "nome_completo": f"{empregado.nome} {empregado.sobrenome}",
        "cpf": empregado.cpf,
        "idade": empregado.idade,
        "cod_departamento": empregado.cod_departamento.nome,
        "email": empregado.email,
        "contato": empregado.contato,
        "cargo": empregado.cargo
      })
    return JsonResponse(empregados_list, safe=False, status=200)

  return JsonResponse({"message": "Método inválido!"}, status=405)


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body.decode('utf-8'))

      if verifica_campo_faltante(data=data, campo_requerido=["cod_empregado", "nome", "sobrenome", "cpf", "idade", "email", "contato", "cargo"]):
        return JsonResponse({"message": "Campo faltante!"}, status=400) 
      
      departamento = Departamento.objects.get(nome=data.get("cod_departamento"))
      Empregado.objects.create(
        nome = data.get("nome"),
        sobrenome = data.get("sobrenome"),
        cpf = data.get("cpf"),
        idade = data.get("idade"),
        cod_departamento = departamento,
        email = data.get("email"),
        contato = data.get("contato"),
        cargo = data.get("cargo")
      )
      return JsonResponse({"message": "Empregado criado com sucesso!"}, status=201)
    except Exception as e:
      return JsonResponse({"message": f"Erro ao criar empregado: {str(e)}"}, status=500)
    
  return JsonResponse({"message": "Método inválido!"}, status=405)

@csrf_exempt
@require_http_methods(["GET"])
def information_by_name(request):
  if request.method == "GET":
      data = json.loads(request.body.decode('utf-8'))
      
      if "cod_empregado" not in data:
        return JsonResponse({"message": "Campo faltante!"}, status=400)
      
      try:
          empregado = Empregado.objects.get(cod_empregado=data.get("cod_empregado"))
      except Empregado.DoesNotExist:
          return JsonResponse({"message": "Empregado não encontrado!"}, status=404)


      return JsonResponse({
        "nome_completo": f"{empregado.nome} {empregado.sobrenome}",
        "cpf": empregado.cpf,
        "idade": empregado.idade,
        "cod_departamento": empregado.cod_departamento.nome,
        "email": empregado.email,
        "contato": empregado.contato,
        "cargo": empregado.cargo
      }, status=200)

  return JsonResponse({"message": "Método inválido!"}, status=405)

@csrf_exempt
@require_http_methods(["PUT"])
def update(request):
  if request.method == "PUT":
    try:
      data = json.loads(request.body.decode('utf-8'))

      if verifica_campo_faltante(data=data, campo_requerido=["cod_empregado", "nome", "sobrenome", "cpf", "idade", "email", "contato", "cargo"]):
        return JsonResponse({"message": "Campo faltante!"}, status=400)

      empregado = Empregado.objects.get(cod_empregado=data.get("cod_empregado"))
      departamento = None

      if "cod_departamento" in data:
        departamento = Departamento.objects.get(nome=data.get("cod_departamento"))
      
      empregado.nome = data.get("nome", empregado.nome)
      empregado.sobrenome = data.get("sobrenome", empregado.sobrenome)
      empregado.cpf = data.get("cpf", empregado.cpf)
      empregado.idade = data.get("idade", empregado.idade)
      empregado.cod_departamento = departamento if departamento else empregado.cod_departamento
      empregado.email = data.get("email", empregado.email)
      empregado.contato = data.get("contato", empregado.contato)
      empregado.cargo = data.get("cargo", empregado.cargo)
      
      empregado.save()
      return JsonResponse({"message": "Empregado atualizado com sucesso!"}, status=200)
    
    except Empregado.DoesNotExist:
      return JsonResponse({"message": "Empregado não encontrado!"}, status=404)
    
    except Departamento.DoesNotExist:
      return JsonResponse({"message": "Departamento não encontrado!"}, status=404)
    
    except Exception as e:
      return JsonResponse({"message": f"Erro ao atualizar empregado: {str(e)}"}, status=500)


@csrf_exempt
@require_http_methods(["PATCH"])
def update_field(request):
  if request.method == "PATCH":
    data = json.loads(request.body.decode('utf-8'))
    empregado = Empregado.objects.get(cod_empregado=data.get("cod_empregado"))

    if len(data.keys()) == 2: 
      for i in data.keys():
        if i != "cod_empregado":
          campo = i

      try:
        valor = data.get(str(campo))

        if not campo or not hasattr(empregado, campo):
          return JsonResponse({"message": "Campo inválido!"}, status=400)

        setattr(empregado, campo, valor)
        empregado.save()

        return JsonResponse({"message": f"Campo '{campo}' atualizado com sucesso!"}, status=200)
      
      except Empregado.DoesNotExist:
        return JsonResponse({"message": "Empregado não encontrado!"}, status=404)
      
      except Exception as e:
        return JsonResponse({"message": f"Erro ao atualizar campo: {str(e)}"}, status=500)


    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete(request):
  if request.method == "DELETE":
    data = json.loads(request.body.decode("utf-8"))
    empregado_id = data.get("cod_empregado")
    
    try:
      empregado = Empregado.objects.get(cod_empregado= empregado_id)
      empregado.delete()
      return JsonResponse({"message":"Empregado deletado!"}, status=200)
    
    except Exception as e:
      return JsonResponse({"message": f"Erro ao deletar: {str(e)}"}, status=500)

