from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('dashboard_faves/<int:book_id>/<int:user_id>', views.  dashboard_faves),
    path('go_back', views.go_back),
    path('logout', views.logout),
    path('add_a_book', views.add_a_book),
    path('books/<int:book_id>', views.show_book),
    path('update_a_book/<int:book_id>', views.update_book),
    path('delete/<int:book_id>', views.delete),
    path('add_to_favorites/<int:book_id>/<int:user_id>', views.add_to_favorites),
    path('unfavorite/<int:book_id>/<int:user_id>', views.unfavorite),
]