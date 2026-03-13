from django.contrib import admin
from .models import Artiste, Disc, Piste, Label, Categorie

# Register your models here.

class DiscAdmin(admin.ModelAdmin):
    search_fields = ["nom_album", "auteurs__nom"]
    filter_horizontal = ('pistes',)
    list_display = ["nom_album", "get_auteurs", "categorie", "date_acquisition" ]

admin.site.register(Disc, DiscAdmin)
admin.site.register(Artiste)
admin.site.register(Piste)
admin.site.register(Label)
admin.site.register(Categorie)