from django.contrib.auth.models import User
from ..models import Profile


def get_profile():
    user = User.objects.create_user(
        username='user_test',
        email='user_test@test.com',
        password='password'
    )
    profile = Profile.objects.create(
        user=user,
        favorite_city='Paris'
    )
    return user, profile
