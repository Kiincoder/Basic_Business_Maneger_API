# Generated by Django 5.2 on 2025-04-24 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('cod_departamento', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Despesas',
            fields=[
                ('cod_despesa', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_pagamento', models.DateField()),
                ('cod_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Empregado',
            fields=[
                ('cod_empregado', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('idade', models.IntegerField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contato', models.CharField(max_length=15, unique=True)),
                ('cargo', models.CharField(max_length=100)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Materiais',
            fields=[
                ('cod_item', models.AutoField(primary_key=True, serialize=False)),
                ('nome_item', models.CharField(max_length=100)),
                ('quantidade', models.IntegerField()),
                ('cod_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Solitacoes_de_compras',
            fields=[
                ('cod_solicitacao', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('data_solicitacao', models.DateField()),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Rejeitado', 'Rejeitado')], max_length=20)),
                ('cod_empregado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.empregado')),
                ('cod_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.materiais')),
            ],
        ),
        migrations.AddField(
            model_name='materiais',
            name='solicitacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.solitacoes_de_compras'),
        ),
    ]
