from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from fuelest.views import HomePageView, ProfileView, QuoteListView, SuccessView

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='fuelest/login.html')),
    path('index/', HomePageView.as_view(), name="login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit/', views.profile_model, name="editprof"),
    path('register/', views.register_model, name="register"),
    path('quotes/generate/', views.quote_model, name="quotegen"),
    path('quotes/success/', SuccessView.as_view(), name="quotesuccess"),
    path('quotes/history/', QuoteListView.as_view(), name="quotehist"),
]
