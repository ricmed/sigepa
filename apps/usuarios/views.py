from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import UsuarioCreationForm


def home(request):
    """
    View para a página inicial.
    """
    return render(request, 'usuarios/home.html')


def register(request):
    """
    View para registro de novos usuários.
    """
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            login(request, user)
            return redirect('usuarios:home')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    View personalizada para login com redirecionamento.
    """
    template_name = 'usuarios/login.html'
    form_class = AuthenticationForm
    
    def get_success_url(self):
        """Redireciona para a página inicial após login bem-sucedido."""
        return reverse_lazy('usuarios:home')
    
    def form_valid(self, form):
        """Override para adicionar mensagem de sucesso."""
        messages.success(self.request, f'Bem-vindo, {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)


@login_required
def profile(request):
    """
    View para o perfil do usuário logado.
    """
    return render(request, 'usuarios/profile.html', {'user': request.user})
