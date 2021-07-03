from django.urls import path

from . import views

urlpatterns = [
	path('<str:matieresScolaire>/<str:typeSelected>', views.getMatiereType, name='matieresScolaireType'),
    path('<str:matieresScolaire>/', views.getMatiere, name='matieresScolaire'),
]
