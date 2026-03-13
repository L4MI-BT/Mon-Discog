from django.db import models
from django.utils import timezone

# Create your models here.
class Label(models.Model):
    nom = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom


class Artiste(models.Model):
    nom = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    label_apartenance = models.ForeignKey(
        Label,
        on_delete = models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nom


class Piste(models.Model):
    titre = models.CharField(max_length=255)
    duree = models.CharField(max_length=10)
    auteur = models.ForeignKey(Artiste, on_delete = models.CASCADE)
    compositeur = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.titre


# TODO Changer pour ne mettre qu'un seul auteur possible par disc
class CategorieEnum(models.TextChoices):
    SIZE45 = '45T', '45 tours'
    SIZE33 = '33T', '33 tours'
    SIZECD = 'CD', 'cd'

class Categorie(models.Model):
    categorie = models.CharField(
        max_length=3, choices=CategorieEnum.choices, default=CategorieEnum.SIZE45
    )

    def __str__(self):
        return self.categorie

class Genre(models.Model):
    genre = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.genre

# TODO ajouter le genre de chaque album
class Disc(models.Model):
    nom_album = models.CharField(max_length=255)
    jacket= models.ImageField(
        upload_to='collection/images/',
        blank=True,
        null=True
    )
    date_published = models.DateField("date de publication")
    date_acquisition = models.DateField("date d'achat", default=timezone.now)
    prix = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )
    auteurs = models.ManyToManyField(Artiste)
    pistes = models.ManyToManyField(Piste)
    categorie = models.ForeignKey(Categorie, on_delete = models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete= models.CASCADE, blank=True, null=True)

    def get_auteurs(self):
        return "\n".join([p.nom for p in self.auteurs.all()])
    

    def __str__(self):
        return self.nom_album


