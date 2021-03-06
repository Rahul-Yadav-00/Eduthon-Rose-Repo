from django.urls import path
from . import views

urlpatterns = [
    path('joincls/',views.joinClass,name='joincls'),
    path('createcls/',views.createClass,name='createcls'),
    path('classdetail/<slug:clscode>/',views.classDetails,name='classdetail'),
    path('createtest/<slug:clscode>/',views.createTest,name='createtest'),
    path('attempttest/<slug:testcode>/',views.attemptTest,name='attempttest'),

    #rest api
    path('all-joinclass/',views.allJoinclass,name='all-joinclass'),
    path('all-ownclass/',views.allOwnclass,name='all-ownclass')
]