from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import SignupForm


def home(request, *args, **kwargs):

    template = loader.get_template('gui/home.html')
    context = {}

    return HttpResponse(template.render(context, request))


def terms(request, *args, **kwargs):

    template = loader.get_template('gui/terms.html')
    context = {}

    return HttpResponse(template.render(context, request))


def about(request, *args, **kwargs):

    template = loader.get_template('gui/about.html')
    context = {}

    return HttpResponse(template.render(context, request))


# def signup(request, *args, **kwargs):
#
#     template = loader.get_template('gui/signup.html')
#     context = {}
#
#     return HttpResponse(template.render(context, request))


def signup(request):
    form = SignupForm()

    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    pass1 = request.POST.get('pass1', '')
    pass2 = request.POST.get('pass2', '')

    # Do some validations here

    # user = User.objects.create_user(name, email, pass2)
    # if user:
    #     user.save()

    return render(request, 'gui/signup.html', {'form': form})
