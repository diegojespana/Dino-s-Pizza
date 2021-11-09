from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from django.utils.translation import ugettext
from .models import Customer, Address
from django.core.exceptions import ValidationError


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Nombre Completo"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Número de Teléfono"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Dirección"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Instrucciones de Entrega"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Ciudad"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Código Postal"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nombre de Usuario', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Ingrese un nombre de Usuario', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Lo lamentamos, necesitas ingresar tu email'})
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, min_length=12)
    password2 = forms.CharField(
        label='Repite tu Contraseña', widget=forms.PasswordInput, min_length=12)

    # image = forms.ImageField(
    #    label='Ingrese una Imagen para su Usuario', help_text='Required', error_messages={
    #        'required': 'Lo lamentamos, necesitas ingresar tu imagen'
    #    }
    # )

    class Meta:
        model = Customer
        fields = ('user_name', 'email')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        if Customer.objects.filter(user_name=user_name).exists():
            raise forms.ValidationError(
                'Por favor utiliza otro nombre de usuario, este ya existe')
        return user_name

    def psw_validate(self):
        password = self.cleaned_data['password']
        if len(password) < 12:
            raise ValidationError(ugettext('La contraseña debe tener al menos 12 caracteres.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                ugettext('La contraseña debe contener al menos un dígito'))
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                ugettext('La contraseña debe contener al menos un caracter especial.'))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Por favor utiliza otro email, ya existe un usuario con este')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nombre de Usuario'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repite tu Contraseña'})
        # self.fields['image'].widget.attrs.update(
        #    {'class': 'form-control', 'placeholder': 'Repite tu Contraseña'})


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Desafortunadamente no pudimos encontrar ningun usuario con este email')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva Contraseña', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Nueva Contraseña', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repite tu Contraseña', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Nueva Contraseña', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Nombre de Usuario (No se puede modificar)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Nombre de Usuario', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Nombre de Usuario', 'id': 'form-firstname',
                   'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Primer Nombre', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Primer Nombre', 'id': 'form-lastname'}))

    class Meta:
        model = Customer
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
