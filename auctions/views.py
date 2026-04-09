from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .models import User, Listing, Bid


def index(request):
    listings = Listing.objects.all()



    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        min_bid = request.POST["min_bid"]
        image = request.POST["image"]
        category = request.POST["category"]

        new_listing = Listing(creator=user, title=title, description=description, starting_bid=min_bid, image=image, category=category)
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
    })

@login_required(login_url="/login")
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        new_bid = int(request.POST["bid"])
        user = request.user
        try:
            bid = listing.bids.get()
        except:
            if new_bid >= listing.starting_bid:
                bid = Bid(listing=listing, bidder=user, amount=new_bid)
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Not appropriate bid"
                })
        else:
            if new_bid >= bid.amount + listing.starting_bid:
                bid.amount = new_bid
                bid.bidder = user
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Not appropriate bid"
                })
        bid.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

@login_required
def watchlist(request):
    user = request.user
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)

        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, "auctions/index.html", {
            "listings": user.watchlist.all()
        })