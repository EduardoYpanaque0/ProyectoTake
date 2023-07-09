from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categorias/', default='path/to/default/image.jpg')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_producto

class CategoriaDeBebidas(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    elementoLista = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.producto.nombre_producto

class Adicional(models.Model):
    nombre = models.CharField(max_length=100)
    nombreJunto = models.CharField(max_length=100, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario_id = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Carrito ({self.usuario_id})"

class ItemsCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    tipo_papas = models.CharField(max_length=100, default="Sin Papas")  # Agregar campo tipo de papas
    ensalada = models.CharField(max_length=100, default="Sin Ensalada")  # Agregar campo tipo de papas
    cremas = models.CharField(max_length=100, null=True)  # Agregar campo cremas
    adicionales = models.ManyToManyField(Adicional)
    opcionales = models.TextField(null=True)  # Agregar campo opcionales
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Agregar campo precio

    def __str__(self):
        return f"Item de Carrito {self.id}"

class Pedido(models.Model):
    fecha_pedido = models.DateField(auto_now_add=True)
    usuario_id = models.CharField(max_length=100)
    nombreDeCalle = models.CharField(max_length=100, null=True)
    numeroContacto = models.PositiveIntegerField(null=True)
    metodoDePago = models.CharField(max_length=10, default="Efectivo")
    total = models.DecimalField(max_digits=8, decimal_places=2)
    vueltoDe = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    items = models.ManyToManyField(ItemsCarrito)

    def __str__(self):
        return f"Pedido ({self.usuario_id}) - Total: {self.total}"
    
class Calles(models.Model):
    direccion = models.CharField(max_length=100, default="")
    direccionCorta = models.CharField(max_length=100 , default="")

    def __str__(self):
        return self.direccion

class PruebaDatos(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    tipo_papas = models.CharField(max_length=100, default="Sin Papas")  # Agregar campo tipo de papas
    ensalada = models.CharField(max_length=100, default="Sin Ensalada")  # Agregar campo tipo de papas
    cremas = models.CharField(max_length=100, null=True)  # Agregar campo cremas
    adicionales = models.ManyToManyField(Adicional)
    opcionales = models.TextField(null=True)  # Agregar campo opcionales
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Agregar campo precio

    def __str__(self):
        return f"Item de PruebaDatos {self.id}"