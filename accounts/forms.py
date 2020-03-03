from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """Updated for customer user model"""
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'email', 'date_of_birth', 'address', 'city',
                  'country', 'post_code', )


class CustomUserChangeForm(UserChangeForm):
    """Updated for customer user model"""
    class Meta:
        model = get_user_model()
        fields = '__all__'
