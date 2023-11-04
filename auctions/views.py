from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal

from .models import User, Category, Listing, Comment, Bid


def index(request):
    listing = Listing.objects.filter(activation=True).order_by("-time")
    return render(request, "auctions/index.html", {
        "listing": listing
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
    

def create_listing(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = Category.objects.get(categoryName = request.POST["category"])
        photo = request.POST["photo"]
        price = request.POST["price"]
        activation = request.POST["activation"]
        user = request.user
        if not title or not price:
            return render(request, "auctions/error.html", {
                "message":"Must Enter a Title and Price!"
            })

        listing = Listing(
            title=title, 
            description=description, 
            category=category,
            photo=photo, 
            price=float(price), 
            activation=activation, 
            user=user
        )
        listing.save()

        return HttpResponseRedirect(reverse(index))

    return render(request, "auctions/create_listing.html", {
        "categories": categories
    })

def edit_listing(request, listing_id):
    categories = Category.objects.all()
    listing = Listing.objects.get(pk = listing_id)
    if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            category = Category.objects.get(categoryName = request.POST["category"])
            photo = request.POST["photo"]
            activation = request.POST["activation"]

            if not title:
                return render(request, "auctions/error.html",{
                    "message":"Must Enter a Title"
                })

            listing.title = title
            listing.description = description
            listing.category = category
            listing.photo = photo
            listing.activation = activation
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    return render(request, "auctions/edit.html", {
        "categories": categories,
        "listing": listing,
    } )


def listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    comment = Comment.objects.filter(listing = listing_id).order_by("-time")
    user = request.user
    bids = Bid.objects.filter(listing = listing_id)
    top = bids.order_by("-price").first()
    counter = bids.count()
    categories = Category.objects.all()
    if request.method == "POST":
        if 'add' in request.POST:
            watchlist = request.POST["add"]
            user.watchlist.add(listing)

            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        if 'remove' in request.POST:
            watchlist = request.POST["remove"]
            user.watchlist.remove(listing)

            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        if 'placebid' in request.POST:
            price = Decimal(request.POST["placebid"])
            if top and price > top.price:
                
                bid = Bid(
                    listing=listing,
                    price=price,
                    bidder=user
                )
                bid.save()
                listing.currentprice = price
                listing.save()

                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            
            elif not top and price >= listing.price:
                bid = Bid(
                    listing=listing,
                    price=price,
                    bidder=user
                )
                bid.save()

                listing.currentprice = price
                listing.save()
                
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        
            else:
                return render(request,"auctions/error.html", {
                    "message": "Must Be Greater Than Current Price"
                })


        if 'new_comment' in request.POST:
            new_comment = request.POST["new_comment"]
            new = Comment(
                user=user,
                listing=listing,
                comment=new_comment,
            )
            new.save()

            return render(request, "auctions/listing.html", {
                "listing":listing,
                "comment": comment,
                "top": top,
                "counter": counter,
            })
        
        if 'edit' in request.POST:
                      
            return render(request, "auctions/edit.html", {
                "categories": categories,
                "listing":listing,
            })

        if 'activation' in request.POST:
            activation = request.POST["activation"]
            listing.activation = activation
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
    


    return render(request, "auctions/listing.html", {
        "listing":listing,
        "comment": comment,
        "top": top,
        "counter": counter, 
    })

def bid(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if listing:
        bid = Bid.objects.filter(listing = listing).order_by("-price")
        return render(request, "auctions/bids.html", {
            "bid":bid,
        })
    else:
        return render(request, "auctions/error.html", {
            "message":"Listing Not Exist."
        })
    

def user(request):
    user = request.user
    listing = Listing.objects.filter(user = user.id) 
    bid = Bid.objects.filter(bidder = user.id).order_by("-time")
    watchlist = user.watchlist
    return render(request, "auctions/user.html", {
        "user":user,
        "bid":bid,
        "listing":listing,
    })