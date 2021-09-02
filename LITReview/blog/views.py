from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError

from .forms import UploadTicketForm, UploadReviewForm

from .models import User, Ticket, UserFollows, Review


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
        return redirect('post')
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


@login_required
def flux(request):
    """Show user's feed"""
    tickets = Ticket.objects.all
    reviews = Review.objects.all
    return render(request, "flux.html", {"tickets": tickets, "reviews": reviews})


@login_required
def subscribe(request):
    """Show user's following posts"""
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, "subscribe.html", {"following": following, "followers": followers})


@login_required
def edit_critical(request, review_id):
    """Let user update a review"""
    if request.method == "POST":
        review_update = Review.objects.get(id=review_id)
        review_update.headline = request.POST["headline"]
        review_update.body = request.POST["body"]
        review_update.rating = request.POST["rating"]
        review_update.save()
        return HttpResponseRedirect(reverse("post"))
    else:
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form_review = UploadReviewForm(initial={"user": request.user,
                                                "ticket": review.ticket,
                                                "headline": review.headline,
                                                "body": review.body,
                                                "rating": review.rating,
                                                })
        return render(request, "edit_critical.html", {"review": review, "form_review": form_review, "ticket": ticket})


@login_required
def edit_ticket(request, ticket_id):
    """Let user update a ticket"""
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket_update = Ticket.objects.get(id=ticket_id)
        form_ticket = UploadTicketForm(request.POST, request.FILES, instance=ticket_update)
        if form_ticket.is_valid():
            form_ticket.save()
            return HttpResponseRedirect(reverse("post"))
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user,
                                                "title": ticket.title,
                                                "description": ticket.description,
                                                "image": ticket.image,
                                                })
        return render(request, "edit_ticket.html", {"ticket": ticket, "form_ticket": form_ticket})


@login_required
def ticket_respond(request, id):
    """Create review in response to a ticket"""
    if request.method == "POST":
        ticket = Ticket.objects.get(id=id)
        review = Review.objects.create(
            headline=request.POST["headline"],
            body=request.POST["body"],
            user=request.user,
            rating=request.POST["rating"],
            ticket=ticket
        )
        review.save()
        return HttpResponseRedirect(reverse("view-posts"))
    else:
        ticket = Ticket.objects.get(id=id)
        return render(request, "ticket_respond.html", {"ticket": ticket})
