from .views import get_user_role, get_user_role_badge_class

def user_role_context(request):
    """
    Context processor to add user role information to all templates
    """
    if request.user.is_authenticated:
        return {
            'user_role': get_user_role(request.user),
            'role_badge_class': get_user_role_badge_class(request.user),
        }
    return {
        'user_role': 'Guest',
        'role_badge_class': 'bg-secondary',
    }
