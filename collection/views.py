from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Label, Artiste, Piste, Categorie, Disc
# Create your views here.
class IndexView(generic.ListView):
    model = Disc
    template_name = "collection/index.html"
    context_object_name = "albums"