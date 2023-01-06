from django.contrib import admin
from blog.models import Article,Comment, Tag


class TagInline(admin.StackedInline):
    model = Article.tags.through


class ArticleAdmin(admin.ModelAdmin):
    Inlines=[TagInline]
    #exclude=['tags',]


# Register your models here.
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)