from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterModelForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


class LoginPage(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('education:index')

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(self.request, email=cd['email'], password=cd['password'])

        if user and user.is_active:
            login(self.request, user)
            return redirect('education:index')
        else:
            messages.error(self.request, 'Email yoki parol noto‘g‘ri yoki email tasdiqlanmagan.')
            return self.form_invalid(form)



    
def logout_page(request):
    logout(request)
    return redirect('education:index')


class RegisterPage(FormView):
    template_name = 'users/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('users:login_page')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')

User = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!') 