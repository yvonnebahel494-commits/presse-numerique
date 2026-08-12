from urllib import request
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Editeur, Maison,Article
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    return render(request,'index.html')

def login_view(request):
    return render(request,'login_form.html')

def editeur_form(request):
    return render(request,'editeur_form.html')

def maison_edition_form(request):
    return render(request,'maison_edition_form.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Editeur


def dashboard_form(request):

    # Vérifier si l'utilisateur est connecté
    if "role" not in request.session:

        messages.error(
            request,
            "Vous devez être connecté pour accéder à cette page."
        )

        return redirect("login")


    # Vérifier que c'est bien un éditeur
    if request.session.get("role") != "editeur":

        messages.error(
            request,
            "Accès refusé : cette page est réservée aux éditeurs."
        )

        return redirect("login")


    editeur_id = request.session.get("editeur_id")

    try:

        editeur = Editeur.objects.get(
            id=editeur_id
        )

    except Editeur.DoesNotExist:

        request.session.flush()

        messages.error(
            request,
            "Votre session est invalide. Veuillez vous reconnecter."
        )

        return redirect("login")


    articles = Article.objects.filter(
        maison=editeur.maison
    ).order_by("-date_publication")


    return render(
        request,
        "dashboard.html",
        {
            "editeur": editeur,
            "maison": editeur.maison,
            "articles": articles,
        }
    )

def creer_maison(request):

    if request.method == "POST":

        nom = request.POST.get("nom")
        ville = request.POST.get("ville")
        lieu = request.POST.get("lieu")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        logo = request.FILES.get("logo")

        maison = Maison.objects.create(
            nom_maison=nom,
            ville=ville,
            lieu=lieu,
            tel=telephone,
            email_m=email,
            logo=logo
        )

        sujet = "Bienvenue chez True Site Technology"

        message = f"""
Bonjour,

Votre maison d'édition a été enregistrée avec succès.

Nom : {maison.nom_maison}

Votre identifiant unique est :

{maison.identifiant}

Conservez cet identifiant, il vous sera demandé lors de vos prochaines connexions.

Merci.
"""

        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [maison.email_m],
            fail_silently=False,
        )

        # Message de succès
        messages.success(
            request,
            f"La maison d'édition '{maison.nom_maison}' a été créée avec succès."
        )

        return redirect("maison_edition")

    return render(request, "maison_edition_form.html")


def creer_editeur(request):

    if request.method == "POST":

        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        identm = request.POST.get("identm")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        # Vérifier si la maison existe
        try:
            maison = Maison.objects.get(
                identifiant=identm
            )

        except Maison.DoesNotExist:

            messages.error(
                request,
                "Erreur : aucune maison d'édition trouvée avec cet identifiant."
            )

            return redirect("creer_editeur")


        # Vérifier si email déjà utilisé

        if Editeur.objects.filter(email=email).exists():

            messages.error(
                request,
                "Erreur : cette adresse email est déjà utilisée par un éditeur."
            )

            return redirect("creer_editeur")


        # Vérifier les mots de passe

        if password != confirm_password:

            messages.error(
                request,
                "Erreur : les deux mots de passe ne correspondent pas."
            )

            return redirect("creer_editeur")



        # Création de l'éditeur

        editeur = Editeur.objects.create(

            maison=maison,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            email=email,
            password=password

        )


        messages.success(
            request,
            f"L'éditeur {nom} {prenom} a été créé avec succès."
        )


        return redirect("editeur")



    return render(
        request,
        "editeur_form.html"
    )

def login_editeur(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")


        # Vérifier si l'éditeur existe

        try:

            editeur = Editeur.objects.get(
                email=email
            )

        except Editeur.DoesNotExist:

            messages.error(
                request,
                "Erreur : aucun éditeur trouvé avec cette adresse email."
            )

            return redirect("login_editeur")



        # Vérifier le mot de passe

        if check_password(password, editeur.password):


            # Création de la session

            request.session["editeur_id"] = editeur.id
            request.session["maison_id"] = editeur.maison.id
            request.session["editeur_nom"] = editeur.nom
            request.session["editeur_prenom"] = editeur.prenom
            request.session["role"] = "editeur"


            messages.success(
                request,
                f"Bienvenue {editeur.nom} {editeur.prenom}."
            )


            return redirect(
                "dashboard"
            )



        else:

            messages.error(
                request,
                "Erreur : mot de passe incorrect."
            )

            return redirect(
                "login"
            )



    return render(
        request,
        "dashboard.html"
    )

def logout_editeur(request):

    request.session.flush()

    messages.success(
        request,
        "Vous êtes déconnecté avec succès."
    )

    return redirect(
        "login"
    )
##creer article

def creer_article(request):

    # Vérifier la connexion
    if "role" not in request.session:

        messages.error(
            request,
            "Vous devez être connecté pour publier un article."
        )

        return redirect("login")


    # Vérifier le rôle
    if request.session.get("role") != "editeur":

        messages.error(
            request,
            "Accès refusé : seuls les éditeurs peuvent publier des articles."
        )

        return redirect("login")


    if request.method != "POST":
        return redirect("dashboard")


    editeur_id = request.session.get("editeur_id")

    try:

        editeur = Editeur.objects.get(
            id=editeur_id
        )

    except Editeur.DoesNotExist:

        request.session.flush()

        messages.error(
            request,
            "Votre session est invalide."
        )

        return redirect("login")


    titre = request.POST.get("titre")
    type_article = request.POST.get("type")
    prix = request.POST.get("prix")

    image = request.FILES.get("image")
    pdf = request.FILES.get("pdf")


    Article.objects.create(
        maison=editeur.maison,
        editeur=editeur,
        titre=titre,
        type=type_article,
        prix=prix,
        image=image,
        pdf=pdf
    )


    messages.success(
        request,
        "L'article a été publié avec succès."
    )

    return redirect("dashboard")

##modifier article
def modifier_article(request, article_id):

    if "editeur_id" not in request.session:

        messages.error(
            request,
            "Vous devez être connecté."
        )

        return redirect("login")


    editeur = get_object_or_404(
        Editeur,
        id=request.session["editeur_id"]
    )


    article = get_object_or_404(
        Article,
        id=article_id,
        maison=editeur.maison
    )


    if request.method == "POST":

        article.titre = request.POST.get("titre")

        article.type = request.POST.get("type")

        article.prix = request.POST.get("prix")


        if request.FILES.get("image"):
            article.image = request.FILES.get("image")


        if request.FILES.get("pdf"):
            article.pdf = request.FILES.get("pdf")


        article.save()


        messages.success(
            request,
            "L'article a été modifié avec succès."
        )


        return redirect("dashboard")


    return render(
        request,
        "modifier_article.html",
        {
            "article": article
        }
    )

##supprimer aticle
def supprimer_article(request, article_id):

    if "editeur_id" not in request.session:

        messages.error(
            request,
            "Vous devez être connecté."
        )

        return redirect("login")


    editeur = get_object_or_404(
        Editeur,
        id=request.session["editeur_id"]
    )


    article = get_object_or_404(
        Article,
        id=article_id,
        maison=editeur.maison
    )


    article.delete()


    messages.success(
        request,
        "L'article a été supprimé avec succès."
    )


    return redirect("dashboard")