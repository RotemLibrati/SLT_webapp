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
    set = User.objects.all()
    CHOICES=list(map(lambda x: (str(x.username), str(x.username)) ,set))
    chosen_son = forms.CharField(label = "choose a sun", widget=forms.Select(choices=CHOICES))




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

class ReportUserForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    reason = forms.CharField(max_length=100, widget=forms.Textarea)

class GameForm(forms.Form):
    moves = forms.IntegerField()
    mistakes = forms.IntegerField()

class ChooseLevelSon(forms.Form):
    LEVEL = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    level = forms.IntegerField(widget=forms.Select(choices=LEVEL))

class InviteFriend(forms.ModelForm):

    class Meta:
        model = Friend
        fields = ('users',)