from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme

from interactions.models import Enquiry
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get_success_url(self):
        next_url = self.request.POST.get('next', '')
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url
        return super().get_success_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class KejaLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class KejaLogoutView(LogoutView):
    pass


@login_required
def dashboard(request):
    if request.user.role in ['advertiser', 'both']:
        return redirect('listings:landlord-dashboard')

    enquiries = Enquiry.objects.filter(
        seeker=request.user
    ).select_related('property', 'property__county', 'property__town')
    return render(request, 'accounts/dashboard.html', {
        'enquiries': enquiries,
    })
