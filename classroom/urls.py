from django.urls import path
from . import views

urlpatterns = [
    #rest api
    path('all-joinclass/',views.allJoinclass,name='all-joinclass'),
    path('all-ownclass/',views.allOwnclass,name='all-ownclass')
]