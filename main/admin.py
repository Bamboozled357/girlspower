from django.contrib import admin

from main.models import Message, Favorite, Publication, Comment, PublicationImage, PublicationLikes

admin.site.register(Message)
admin.site.register(Favorite)
admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(PublicationImage)
admin.site.register(PublicationLikes)



