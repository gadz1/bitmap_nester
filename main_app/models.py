from django.db import models
# Create your models here.
class nesters(models.Model):
    name=models.CharField(max_length=100)
    mail=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class history_m(models.Model):
    nester=models.ForeignKey(nesters,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    result = models.ImageField(null=True, blank=True)

class Pre_Input(models.Model):
    input_image = models.ImageField(null=True, blank=True)

class SVGFile(models.Model):
    svg_file = models.FileField(upload_to='svg_files/')

class new_in(models.Model):
    input_image = models.ImageField(null=True, blank=True)