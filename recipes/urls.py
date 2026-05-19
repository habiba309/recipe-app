from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ──
    path('',        views.signin_view,  name='signin'),
    path('signup/', views.signup_view,  name='signup'),
    path('logout/', views.logout_view,  name='logout'),

    # ── User pages ──
    path('home/',                      views.home_view,            name='home'),
    path('recipes/',                   views.recipes_list_view,    name='recipes_list'),
    path('recipes/<int:pk>/',          views.recipe_detail_view,   name='recipe_detail'),
    path('recipes/<int:pk>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),


    # ── Admin dashboard ──
    path('favorites/',                 views.favorites_view,       name='favorites'),
    path('admin_home/',                 views.admin_home_view,       name='admin_home'),
    path('dashboard/',                 views.dashboard_view,       name='dashboard'),

    path('dashboard/add/',             views.add_recipe_view,      name='add_recipe'),
    path('dashboard/edit/<int:pk>/',   views.edit_recipe_view,     name='edit_recipe'),

    path('dashboard/delete/<int:pk>/', views.delete_recipe_view,   name='delete_recipe'),



]
