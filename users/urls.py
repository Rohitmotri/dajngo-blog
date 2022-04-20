from users import views
from django.urls import path

urlpatterns = [
    path("accounts/register",views.AuthorCreateView.as_view(),name = "account_register"),
    path("accounts/profile/",views.AuthorUpdateView.as_view(),name= "accounts_update"),
]

