import array
from ctypes import Array
from multiprocessing import Value
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from django.db.models import Max
from .models import User, Listing, Bid, Watchlist, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listing":Listing.objects.filter(status="Open")
    })

def watchlist(request):
    w_items=[]
    watchlist_items = Watchlist.objects.filter(on_list="Yes", account=request.user.username)
    for watchlist_item in watchlist_items:
        w_items.append(watchlist_item.list_item)
    return render(request, "auctions/watchlist.html", {
        "listing":w_items
    })


def listing(request, product):
    item = Listing.objects.get(title=product)
    current_high=Bid.objects.filter(item=item).aggregate(Max("amount"))
    all_comments = Comment.objects.filter(comment_item = item)
    bidform = forms.bid(request.POST)
    closeform = forms.close(request.POST)
    watchform = forms.watchlist(request.POST)
    comment_form = forms.comment(request.POST)
    remove_watchform = forms.remove_watchlist(request.POST)
    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
                "listing": item,
                "current_high":current_high['amount__max'],
                "all_comments": all_comments
                })

    current_user = User.objects.get(username = request.user.username)
    watchlist_item = Watchlist.objects.get(list_item=item, account=request.user.username)
    if item.status == "Closed":
        check = Bid.objects.get(amount=current_high["amount__max"])
        if check.bidder == request.user:
            return render(request, "auctions/listing.html", {
                "listing": item,
                "current_high":current_high['amount__max'],
                "win_msg":"You have won the bid!",
                "all_comments": all_comments
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": item,
                "current_high":current_high['amount__max'],
                "win_msg":"This bid is closed!",
                "all_comments": all_comments
                })
    if item.owner == request.user.username:
        if closeform.is_valid():
            submitbutton = request.POST.get('submit')
            if submitbutton:
                item.status="Closed"
                item.save()
                return redirect(index)
        if request.method == "POST":
            if comment_form.is_valid():
                comment_content = comment_form.cleaned_data.get("content")
                if comment_content != '':
                    new_comment = Comment(content=comment_content, usr_account=request.user.username, comment_item=item)
                    new_comment.save()
                return redirect(listing, product=item.title) 
        if request.method == "POST":
            if watchform.is_valid():
                submitbutton1 = request.POST.get('submit_watch')
                if submitbutton1:                
                    watchlist_item.on_list = "Yes"
                    watchlist_item.save()
                    return redirect(watchlist)
        if request.method == "POST":
            if remove_watchform.is_valid():
                submitbutton2 = request.POST.get('submit_remove_watch')
                if submitbutton2:
                    watchlist_item.on_list = "No"
                    watchlist_item.save()
                    return redirect(watchlist)
        if watchlist_item.on_list == "Yes":    
            return render(request, "auctions/listing.html", {
                "listing": item,
                "current_high":current_high['amount__max'],
                "closeform":closeform,
                "remove_watchform":remove_watchform,
                "comment_form": comment_form,
                "all_comments": all_comments
                })
        if watchlist_item.on_list == "No":    
            return render(request, "auctions/listing.html", {
                "listing": item,
                "current_high":current_high['amount__max'],
                "closeform":closeform,
                "watchform":watchform,
                "comment_form":comment_form,
                "all_comments": all_comments
                })
    if request.method == "POST":
        if bidform.is_valid():
            price=0
            submitbid = request.POST.get('submitbid')
            if submitbid:
                price = bidform.cleaned_data.get("amount")
                if price > item.price:
                    bid = Bid(amount=price, item=item, bidder=current_user)   
                    bid.save()
                    return redirect(listing, product=item.title)
                elif watchlist_item.on_list == "No":
                    return render(request, "auctions/listing.html", {
                    "message": "Your bid must be higher than the current price!",
                    "bidform":bidform,
                    "watchform":watchform,
                    "listing": item,
                    "current_high":current_high['amount__max'],
                    "comment_form": comment_form,
                    "all_comments": all_comments
                    })
                elif watchlist_item.on_list == "Yes":
                    return render(request, "auctions/listing.html", {
                    "message": "Your bid must be higher than the current price!",
                    "bidform":bidform,
                    "remove_watchform":remove_watchform,
                    "listing": item,
                    "current_high":current_high['amount__max'],
                    "comment_form": comment_form,
                    "all_comments": all_comments
                    })
    if request.method == "POST":
        if watchform.is_valid():
            submitbutton1 = request.POST.get('submit_watch')
            if submitbutton1:                
                watchlist_item.on_list = "Yes"
                watchlist_item.save()
                return redirect(watchlist)
    if request.method == "POST":
        if remove_watchform.is_valid():
            submitbutton2 = request.POST.get('submit_remove_watch')
            if submitbutton2:
                watchlist_item.on_list = "No"
                watchlist_item.save()
                return redirect(watchlist)
    if request.method == "POST":
            if comment_form.is_valid():
                comment_content = comment_form.cleaned_data.get("content")
                new_comment = Comment(content=comment_content, usr_account=request.user.username, comment_item=item)
                new_comment.save()
                return redirect(listing, product=item.title) 
    
    if watchlist_item.on_list == "Yes":
        return render(request, "auctions/listing.html", {
                "bidform":bidform,
                "remove_watchform":remove_watchform,
                "listing": item,
                "current_high":current_high['amount__max'],
                "comment_form": comment_form,
                "all_comments": all_comments
            })
    elif watchlist_item.on_list == "No":
        return render(request, "auctions/listing.html", {
                "bidform":bidform,
                "watchform":watchform,
                "listing": item,
                "current_high":current_high['amount__max'],
                "comment_form": comment_form,
                "all_comments": all_comments,
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

def create(request):
    createform = forms.create(request.POST)
    all_users = User.objects.all()
    if request.method == "POST":
        if createform.is_valid():
            title = createform.cleaned_data.get("title")
            description = createform.cleaned_data.get("description")
            category = createform.cleaned_data.get("category")
            price = createform.cleaned_data.get("price")
            image = createform.cleaned_data.get("image")
            listing = Listing(title=title, description=description, price=price, image=image, owner=request.user.username, status="Open", category=category)
            listing.save()
            for each_user in all_users:
                watchlist_item = Watchlist(account=each_user.username, list_item=listing, on_list="No")
                watchlist_item.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "createform":createform
    })

def category(request):
    all_items = Listing.objects.all()
    categories=[]
    for each_item in all_items:
        if each_item.category not in categories:
            categories.append(each_item.category)
    return render(request, "auctions/category.html", {
        "categories":categories
    })

def categorylist(request, cat):
    all_items = Listing.objects.all()
    items_in_category = []
    for each_item in all_items:
        if each_item.category == cat:
            items_in_category.append(each_item)
    return render(request, "auctions/categorylist.html", {
        "items":items_in_category,
        "category":cat
    })


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
