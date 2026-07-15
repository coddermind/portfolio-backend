from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import Profile, User


class ProfileAdminForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "vFileField"}),
    )

    class Meta:
        model = Profile
        fields = ("profile_picture",)

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data["first_name"]
            self.user.last_name = self.cleaned_data["last_name"]
            self.user.save(update_fields=["first_name", "last_name"])
        if commit:
            profile.save()
        return profile


class ProfilePasswordForm(PasswordChangeForm):
    pass
