from django.shortcuts import render


# all static packages import below
from . import PAGE_MAPPER
# Create your views here.


def homepage(request):

    pageDictKey = 'homepage'

    return render(request, PAGE_MAPPER.pageDict[pageDictKey])
