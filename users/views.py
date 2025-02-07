from django.shortcuts import render, redirect
from django.views import  View
from .forms import UserRegisterForm

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')
        # If form is not valid, re-render the form with errors
        return render(request, 'users/register.html', {'form': form})
    
def toggle_theme(request):
    """Toggle the theme between light and dark, storing it in the session."""
    current_theme = request.session.get('theme', 'dark')
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    request.session['theme'] = new_theme
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page
