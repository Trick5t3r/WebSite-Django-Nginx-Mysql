import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hx2Site.settings")
django.setup()

from django.core.files import File
from Matieres.models import *

import sys

#walk_dir = sys.argv[1]
walk_dir = "/path/to/the/folder/to/siphon/"


print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    print('--\nroot = ' + root)
    for filename in files:
            file_path = os.path.join(root, filename)

            print('\t- file %s (full path: %s)' % (filename, file_path))
            main_Dir = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))
            first_Dir = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
            second_Dir = os.path.basename(os.path.dirname(file_path))
            print(main_Dir, first_Dir, second_Dir)

            annee = AnneeArchivee.objects.get(date=2021)
            matiere = MatiereScolaire.objects.get(name=main_Dir, annee=annee)
            type_fichier = TypeDeFichier.objects.get_or_create(name=first_Dir)[0]
            themeLink = second_Dir

            f = File(open(os.path.join(root, filename), 'rb'))

            changedName = os.path.splitext(filename)[0]

            #Normalization of the name in my case
            changedName = changedName .replace("ex", "Ex")
            changedName = changedName.replace("Exercice", "Ex")
            changedName = changedName.replace("x", "x ")
            changedName = changedName.replace("  ", " ")
            #

            Fichiers.objects.create(matiereLinked=matiere, typeDoc=type_fichier, name=changedName, theme=themeLink, file=f)

