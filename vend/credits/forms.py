from django import forms
from django.contrib.auth.models import User
from credits.models import UserProfile, Purchase, Design, Transfer, Submission, Job, Accept

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('credits','user')
class SpendForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Purchase.objects.all())
    class Meta:
        model = Purchase
	fields = ('name',)
class StlForm(forms.ModelForm):
    class Meta:
        model = Design
        exclude = ('owner','cost','name','area','volume')
class transForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ('cost', 'recipient')

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title','desc','cost')
        exclude = ('owner','name')
class SubmissionForm(forms.ModelForm):
    job = forms.ModelChoiceField(queryset=Job.objects.all(),widget=forms.HiddenInput())
    class Meta:
        model = Submission
        fields = ('submission','job',)
        exclude = ('submitter', 'name',)
class AcceptForm(forms.ModelForm):
    class Meta:
        model = Accept
        fields = ('submission','job',)
