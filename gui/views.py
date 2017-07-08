from django.http import HttpResponse
from django.template import loader


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