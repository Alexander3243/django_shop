from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, forms
from extension_users.models import User
from django.contrib.auth.hashers import check_password


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PasswordResetFormUser(PasswordResetForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CustomPasswordResetUserConfirmForm(SetPasswordForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'city', 'address', 'phone_number', 'password1', 'password2')


class CustomUserCreationForm(RegisterUserForm):

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exist")
        return email


class CustomUserLoginForm(LoginUserForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(_("Your account has expired. \Please click the renew subscription link below"),
                                        code='inactive', )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError("This user doesn't exist")

    def clean_password(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username'].lower()
            password = self.cleaned_data['password']
            user = User.objects.filter(username=username)
            if check_password(password, user[0].password):
                if not user[0].is_active:
                    raise forms.ValidationError(
                        ("Уour account has not been activated. We sent link to {} for activate your account".format(
                            user[0].email)),
                        code='inactive', )
                return password
            else:
                raise forms.ValidationError("Wrong password")


class CustomUserPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist")
        return email
