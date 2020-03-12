from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from .forms import ProfileForm

# Create your views here.


class ProfilePageView(LoginRequiredMixin, UpdateView):
    """User profile modification view"""
    form_class = ProfileForm
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'There was a problem with the data you inputted - '
            'please see the error messages below.')
        return super().form_invalid(form)
