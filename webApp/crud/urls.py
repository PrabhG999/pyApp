# crud app endpoints
# import statements are important
from django.urls import path
from . import views

urlpatterns = [
    # This URL will match a GET or POST request without an ID.
    path('crud/', views.CrudViewset.as_view()),

    # This URL will match GET, PATCH, and DELETE requests with an ID.
    path('crud/<int:id>/', views.CrudViewset.as_view()),
]
