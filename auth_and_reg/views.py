from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from auth_and_reg.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserPasswordResetForm
from auth_and_reg.token import account_activation_token
from extension_users.models import User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password2'])
            new_user.is_active = False
            new_user.save()
            send_activate_email(get_current_site(request), new_user)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def send_activate_email(current_site, user):
    current_site = current_site
    mail_subject = 'Confirm registration'
    message = render_to_string('account_active_email.html', {
        'new_user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(subject=mail_subject, body=message, to=[to_email])
    email.send()


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_verify = True
        user.save()
        return render(request, 'account_active_email_done.html')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginUser(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('home')
    template_name = 'login.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        if 'data' in kwargs:
            form_user = kwargs['data']['username']
            if User.objects.filter(username=form_user).exists():
                user = User.objects.filter(username=form_user)
                if not user[0].is_active:
                    send_activate_email(get_current_site(self.request), user[0])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(requests):
    logout(requests)
    return redirect('home')


class PasswordResetUserView(PasswordResetView):
    form_class = CustomUserPasswordResetForm
    success_url = reverse_lazy('auth_and_reg:password_reset_done')
    email_template_name = 'password_reset_email.html',
    template_name = 'password_reset_form.html'


class PasswordResetUserConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('auth_and_reg:password_reset_complete')


class PasswordResetUserDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class PasswordResetUserCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
