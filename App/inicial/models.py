from django.utils import timezone

from django.db import models

class servicios(models.Model):
    class Meta:
        db_table = 'servicios'
    cod_servicio = models.IntegerField(null=True, blank=True, verbose_name="Cod servicio", unique=True)
    descripcion = models.TextField(null=True, blank=True, max_length=150, verbose_name="descripcion")

class cargos(models.Model):
    class Meta:
        db_table = 'cargos'
    cod_cargo = models.IntegerField(null=True, blank=True, verbose_name="Cod cargo", unique=True)
    descripcion = models.TextField(null=True, blank=True, max_length=150, verbose_name="descripcion")

class derivacion(models.Model):
    class Meta:
        db_table = 'derivacion'
    cod_derivacion = models.IntegerField(null=True, blank=True, verbose_name="Cod derivacion")
    rut = models.CharField(null=True, blank=True, max_length=20, verbose_name="rut")
    nombre = models.TextField(null=True,blank=True, max_length=150,verbose_name="nombre")
    direccion = models.TextField(null=True, blank=True, max_length=200, verbose_name="direccion")
    telefono = models.TextField(null=True, blank=True, verbose_name="telefono")
    correo = models.TextField(null=True, blank=True, max_length=200, verbose_name="correo")
    fecha_derivacion = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="Fecha derivacion")
    derivador = models.TextField(null=True,blank=True, max_length=100,verbose_name="ejecutivo")
    derivado = models.BooleanField(default=True, verbose_name="Derivado")
    observacion = models.TextField(null=True,blank=True, max_length=160,verbose_name="Observacion")
    fecha_derivacion_nueva = models.DateTimeField(blank=True, null=True, verbose_name="Fecha derivacion anterior")
    nuevo_derivador = models.TextField(null=True, blank=True, max_length=100,verbose_name="Nuevo ejecutivo derivador")
    cantidad_derivacion = models.IntegerField(null=True, blank=True, verbose_name="cantidad derivaciones")
    correo_derivacion = models.TextField(null=True,blank=True, max_length=200,verbose_name="Correo ejecutivo enviado")
    correo_derivacion_nuevo = models.TextField(null=True, blank=True, max_length=200,verbose_name="Correo ejecutivo enviado")
    fecha_anulado = models.DateTimeField(blank=True, null=True, verbose_name="Fecha anulado")
    anulado = models.BooleanField(default=False, verbose_name="anulado")
    campania = models.ForeignKey('campana', on_delete=models.RESTRICT, null=True, blank=True, verbose_name="id", to_field="id")

class puntaje(models.Model):
    class Meta:
        db_table = 'puntaje'
    rut_ejecutivo = models.CharField(null=True, blank=True, max_length=20, verbose_name="rut")
    user_ejecutivo = models.TextField(null=True, blank=True, max_length=100, verbose_name="usuario del ejecutivo")
    n_personal = models.IntegerField(null=True, blank=True, verbose_name="n de personal")
    nombre_ejecutivo = models.TextField(null=True,blank=True, max_length=150,verbose_name="nombre ejecutivo")
    puntaje_periodo = models.IntegerField(null=True, blank=True, verbose_name="puntaje periodo")
    puntaje_acumulado_total = models.IntegerField(null=True, blank=True, verbose_name="puntaje total acumulado")
    fecha_inicio_camp = models.DateTimeField(blank=True, null=True, verbose_name="Fecha inicio")
    fecha_termino_camp = models.DateTimeField(blank=True, null=True, verbose_name="Fecha termino")
    fecha_reset = models.DateTimeField(blank=True, null=True,verbose_name="Fecha reset campaña")
    fecha_inicio_sistema = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de creacion sistema")
    fecha_movimiento = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="Fecha movimiento")
    fecha_anulado = models.DateTimeField(blank=True, null=True, verbose_name="Fecha anulado")
    anulado = models.BooleanField(default=False, verbose_name="anulado")
    campania_id = models.ForeignKey('campana', on_delete=models.RESTRICT, null=True, blank=True, verbose_name="id",to_field="id")
    cod_servicio = models.ForeignKey(servicios, on_delete=models.RESTRICT, null=True, blank=True, verbose_name="cod servicio",to_field="cod_servicio")
    cod_cargo = models.ForeignKey(cargos, on_delete=models.RESTRICT, null=True, blank=True,verbose_name="cod cargo", to_field="cod_cargo")

class correo(models.Model):
    class Meta:
        db_table = 'correo'
    rut = models.CharField(blank=True, null=True, max_length=11, verbose_name="RUT")
    nombre = models.TextField(blank=True, null=True, max_length=200, verbose_name="Nombre")
    correo = models.CharField(max_length=150, blank=False, null=False, verbose_name="Correo")
    valido = models.BooleanField(default=True, verbose_name="valido")
    actual = models.BooleanField(default=False, verbose_name="actual")


class premios(models.Model):
    class Meta:
        db_table = 'premios'
    id = models.AutoField(primary_key=True, verbose_name="ID")
    premio = models.TextField(blank=True, null=True, max_length=200, verbose_name="Premio")
    fecha = models.DateField(blank=True, null=True, verbose_name="Fecha")
    usuario = models.TextField(null=False, blank=False, max_length=100, verbose_name="Usuario")
    id_campana = models.ForeignKey('campana', on_delete=models.RESTRICT, null=True, blank=True, verbose_name="id", to_field="id")


class campana(models.Model):
    class Meta:
        db_table = 'campana'
    id = models.AutoField(primary_key=True, verbose_name="ID")
    nombre = models.TextField(blank=True, null=True, max_length=200, verbose_name="nombre")
    fecha_inicio = models.DateTimeField(blank=True, null=True, verbose_name="f_inicio")
    fecha_final = models.DateTimeField(blank=True, null=True, verbose_name="f_final")
    activo = models.BooleanField(default=True, blank=True, null=True, verbose_name="activo")
    sorteado = models.BooleanField(default=False, blank=True, null=True, verbose_name="sorteado")
    valida = models.BooleanField(default=True, verbose_name="valida")

class historial_puntaje(models.Model):
    class Meta:
        db_table = 'historial_puntaje'
    rut_ejecutivo = models.CharField(null=True, blank=True, max_length=20, verbose_name="rut")
    fecha_inicio_camp = models.DateTimeField(blank=True, null=True, verbose_name="Fecha inicio")
    fecha_termino_camp = models.DateTimeField(blank=True, null=True, verbose_name="Fecha termino")
    puntaje_periodo = models.IntegerField(null=True, blank=True, verbose_name="puntaje periodo")
    campania = models.ForeignKey('campana', on_delete=models.RESTRICT, null=True, blank=True, verbose_name="id", to_field="id")

class derivacion_rechazada(models.Model):
    class Meta:
        db_table = 'derivacion_rechazada'
    rut = models.CharField(null=True, blank=True, max_length=20, verbose_name="rut")
    fecha_rechazo = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="Fecha rechazo")
    ejecutivo = models.TextField(null=True,blank=True, max_length=100,verbose_name="ejecutivo")
    anulado = models.BooleanField(default=False, verbose_name="anulado")