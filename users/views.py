from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from multiselectfield import MultiSelectFormField


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileRegisterForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Gender: ',choices=Profile.gender_choices, widget=forms.RadioSelect())
    intrests = MultiSelectFormField(label = 'Intrests: ', choices=Profile.intrests_choices)
    boolean = forms.BooleanField(widget=forms.CheckboxInput, required=False, initial=True)
    
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'country', 'intrests', 'float', 'boolean']
        exclude = ('user',)

    def clean_intrests(self):
        intrests = self.cleaned_data['intrests']
        if not intrests:
            raise forms.ValidationError("...")

        if len(intrests) > 4:
            raise forms.ValidationError("...")

        return intrests


class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Gender: ',choices=Profile.gender_choices, widget=forms.RadioSelect())
    intrests = MultiSelectFormField(label = 'Intrests: ', choices=Profile.intrests_choices)
    boolean = forms.BooleanField(widget=forms.CheckboxInput, required=False, initial=True)
    
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'country', 'intrests', 'float', 'boolean']

    def clean_intrests(self):
        intrests = self.cleaned_data['intrests']
        if not intrests:
            raise forms.ValidationError("...")

        if len(intrests) > 4:
            raise forms.ValidationError("...")

        return intrests

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user.set_password(u_form.cleaned_data.get('password1'))
            p_form = ProfileRegisterForm(request.POST, request.FILES, instance=user.profile)
            if p_form.is_valid():
                p_form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
