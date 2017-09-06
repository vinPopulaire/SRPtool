from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate

from .forms import SignupForm


def home(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/home.html', context)


def terms(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/terms.html', context)


def about(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/about.html', context)


def delete(request):

    current_user = request.user

    if current_user.is_authenticated:
        current_user.delete()

    return redirect('home')


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'gui/signup.html', {'form': form})
