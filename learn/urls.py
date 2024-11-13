from django.urls import path

from .views import views, auth, courses, ml
from .views.__init__ import execute_code

urlpatterns = [
    # Authentication paths
    path('login/', auth.login, name='login'),
    path('register/', auth.register, name='register'),
    path('logout/', auth.logout, name='logout'),

    # Home and informational pages
    path('', views.index, name='index'),
    path('features', views.features, name='features'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('hackathon', views.hackathon, name='hackathon'),
    path('game', views.game, name='game'),
    path('perks', views.perks, name='perks'),

    # Profile and setup paths
    path('profile/', views.profile, name='profile'),
    path('setup', views.setup, name='setup'),

    # Course-related paths
    path('courses/<str:lesson>', courses.courses, name='courses'),

    # Exam and reports
    path('exam', ml.exam, name='exam'),
    path('report', ml.report, name='report'),

    # Compiler and analysis paths
    path('coding', views.compiler, name='coding'),
    path('execute/', execute_code, name='execute_code'),
]
