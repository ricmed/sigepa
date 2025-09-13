from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    """
    Formulário personalizado para criação de usuários.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    telefone = forms.CharField(max_length=20, required=False)
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'telefone', 'data_nascimento', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.telefone = self.cleaned_data['telefone']
        user.data_nascimento = self.cleaned_data['data_nascimento']
        if commit:
            user.save()
        return user
