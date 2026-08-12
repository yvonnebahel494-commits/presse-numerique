from django.db import models
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
import secrets
from django.utils import timezone
import string
from django.contrib.auth.hashers import make_password

class Maison(models.Model):
    nom_maison = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    lieu = models.CharField(max_length=200)
    identifiant = models.CharField(max_length=11, unique=True, editable=False)
    email_m = models.EmailField(unique=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_maison

    def save(self, *args, **kwargs):
        # Générer un identifiant uniquement pour les nouveaux objets
        if not self.identifiant:
            self.identifiant = self.generer_identifiant_unique()
        super().save(*args, **kwargs)

    def generer_identifiant_unique(self):
        # Générer un identifiant alphanumérique de 11 caractères
        alphabet = string.ascii_letters + string.digits
        while True:
            identifiant = ''.join(secrets.choice(alphabet) for _ in range(11))
            # Vérifier que l'identifiant n'existe pas déjà
            if not Maison.objects.filter(identifiant=identifiant).exists():
                return identifiant
            




class Editeur(models.Model):

    maison = models.ForeignKey(
        Maison,
        on_delete=models.CASCADE,
        related_name="editeurs"
    )

    nom = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)

    telephone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=255
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )


    def save(self, *args, **kwargs):

        # Crypter le mot de passe avant sauvegarde
        if not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.nom} {self.prenom}"



class Article(models.Model):

    TYPE_CHOICES = [
        ('actualite', 'Actualité'),
        ('politique', 'Politique'),
        ('economie', 'Économie'),
        ('sport', 'Sport'),
        ('culture', 'Culture'),
        ('technologie', 'Technologie'),
        ('societe', 'Société'),
        ('autre', 'Autre'),
    ]

    maison = models.ForeignKey(
        Maison,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    editeur = models.ForeignKey(
        Editeur,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    titre = models.CharField(max_length=200)

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='articles/images/',
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to='articles/pdf/',
        blank=True,
        null=True
    )

    date_publication = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.titre