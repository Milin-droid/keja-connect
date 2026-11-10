from django.urls import path

from .views import KejaLoginView, KejaLogoutView, SignUpView, dashboard

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', KejaLoginView.as_view(), name='login'),
    path('logout/', KejaLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
