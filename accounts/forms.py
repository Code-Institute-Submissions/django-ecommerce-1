from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
# from allauth.account.forms import SignupForm


class CustomUserCreationForm(UserCreationForm):
    """Updated for customer user model"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name',
                  'last_name', 'date_of_birth', 'address', 'city',
                  'country', 'post_code', 'username')


class CustomUserChangeForm(UserChangeForm):
    """Updated for customer user model"""
    class Meta:
        model = get_user_model()
        fields = '__all__'


class CustomSignupForm(forms.Form):
    """Override the default allauth signup form"""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=100)
    post_code = forms.CharField(max_length=30)
    date_of_birth = forms.DateField()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.city = self.cleaned_data['city']
        user.country = self.cleaned_data['country']
        user.post_code = self.cleaned_data['post_code']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'date_of_birth',
                  'address', 'city', 'country', 'post_code')
