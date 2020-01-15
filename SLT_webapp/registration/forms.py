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


class ParentForm(forms.Form):
    chosen_son = forms.CharField(max_length=25)


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

        if commit:
            user.save()

        return user


class FriendForm(forms.Form):
    ACTIONS = (('Add', 'Add'), ('Remove', 'Remove'))
    new_friend = forms.CharField(max_length=25)
    action = forms.CharField(max_length=25, widget=forms.Select(choices=ACTIONS))


class MessageForm(forms.Form):
    receiver = forms.CharField(max_length=50, initial='user name')
    subject = forms.CharField(max_length=50, initial='message subject')
    body = forms.CharField(max_length=250)

class RankGameForm(forms.Form):
    RANK = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    rank = forms.IntegerField(widget=forms.Select(choices=RANK))


class GameForm(forms.Form):
    moves = forms.IntegerField()
    mistakes = forms.IntegerField()
