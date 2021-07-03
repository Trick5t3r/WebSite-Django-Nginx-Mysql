from django.shortcuts import render
from django.shortcuts import redirect
from .models import MatiereScolaire, Fichiers, TypeDeFichier, AnneeArchivee
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def getMatiere(request, matieresScolaire=None):
	if matieresScolaire == None:
		return redirect("mainPage")
	an = AnneeArchivee.objects.filter(date=request.session.get('currentYear', ''))
	matiere_correspondante = MatiereScolaire.objects.filter(name=matieresScolaire, annee=an[0])
	if len(matiere_correspondante) == 0:
		return redirect("mainPage")

	context = {}
	context['matiere_correspondante'] = matiere_correspondante[0]
	list_type = TypeDeFichier.objects.all()
	list_type_full = []
	for un_type in list_type:
		if Fichiers.objects.filter(matiereLinked=matiere_correspondante[0], typeDoc=un_type): #Verifie que le dossiers contient des elements
			list_type_full.append(un_type)
	context["list_type"] = list_type_full
	return render(request, 'Matieres/templateMatiere.html', context)

@login_required
def getMatiereType(request,  matieresScolaire=None, typeSelected=None):
	if matieresScolaire == None:
		return redirect("mainPage")
	an = AnneeArchivee.objects.filter(date=request.session.get('currentYear', ''))
	matiere_correspondante = MatiereScolaire.objects.filter(name=matieresScolaire, annee=an[0])
	if len(matiere_correspondante) == 0:
		return redirect("mainPage")

	context = {}
	context['matiere_correspondante'] = matiere_correspondante[0]
	list_type = TypeDeFichier.objects.all()
	list_type_name = [instanceType.name for instanceType in list_type]

	if typeSelected not in list_type_name:
		return redirect("matieresScolaire", matieresScolaire = matieresScolaire)

	typeDuFichier = TypeDeFichier.objects.filter(name=typeSelected)[0]
	context['docs'] = Fichiers.objects.filter(matiereLinked=matiere_correspondante[0], typeDoc=typeDuFichier)
	context['typeSelected'] = typeDuFichier

	return render(request, 'Matieres/templateCours.html', context)


