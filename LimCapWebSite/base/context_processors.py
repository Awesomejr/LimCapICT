def user_avatar(request):
    return {
        'user_avatar': request.user.avatar.url if request.user.is_authenticated else None
    }