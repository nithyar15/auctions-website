from django.contrib import admin
from .models import Listing, User, Bid, Watchlist, Comment

class listing_admin(admin.ModelAdmin):
    list_display = ("id", "title", "description","owner","status", "price","category", "image")
class watchlist_admin(admin.ModelAdmin):
    list_display = ("id", "account", "on_list", "list_item")
class bid_admin(admin.ModelAdmin):
    list_display = ("id", "amount", "item","bidder")

admin.site.register(Listing, listing_admin)
admin.site.register(User)
admin.site.register(Bid, bid_admin)
admin.site.register(Watchlist, watchlist_admin)
admin.site.register(Comment)