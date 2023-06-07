from django.contrib import admin
from board.models import Board

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_displat=("title","writer","content")
    
# admin.site.register(Board,BoardAdmin) # @admin.register(Board) 둘 중 하나만