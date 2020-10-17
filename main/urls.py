from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("timetable/",views.timetable,name="timetable"),
    path("timetable/states/",views.tablestatus,name="tablestatus"),
    path("lesson/create/",views.createlessonfield,name="createlessonfield"),
]