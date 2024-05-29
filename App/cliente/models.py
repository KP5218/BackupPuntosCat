#Desarrollado por Manuel Godoy
from django.db import models

# Create your models here.
class region(models.Model):
    cod_region = models.CharField(blank=False, null=False, max_length=5, unique=True)
    nom_region = models.TextField(blank=False, null=False, max_length=100)

    def __str__(self):
        texto = "{} - {} "
        return texto.format(self.cod_region, self.nom_region)

class provincia(models.Model):
    cod_provincia = models.CharField(blank=False, null=False, max_length=5, unique=True)
    nom_provincia = models.TextField(blank=False, null=False, max_length=100)
    cod_region = models.CharField(blank=False, null=False, max_length=5)

    def __str__(self):
        texto = "{} - {} "
        return texto.format(self.cod_provincia, self.nom_provincia)


class comuna(models.Model):
    cod_comuna = models.CharField(blank=False, null=False, max_length=6, unique=True)
    nom_comuna = models.TextField(blank=False, null=False, max_length=100)
    cod_provincia = models.CharField(blank=False, null=False, max_length=5)

    def __str__(self):
        texto = "{} - {} "
        return texto.format(self.cod_comuna, self.nom_comuna)



class pais(models.Model):
    cod_pais = models.CharField(blank=False, null=False, max_length=5, unique=True)
    nom_pais = models.TextField(blank=False, null=False, max_length=100)
    abre_pais = models.CharField(blank=False, null=False, max_length=4)

    def __str__(self):
        texto = "{} - {} -{}"
        return texto.format(self.cod_pais, self.nom_pais, self.abre_pais)


class prevision(models.Model):
    cod_prevision = models.CharField(max_length=2, unique=True)
    prevision_nom = models.CharField(max_length=100)
    def __str__(self):
        return "{} - {}".format(self.cod_prevision, self.prevision_nom)


class estadocivil(models.Model):
    cod_estadocivil = models.CharField(max_length=2, unique=True)
    estadocivil = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.cod_estadocivil, self.estadocivil)


class sexo(models.Model):
    cod_sexo = models.CharField(blank=False, null=False, max_length=2, unique=True)
    letra_sexo = models.CharField(blank=False, null=False, max_length=2)
    nom_sexo = models.TextField(blank=False, null=False, max_length=100)

    def __str__(self):
        texto = "{} - {} - {}"
        return texto.format(self.cod_sexo, self.letra_sexo, self.nom_sexo)


class Basecliente(models.Model):
    id2cliente = models.IntegerField(blank=True, null=True, verbose_name="numero de presupuesto",unique=True)
    rut = models.CharField(blank=True, null=True, max_length=11, verbose_name="RUT", unique=True)
    pasaporte = models.CharField(max_length=100,blank=True, null=True, verbose_name="Pasaporte")
    nombre = models.TextField(blank=True, null=True, max_length=200, verbose_name="Nombres")
    nombresocial = models.TextField(blank=True, null=True, max_length=200, verbose_name="Nombre social")
    appaterno = models.TextField(blank=True, null=True, max_length=100, verbose_name="Apellido Paterno")
    apmaterno = models.TextField(blank=True, null=True, max_length=100, verbose_name="Apellido Materno")
    sexo = models.ForeignKey(sexo, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_sexo')
    fechanacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    nacionalidad = models.ForeignKey(pais, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_pais')
    estadocivil = models.ForeignKey(estadocivil, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Estado Civil", to_field='cod_estadocivil')
    direccion = models.TextField(blank=True, null=True, max_length=200)
    region = models.ForeignKey(region, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_region')
    provincia = models.ForeignKey(provincia, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_provincia')
    comuna = models.ForeignKey(comuna, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_comuna')
    ciudad = models.TextField(blank=True, null=True, max_length=150, verbose_name="Ciudad")
    fonomovil = models.TextField(blank=True, null=True, max_length=20, verbose_name="celular")
    fonofijo = models.TextField(blank=True, null=True, max_length=20, verbose_name="Telefono Fijo")
    email = models.TextField(blank=True, null=True, max_length=200)
    prevision = models.ForeignKey(prevision,on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_prevision')
    ppn = models.IntegerField(blank=True, null=True,unique=True)
    email_envio = models.TextField(blank=True, null=True, max_length=200)

    def id_rut(self):
        return "{} {}".format(self.id,self.rut)

    def nombre_completo(self):
        return "{} {} {}".format(self.nombre, self.appaterno, self.apmaterno)

    def __str__(self):
        return self.nombre_completo()