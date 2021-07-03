from Matieres.models import AnneeArchivee

def displayYearAvailable(request):
	if request.user.is_authenticated:
		yearsAvailable = []
		groupsAvailable = request.user.groups.order_by("-name")
		for groupA in groupsAvailable:
			yearsAvailable += list(AnneeArchivee.objects.filter(date=groupA.name))#.values_list('date',flat = True))
	else:
		yearsAvailable = AnneeArchivee.objects.all()
	return {"yearsAvailable":yearsAvailable}

