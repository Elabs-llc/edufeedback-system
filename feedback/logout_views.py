from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

@csrf_protect
@require_http_methods(["POST"])
@login_required
def custom_logout_view(request):
    """Custom logout view with proper CSRF handling"""
    user_name = request.user.get_full_name() or request.user.username
    logout(request)
    messages.success(request, f'Successfully logged out. See you soon, {user_name}!')
    return redirect('login')

@csrf_protect  
@require_http_methods(["GET", "POST"])
def safe_logout_view(request):
    """Safe logout view that handles both GET and POST"""
    if request.method == 'POST':
        user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else 'User'
        logout(request)
        messages.success(request, f'Successfully logged out. See you soon, {user_name}!')
        return redirect('login')
    else:
        # For GET requests, show a logout confirmation page
        return render(request, 'registration/logout_confirm.html')
