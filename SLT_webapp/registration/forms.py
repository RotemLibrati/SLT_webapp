from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, Friend


class LoginForm(forms.Form):
    user_name = forms.CharField(initial='')
    password = forms.CharField(widget=forms.PasswordInput(), initial='')


class CardForm(forms.Form):
    word = forms.CharField()
    image = forms.ImageField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address', 'age', 'type')


class ParentForm(forms.ModelForm):
    chosen_son = forms.CharField(max_length=25)

    class Meta:
        model = UserProfile
        fields = ('son',)


class CompleteUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(CompleteUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        # user.userprofile.address = self.cleaned_data['address']
        # user.userprofile.age = self.cleaned_data['age']
        # user.userprofile.points = self.cleaned_data['points']

        if commit:
            user.save()

        return user


class FriendForm(forms.Form):
    ACTIONS = (('Add', 'Add'), ('Remove', 'Remove'))
    new_friend = forms.CharField(max_length=25)
    action = forms.CharField(max_length=25, widget=forms.Select(choices=ACTIONS))
