from django.shortcuts import render
from editeur.models import Article

def indexvisiteur(request):
    articles = Article.objects.all().order_by('-date_publication')

    return render(
        request,
        'indexvisiteur.html',
        {
            'articles': articles
        }
    )
    



    