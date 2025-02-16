# Generated by Django 4.2.13 on 2025-01-13 21:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='campana',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(blank=True, max_length=200, null=True, verbose_name='nombre')),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True, verbose_name='f_inicio')),
                ('fecha_final', models.DateTimeField(blank=True, null=True, verbose_name='f_final')),
                ('activo', models.BooleanField(blank=True, default=True, null=True, verbose_name='activo')),
                ('sorteado', models.BooleanField(blank=True, default=False, null=True, verbose_name='sorteado')),
                ('valida', models.BooleanField(default=True, verbose_name='valida')),
            ],
            options={
                'db_table': 'campana',
            },
        ),
        migrations.CreateModel(
            name='cargos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_cargo', models.IntegerField(blank=True, null=True, unique=True, verbose_name='Cod cargo')),
                ('descripcion', models.TextField(blank=True, max_length=150, null=True, verbose_name='descripcion')),
            ],
            options={
                'db_table': 'cargos',
            },
        ),
        migrations.CreateModel(
            name='correo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(blank=True, max_length=11, null=True, verbose_name='RUT')),
                ('nombre', models.TextField(blank=True, max_length=200, null=True, verbose_name='Nombre')),
                ('correo', models.CharField(max_length=150, verbose_name='Correo')),
                ('valido', models.BooleanField(default=True, verbose_name='valido')),
                ('actual', models.BooleanField(default=False, verbose_name='actual')),
            ],
            options={
                'db_table': 'correo',
            },
        ),
        migrations.CreateModel(
            name='derivacion_rechazada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(blank=True, max_length=20, null=True, verbose_name='rut')),
                ('fecha_rechazo', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha rechazo')),
                ('ejecutivo', models.TextField(blank=True, max_length=100, null=True, verbose_name='ejecutivo')),
                ('anulado', models.BooleanField(default=False, verbose_name='anulado')),
            ],
            options={
                'db_table': 'derivacion_rechazada',
            },
        ),
        migrations.CreateModel(
            name='servicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_servicio', models.IntegerField(blank=True, null=True, unique=True, verbose_name='Cod servicio')),
                ('descripcion', models.TextField(blank=True, max_length=150, null=True, verbose_name='descripcion')),
            ],
            options={
                'db_table': 'servicios',
            },
        ),
        migrations.CreateModel(
            name='puntaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_ejecutivo', models.CharField(blank=True, max_length=20, null=True, verbose_name='rut')),
                ('user_ejecutivo', models.TextField(blank=True, max_length=100, null=True, verbose_name='usuario del ejecutivo')),
                ('n_personal', models.IntegerField(blank=True, null=True, verbose_name='n de personal')),
                ('nombre_ejecutivo', models.TextField(blank=True, max_length=150, null=True, verbose_name='nombre ejecutivo')),
                ('puntaje_periodo', models.IntegerField(blank=True, null=True, verbose_name='puntaje periodo')),
                ('puntaje_acumulado_total', models.IntegerField(blank=True, null=True, verbose_name='puntaje total acumulado')),
                ('fecha_inicio_camp', models.DateTimeField(blank=True, null=True, verbose_name='Fecha inicio')),
                ('fecha_termino_camp', models.DateTimeField(blank=True, null=True, verbose_name='Fecha termino')),
                ('fecha_reset', models.DateTimeField(blank=True, null=True, verbose_name='Fecha reset campaña')),
                ('fecha_inicio_sistema', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de creacion sistema')),
                ('fecha_movimiento', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha movimiento')),
                ('fecha_anulado', models.DateTimeField(blank=True, null=True, verbose_name='Fecha anulado')),
                ('anulado', models.BooleanField(default=False, verbose_name='anulado')),
                ('campania_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='inicial.campana', verbose_name='id')),
                ('cod_cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='inicial.cargos', to_field='cod_cargo', verbose_name='cod cargo')),
                ('cod_servicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='inicial.servicios', to_field='cod_servicio', verbose_name='cod servicio')),
            ],
            options={
                'db_table': 'puntaje',
            },
        ),
        migrations.CreateModel(
            name='premios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('premio', models.TextField(blank=True, max_length=200, null=True, verbose_name='Premio')),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('usuario', models.TextField(max_length=100, verbose_name='Usuario')),
                ('id_campana', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='inicial.campana', verbose_name='id')),
            ],
            options={
                'db_table': 'premios',
            },
        ),
        migrations.CreateModel(
            name='historial_puntaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_ejecutivo', models.CharField(blank=True, max_length=20, null=True, verbose_name='rut')),
                ('fecha_inicio_camp', models.DateTimeField(blank=True, null=True, verbose_name='Fecha inicio')),
                ('fecha_termino_camp', models.DateTimeField(blank=True, null=True, verbose_name='Fecha termino')),
                ('puntaje_periodo', models.IntegerField(blank=True, null=True, verbose_name='puntaje periodo')),
                ('campania', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='inicial.campana', verbose_name='id')),
            ],
            options={
                'db_table': 'historial_puntaje',
            },
        ),
        migrations.CreateModel(
            name='derivacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_derivacion', models.IntegerField(blank=True, null=True, verbose_name='Cod derivacion')),
                ('rut', models.CharField(blank=True, max_length=20, null=True, verbose_name='rut')),
                ('nombre', models.TextField(blank=True, max_length=150, null=True, verbose_name='nombre')),
                ('direccion', models.TextField(blank=True, max_length=200, null=True, verbose_name='direccion')),
                ('telefono', models.TextField(blank=True, null=True, verbose_name='telefono')),
                ('correo', models.TextField(blank=True, max_length=200, null=True, verbose_name='correo')),
                ('fecha_derivacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha derivacion')),
                ('derivador', models.TextField(blank=True, max_length=100, null=True, verbose_name='ejecutivo')),
                ('derivado', models.BooleanField(default=True, verbose_name='Derivado')),
                ('observacion', models.TextField(blank=True, max_length=160, null=True, verbose_name='Observacion')),
                ('fecha_derivacion_nueva', models.DateTimeField(blank=True, null=True, verbose_name='Fecha derivacion anterior')),
                ('nuevo_derivador', models.TextField(blank=True, max_length=100, null=True, verbose_name='Nuevo ejecutivo derivador')),
                ('cantidad_derivacion', models.IntegerField(blank=True, null=True, verbose_name='cantidad derivaciones')),
                ('correo_derivacion', models.TextField(blank=True, max_length=200, null=True, verbose_name='Correo ejecutivo enviado')),
                ('correo_derivacion_nuevo', models.TextField(blank=True, max_length=200, null=True, verbose_name='Correo ejecutivo enviado')),
                ('fecha_anulado', models.DateTimeField(blank=True, null=True, verbose_name='Fecha anulado')),
                ('anulado', models.BooleanField(default=False, verbose_name='anulado')),
                ('campania', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='inicial.campana', verbose_name='id')),
            ],
            options={
                'db_table': 'derivacion',
            },
        ),
    ]
