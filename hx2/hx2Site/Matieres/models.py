from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from functools import partial


#Foncion to rename file
def my_upload_to(instance, path):
    extension = path.split(".")[-1].strip()
    filename = instance.matiereLinked.__str__() + "_" + instance.typeDoc.__str__() +"_" + instance.theme + "_" + instance.name + "." + extension
    #print(filename)
    return os.path.join(filename)

fs = FileSystemStorage(location = 'media/fichiersdeposes')

# Create your models here

class AnneeArchivee(models.Model):
   date = models.CharField(max_length = 100, unique=True, null=False)

   def __str__(self):
        return str(self.date)

class MatiereScolaire(models.Model):
   #id = models.BigAutoField(primary_key=True, default="1")
   name = models.CharField(max_length = 100, null=False)
   annee = models.ForeignKey(AnneeArchivee, on_delete=models.CASCADE, null=False)
   description = models.TextField(null=True)

   def __str__(self):
        return self.annee.__str__() + "_" + self.name


class TypeDeFichier(models.Model):
        #id = models.BigAutoField(primary_key=True, default="1")
        name = models.CharField(max_length = 100, unique=True, null=False)

        def __str__(self):
                return self.name


class Fichiers(models.Model):
   matiereLinked = models.ForeignKey(MatiereScolaire, on_delete=models.CASCADE, null=False)
   typeDoc = models.ForeignKey(TypeDeFichier, on_delete=models.CASCADE, null=False)
   name = models.CharField(max_length = 100, null=False)
   theme = models.CharField(max_length = 100, null=False)
   file = models.FileField(storage=fs, upload_to =my_upload_to, null=False)

   def __str__(self):
        return self.matiereLinked.__str__() + "_" + self.typeDoc.name +"_" +  self.theme + "_" + self.name

