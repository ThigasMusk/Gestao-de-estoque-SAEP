from django.contrib import admin
from .models import Produto, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'quantidade', 'preco')
    search_fields = ('nome', 'codigo')

admin.site.register(Movimentacao)