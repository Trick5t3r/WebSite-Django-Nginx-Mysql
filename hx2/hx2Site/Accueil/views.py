# coding: utf8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Matieres.models import MatiereScolaire, AnneeArchivee
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# Create your views here.
def verifYear(user):
                try:
                      yearWanted = user.groups.order_by("-name")[0].name
                      an = AnneeArchivee.objects.filter(date=yearWanted)
                except ValueError:
                      an = []
                except IndexError:
                      an = []
                if len(an) == 0:
                      return False
                else:
                      return user.groups.order_by("-name")[0].name


@login_required
def mainPage(request):
        context = {}
        #setYear(request)
        an = AnneeArchivee.objects.filter(date=request.session.get('currentYear', ''))
        matieres = MatiereScolaire.objects.filter(annee = an[0])
        context['matieres'] = matieres
        return render(request, 'Accueil/templateMainAccueil.html', context)

def autentificationPage(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			print("auth")
			user = authenticate(request, username=form.cleaned_data['identifiant'], password=form.cleaned_data['password'])
			login(request, user)
			print("log")
			print("pass")
			yearWanted = verifYear(user)
			if yearWanted:
				request.session['currentYear'] = yearWanted
			else:
				return logout_view(request)
			print("pass2")
			request.session.modified = True
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			else:
				return redirect("mainPage")
	else:
		form = UserForm()
	return render(request, 'Accueil/templateLogin.html', {'form':form})

def logout_view(request):
	logout(request)
	return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required
def protectedFile_view(request, pathFile=""):
        isAuthorize = False
        print(pathFile)
        for group in list(request.user.groups.values_list('name',flat = True)):
             if pathFile.startswith(group):
                  isAuthorize = True
        if pathFile.startswith("permanent/"):
             isAuthorize = True
        if not isAuthorize:
             return HttpResponseForbidden()

        response = HttpResponse()
        url = request.path.replace("protected", "fichiersdeposes", 1)

        response['X-Accel-Redirect'] = url.encode('utf-8')
        response['Content-Type'] = ''

        return response


