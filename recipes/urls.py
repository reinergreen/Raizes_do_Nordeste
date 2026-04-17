from django.urls import path

from recipes.views import cliente, home, my_view

urlpatterns = [
    path('', home),
    path('sobre/', my_view),
    path('cliente/', cliente),
]
