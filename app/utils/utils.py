def verifica_campo_faltante(data, campo_requerido):
  
  verificacao = [campo for campo in campo_requerido if campo not in data or not data.get(campo)]
  return verificacao