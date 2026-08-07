from django.shortcuts import render,redirect


def index(request):
    return render(request,'index.html')

def login_view(request):
    return render(request,'login_form.html')

def editeur_form(request):
    return render(request,'editeur_form.html')

def maison_edition_form(request):
    return render(request,'maison_edition_form.html')

def dashboard_form(request):
    return render(request,'dashboard.html')








# def login_view(request):
#     if request.method = "post":
#  form = LoginForm(request.POST)
#  if form.is_valid():
#     email = form.cleaned_data["email"]
#     password = form.cleaned_data["password"]
#     user = authenticate(request, usermane=email, password=password)
#     if user is not none :
#         login(request, user)
#         return redirect("index")
#     else:
#         form.add_error(none, "email ou mot de passe incorrect")
#     else:
#         form = LoginForm()
#         return render(request, "login_form.html" , {"form": form})

# def editeur_view(request):
#     if request.method = "POST":
#  form = LoginForm(request.POST)
#  if form.is_valid():
#     # creer le compte editeur ici
#      return redirect("login")
#  else:
#         form = EditeurForm()
#         return render(request, "editeur_form.html" , {"form": form})
