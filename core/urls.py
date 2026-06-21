from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("experience/", views.experience, name="experience"),
    path("case-studies/", views.case_study_list, name="case_study_list"),
    path("case-studies/<slug:slug>/", views.case_study_detail, name="case_study_detail"),
    path("contact/", views.contact, name="contact"),
]
