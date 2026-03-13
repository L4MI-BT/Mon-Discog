from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from datetime import date
from django.conf import settings
import discogs_client

from .models import Label, Artiste, Piste, Categorie, Disc, Genre, CategorieEnum
# Create your views here.
class IndexView(generic.ListView):
    model = Disc
    template_name = "collection/index.html"
    context_object_name = "albums"

class AddView(generic.TemplateView):
    template_name = "collection/add.html"

    def post(self, request):
        barcode = request.POST.get("code")

        d = discogs_client.Client('my_user_agent/1.0', user_token=settings.DISCOGS_TOKEN)
        results = d.search(barcode=barcode, type='release')

        if results.count == 0:
            return render(request, "collection/add.html", {"error": "Aucun disque trouvé."})

        release = results[0]
        print(release)
        # --- Label ---
        label = None
        if release.labels:
            label, _ = Label.objects.get_or_create(nom=release.labels[0].name)

        # --- Artistes ---
        artistes = []
        for artist in release.artists:
            artiste, _ = Artiste.objects.get_or_create(
                nom=artist.name,
                defaults={"label_apartenance": label}
            )
            artistes.append(artiste)

        artiste_principal = artistes[0] if artistes else None

        # --- Genre ---
        genre = None
        if release.genres:
            genre, _ = Genre.objects.get_or_create(genre=release.genres[0])

        # --- Catégorie (basée sur le format Discogs) ---
        categorie = None
        formats = [f.get("name", "") for f in release.formats] if release.formats else []
        if "CD" in formats:
            cat_value = CategorieEnum.SIZECD
        elif any("12" in f for f in formats):
            cat_value = CategorieEnum.SIZE33
        else:
            cat_value = CategorieEnum.SIZE45

        categorie, _ = Categorie.objects.get_or_create(categorie=cat_value)

        # --- Disc ---
        disc, created = Disc.objects.get_or_create(
            nom_album=release.title,
            defaults={
                "date_published": date(release.year, 1, 1) if release.year else date.today(),
                "genre": genre,
                "categorie": categorie,
            }
        )

        if created:
            for artiste in artistes:
                disc.auteurs.add(artiste)

            # --- Pistes ---
            for track in release.tracklist:
                if not artiste_principal:
                    continue
                piste, _ = Piste.objects.get_or_create(
                    titre=track.title,
                    auteur=artiste_principal,
                    defaults={"duree": track.duration or ""}
                )
                disc.pistes.add(piste)

        return redirect("/add")