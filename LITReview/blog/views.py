from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadTicketForm, UploadReviewForm
from .models import User, Ticket, UserFollows, Review
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("flux"))
        else:
            messages.error(request, 'Mot de passe ou nom de compte incorrecte')
            return render(request, "index.html")
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, "register.html")
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Nom d'utilisateur déjà prit")
            return render(request, "register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("flux"))
    else:
        return render(request, "register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def subscribe(request):
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, "subscribe.html", {"following": following,
                                              "followers": followers})


@login_required
def update_review(request, review_id):
    if request.method == "POST":
        review_update = Review.objects.get(id=review_id)
        review_update.headline = request.POST["headline"]
        review_update.body = request.POST["body"]
        review_update.rating = request.POST["rating"]
        review_update.save()
        return HttpResponseRedirect(reverse("posts"))
    else:
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form_review = UploadReviewForm(initial={"user": request.user,
                                                "ticket": review.ticket,
                                                "headline": review.headline,
                                                "body": review.body,
                                                "rating": review.rating,
                                                })
        return render(request, "update_review.html",
                      {"review": review, "form_review": form_review,
                       "ticket": ticket})


@login_required
def update_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket_update = Ticket.objects.get(id=ticket_id)
        form_ticket = UploadTicketForm(request.POST, request.FILES,
                                       instance=ticket_update)
        if form_ticket.is_valid():
            form_ticket.save()
            return HttpResponseRedirect(reverse("posts"))
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user,
                                                "title": ticket.title,
                                                "description":
                                                    ticket.description,
                                                "image": ticket.image,
                                                })
        return render(request, "update_ticket.html",
                      {"ticket": ticket, "form_ticket": form_ticket})


@login_required
def add_user_follow(request):
    data_follow = request.POST
    username_search = data_follow["username_search"]
    username_search = User.objects.get(username=username_search)
    user_follow = UserFollows.objects.create(
        user=request.user,
        followed_user=username_search
    )
    user_follow.save()
    return HttpResponseRedirect(reverse("subscribe"))


@login_required
def remove_user_follow(request):
    followed_user = request.POST["followed_user"]
    user_defollow = UserFollows.objects.filter(followed_user=followed_user)\
        .filter(user=request.user)
    user_defollow.delete()
    return HttpResponseRedirect(reverse("subscribe"))


@login_required
def create_ticket(request):
    if request.method == "POST":
        form_ticket = UploadTicketForm(request.POST, request.FILES)
        if form_ticket.is_valid():
            form_ticket.save()
            return HttpResponseRedirect(reverse("flux"))
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user})
        return render(request, "create_ticket.html",
                      {'form_ticket': form_ticket})


@login_required
def create_review(request):
    if request.method == "POST":
        form_ticket = UploadTicketForm(request.POST, request.FILES)
        form_review = UploadReviewForm(request.POST)
        if form_ticket.is_valid():
            form_ticket.save()
        ticket = Ticket.objects.filter(user=request.user)\
            .latest("time_created")
        headline = request.POST["headline"]
        body = request.POST["body"]
        user = request.user
        rating = request.POST["rating"]
        ticket = ticket
        review = Review.objects.create(
            headline=request.POST["headline"],
            body=request.POST["body"],
            user=request.user,
            rating=request.POST["rating"],
            ticket=ticket
        )
        return HttpResponseRedirect(reverse("posts"))
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user})
        form_review = UploadReviewForm(initial={"user": request.user})
        return render(request, "create_review.html",
                      {"form_ticket": form_ticket, "form_review": form_review})


@login_required
def reply(request, id):
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
        return HttpResponseRedirect(reverse("posts"))
    else:
        ticket = Ticket.objects.get(id=id)
        return render(request, "reply.html", {"ticket": ticket})


@login_required
def flux(request):
    tickets = Ticket.objects.all
    reviews = Review.objects.all
    return render(request, "flux.html",
                  {"tickets": tickets, "reviews": reviews})


@login_required
def posts(request):
    reviews = Review.objects.filter(user=request.user)
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, "posts.html",
                  {"reviews": reviews, "tickets": tickets})


def handle_not_found(request, exception):
    return render(request, '404.html')
