# Generated by Django 4.0.2 on 2022-04-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='cancelado',
            field=models.BooleanField(default=False, verbose_name='Cancelado'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='data_horario',
            field=models.DateTimeField(verbose_name='Horário do agendamento'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='email_cliente',
            field=models.EmailField(max_length=254, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='nome_cliente',
            field=models.CharField(max_length=255, verbose_name='Nome do cliente'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='telefone_cliente',
            field=models.CharField(max_length=20, verbose_name='Telefone'),
        ),
    ]