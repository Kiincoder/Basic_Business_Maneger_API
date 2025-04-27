from django.db import models

class Departamento(models.Model):
    cod_departamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)

class Despesas(models.Model):
    cod_despesa = models.AutoField(primary_key=True)
    cod_departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()

class Empregado(models.Model):
    cod_empregado = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    idade = models.IntegerField()
    cod_departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    contato = models.CharField(max_length=15, unique=True)
    cargo = models.CharField(max_length=100)
    
class Materiais(models.Model):
    cod_item = models.AutoField(primary_key=True)
    nome_item = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    cod_departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)
    solicitado = models.BooleanField(default=False)

class Solitacoes_de_compras(models.Model):
    cod_solicitacao = models.AutoField(primary_key=True)
    cod_item = models.ForeignKey('Materiais', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    cod_empregado = models.ForeignKey('Empregado', on_delete=models.CASCADE)
    data_solicitacao = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Rejeitado', 'Rejeitado')])