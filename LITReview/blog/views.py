from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('post'))
    elif request.user.is_authenticated:
        return redirect('feed')
    else:
        return render(request, 'index.html')


def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'registration.html', {
                'message': 'les mots de pass doivent correspondre'
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'registration.html', {
                'message': 'Nom déjà prit'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'registration.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def post(request):
    return render(request, 'post.html')
