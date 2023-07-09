from django.contrib import admin
from .models import Categoria, Producto,Adicional, Carrito, ItemsCarrito, Pedido,PruebaDatos,Calles,CategoriaDeBebidas

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Adicional)
admin.site.register(Carrito)
admin.site.register(ItemsCarrito)
admin.site.register(Pedido)
admin.site.register(PruebaDatos)
admin.site.register(Calles)
admin.site.register(CategoriaDeBebidas)