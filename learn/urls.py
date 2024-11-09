from django.urls import path

from .views import views, auth, courses

urlpatterns = [
    path('login/', auth.login, name='login'),
    path('register/', auth.register, name='register'),

    path('setup', views.setup, name='setup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth.logout, name='logout'),

    path('', views.index, name='index'),
    path('courses/<str:lesson>', courses.courses, name='courses'),
    path('courses/<str:lesson>/<str:id>', courses.courses, name='courses'),
    path('process-frame/', views.process_frame, name='process_frame'),
    path('analysis', views.analysis, name='analysis')

]
