from django.contrib import admin

from .models import User, Category, Listing, Comment, Bid

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "categoryName",
    )

class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "listing",
        "user",
    )

class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "listing",
        "price",
        "bidder",
    )

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)