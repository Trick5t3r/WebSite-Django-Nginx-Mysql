from Matieres.models import AnneeArchivee
from django.urls import reverse
from django.shortcuts import redirect


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

class AnneeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # we ignore the urls of the administration in order to be able to create the first accounts otherwise nothing works 
        if request.path.startswith(reverse('admin:index')):
                return self.get_response(request)

          
        if request.path != reverse("logout") and request.user.is_authenticated and request.GET.get('setYear', '') != '' and request.session.get('currentYear', '') != request.GET.get('setYear', ''):
                yearsAvailable = []
                groupsAvailable = request.user.groups.order_by("-name")
                for groupA in groupsAvailable:
                        yearsAvailable.append(groupA.__str__())
                yearWanted = request.GET.get('setYear', '')
                try:
                      an = AnneeArchivee.objects.filter(date=yearWanted)
                except ValueError:
                      an = []
                if len(an) == 0:
                       return redirect(reverse("logout"))
                if yearWanted in yearsAvailable:
                         request.session['currentYear'] = yearWanted

        if request.path != reverse("logout") and request.user.is_authenticated and request.session.get('currentYear', '') == '':
                yearWanted = verifYear(request.user)
                if yearWanted:
                         request.session['currentYear'] = yearWanted
                else:
                         return redirect(reverse("logout"))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
