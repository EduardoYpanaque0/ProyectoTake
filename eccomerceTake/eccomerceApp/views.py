from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from .models import *
import uuid
import gspread
from datetime import datetime
#SangucheriaTake
#Huskar!2



def Home(request):
    request.session.clear()
    return redirect(Menuss)

def Menuss(request):
    if request.method == 'POST':
        for key, value in request.session.items():
            print(key, value)
        print(request.POST.get('switch 1',None))
        if 'carritocreado' not in request.session :
            print("primero")
            carritoCreado = Carrito(usuario_id=request.session['identificador'])
            carritoCreado.save()
            request.session['carritocreado'] = carritoCreado.pk
        
        print(request.POST)

        cremas = ','.join(request.POST.getlist('cremas'))
        Precio = float((request.POST.get('PRECIO')).split("S/")[1])

        opcionalesles = request.POST.get('DatoAdicional',None)
        if request.POST.get('switch 1', None):
            opcionalesles = request.POST.get('switch 1', None)
            if request.POST.get('switch 3', None):
                opcionalesles = opcionalesles + ", " + request.POST.get('switch 3', None)
                if request.POST.get('switch 5', None):
                    opcionalesles = opcionalesles + ", " + request.POST.get('switch 5', None)
                    if request.POST.get('switch 7', None):
                        opcionalesles = opcionalesles + ", " + request.POST.get('switch 7', None)

        producto_seleccionado = Producto.objects.get(pk=request.session['productoSeleccionado'])
        categoria_producto = producto_seleccionado.categoria

        NuevoItemCarrito = ItemsCarrito(carrito = Carrito.objects.get(pk=request.session['carritocreado']),
                                    producto = producto_seleccionado,
                                    categoria_producto=categoria_producto,
                                    cantidad = request.POST.get('CantidadProducto'),
                                    tipo_papas = request.POST.get('tipos_de_papas'),
                                    ensalada = request.POST.get('ensalada'),
                                    cremas = cremas,
                                    opcionales = opcionalesles,
                                    precio = Precio)
        NuevoItemCarrito.save()
        lista_adicionales = request.POST.getlist('adicionales')
        adicionales_seleccionados = Adicional.objects.filter(nombreJunto__in=lista_adicionales)
        for adicional in adicionales_seleccionados:
            print(adicional)
            NuevoItemCarrito.adicionales.add(adicional)
        return redirect(Menuss)
    
    else:
        if 'identificador' not in request.session :
            request.session['identificador'] = str(uuid.uuid4())
        categorias = Categoria.objects.all()
        return render(request, 'menus.html', {'categorias': categorias})

def ItemsMenus(request):
    if request.method == 'POST':
        id_card = request.POST.get("idCard")
        productos = Producto.objects.filter(categoria__nombre=id_card)
        context={
            'productos': productos,
            'categoria':id_card
        }
        return render(request, 'itemMenus.html', context)
    
    else:
        return redirect(Menuss)

def FormItemsMenus(request):
    if request.method == 'POST':
        NameProducto = request.POST.get("idCard")
        productoSeleccionado = Producto.objects.filter(nombre_producto=NameProducto).first()
        request.session['productoSeleccionado'] = productoSeleccionado.pk
        categoriaProducto = str(productoSeleccionado.categoria)
        if categoriaProducto == "Bebidas":
            bebidaSeleccionadas = CategoriaDeBebidas.objects.filter(producto=productoSeleccionado).first()
            listBebida = bebidaSeleccionadas.elementoLista.split(",")
        else : 
            listBebida = False

        print(listBebida)
        adicionales = Adicional.objects.all()
        context={
            'producto': productoSeleccionado,
            'adicionales': adicionales,
            'categoria': categoriaProducto,
            'bebidaSeleccionada' : listBebida
        }
        return render(request, 'formItems.html',context)
    else:
        return redirect(Menuss)
    
def FormModifyItems(request):
    if request.method == 'POST':
        NameProducto = request.POST.get("idCarditem")
        modificarItem = ItemsCarrito.objects.get(pk=NameProducto)
        request.session['pkModificarItem'] = NameProducto
        productoSeleccionado = Producto.objects.filter(nombre_producto=modificarItem.producto).first()
        adicionales_list = modificarItem.adicionales.all().values_list('nombre', flat=True)
        if str(productoSeleccionado.categoria) == "Bebidas":
            bebidaSeleccionadas = CategoriaDeBebidas.objects.filter(producto=productoSeleccionado).first()
            listBebida = bebidaSeleccionadas.elementoLista.split(",")
            listBebida = [bebida.strip() for bebida in listBebida]
            eleccionBebidas = modificarItem.opcionales.split(",")
            eleccionBebidas = [elecbebida.strip() for elecbebida in eleccionBebidas]
        else : 
            listBebida = False
            eleccionBebidas = []

        print(listBebida)
        print(modificarItem.opcionales)
        print(modificarItem.precio)
        print(modificarItem.categoria_producto)
        print("-----------------------------------------------------------------------------------------------")
        adicionales = Adicional.objects.all()
        context={
            'producto': productoSeleccionado,
            'moficarItems': modificarItem,
            'listaAdicionales': adicionales_list,
            'bebidaSeleccionada' : listBebida,
            'eleccionBebida': eleccionBebidas,
            'adicionales': adicionales
        }
        return render(request, 'formModifyItems.html',context)
    else:
        return redirect(Menuss)
    
def ModificarItem(request):
    if request.method == 'POST':
        print(request.POST)
        cremas = ','.join(request.POST.getlist('cremas'))
        Precio = float((request.POST.get('PRECIO')).split("S/")[1])

        opcionalesles = request.POST.get('DatoAdicional')
        if request.POST.get('switch 1', None):
            opcionalesles = request.POST.get('switch 1', None)
            if request.POST.get('switch 3', None):
                opcionalesles = opcionalesles + ", " + request.POST.get('switch 3', None)
                if request.POST.get('switch 5', None):
                    opcionalesles = opcionalesles + ", " + request.POST.get('switch 5', None)
                    if request.POST.get('switch 7', None):
                        opcionalesles = opcionalesles + ", " + request.POST.get('switch 7', None)

        itemcarritoAntes = ItemsCarrito.objects.get(pk=request.session['pkModificarItem'])
        itemcarritoAntes.cantidad = request.POST.get("CantidadProducto")
        itemcarritoAntes.tipo_papas = request.POST.get("tipos_de_papas")
        itemcarritoAntes.ensalada = request.POST.get("ensalada")
        itemcarritoAntes.cremas = cremas
        itemcarritoAntes.adicionales.clear()
        itemcarritoAntes.opcionales = opcionalesles
        itemcarritoAntes.precio = Precio
        itemcarritoAntes.save()

        lista_adicionalesmodificar = request.POST.getlist('adicionales')
        print(lista_adicionalesmodificar)
        adicionales_seleccionados = Adicional.objects.filter(nombreJunto__in=lista_adicionalesmodificar)
        for adicional in adicionales_seleccionados:
            print(adicional)
            itemcarritoAntes.adicionales.add(adicional)

        print(request.session['pkModificarItem'])
        return redirect(CarritoCompra)

def CarritoCompra(request):
    
    if request.method == 'POST':
        id_card = request.POST.get("idCard")
        carrito = ItemsCarrito.objects.get(pk=id_card)
        carrito.delete()
        return redirect(CarritoCompra)
    else:
        if 'carritocreado' in request.session :
            itemscarrito = ItemsCarrito.objects.filter(carrito=request.session['carritocreado'])
            request.session['itemCarritoFormPedido'] = [item.pk for item in itemscarrito]
            if itemscarrito.exists():
                context = {
                    'itemscarrito': itemscarrito
                }
                return render(request, 'carrito.html', context)
            else:
                context = {
                    'itemscarrito': "sinElementos"
                }
                return render(request, 'carrito.html', context)
        else:
            context={
                'itemscarrito': "sinElementos"
            }
            return render(request, 'carrito.html', context)
        
def FormPedido(request):
    if request.method == 'POST':
        print(request.POST)
        calles = Calles.objects.all()
        request.session['TotalPedidoActual'] = request.POST.get('TotalPedido')
        request.session['botonSeleccionadoPedido'] = request.POST.get('opcion')
        context = {
            'opcionBtn': request.POST.get('opcion'),
            'totalPedido': request.POST.get('TotalPedido'),
            'calles': calles
        }
        return render(request, 'formPedido.html',context)
    else:
        return redirect(Menuss)

def EnviarPedido(request):
    if request.method == 'POST':
        print(request.POST)
        vueltoEs = request.POST.get('VueltoDe')
        if not request.POST.get('VueltoDe') :
            vueltoEs = 0.00
        TotalPedido = float((request.session['TotalPedidoActual']).split("S/")[1])
        if request.session['botonSeleccionadoPedido'] == "domicilio":
            calleNumero = request.POST.get('nombreCalle') + " "+ request.POST.get('numeroDomicilio')
            if "Otra Ubicacion" in request.POST.get('nombreCalle') :
                calleNumero = request.POST.get('NombreCalle2')+ " " + request.POST.get('numeroDomicilio')

            nuevoItemPedido = Pedido(usuario_id = request.POST.get('nombreCliente'),
                                    nombreDeCalle = calleNumero,
                                    numeroContacto = request.POST.get('numeroContacto'),
                                    metodoDePago = request.POST.get('metodoPago'),
                                    total = TotalPedido,
                                    vueltoDe = vueltoEs)
        else :
            nuevoItemPedido = Pedido(usuario_id = request.POST.get('nombreCliente'),
                                    numeroContacto = request.POST.get('numeroContacto'),
                                    metodoDePago = request.POST.get('metodoPago'),
                                    total = TotalPedido,
                                    vueltoDe = vueltoEs)
        nuevoItemPedido.save()
        lista_items_carrito = request.session['itemCarritoFormPedido']
        itemsCarritoSeleccionados = ItemsCarrito.objects.filter(pk__in=lista_items_carrito)
        for index,itemcarrito in enumerate(itemsCarritoSeleccionados):
            print(itemcarrito)
            nuevoItemPedido.items.add(itemcarrito)            
            lista = ListaPedido(itemcarrito)
            if index >= 1 : 
                listaCompleta = listaCompleta + "\n\n-----------------------------\n\n" + lista.strip()
            else : 
                listaCompleta = lista.strip()

        print(listaCompleta)
        print("////////////////////////////////////////////////////////////////////////////////")

        
        sa = gspread.service_account(filename="C:/Users/user/Desktop/EL TAKE/eccomerceTake/eccomerceApp/static/archivos/eltake-6fb6c015a363.json")
        sh = sa.open("El TAKE")
        wks = sh.sheet1
        values = [
            str(request.POST.get('nombreCliente')), 
            int(request.POST.get('numeroContacto')), 
            int(TotalPedido), 
            str(datetime.now()), 
            str(datetime.now()), 
            str(request.POST.get('metodoPago')),
            "",
            float(vueltoEs),
            str(listaCompleta),
            "",
            "",
            str(calleNumero),
            "",
            1,
            "",
            0
            ]
        wks.append_row(values)
        
        return redirect(Home)
    else:
        return redirect(Menuss)
    
def ListaPedido(ProductoCarrito):
    cremas = ProductoCarrito.cremas if ProductoCarrito.cremas != "" else "Sin Cremas"
    if str(ProductoCarrito.categoria_producto).strip() != "Bebidas":

        if ProductoCarrito.adicionales == None:
            textList = f"{ProductoCarrito.cantidad} --> {ProductoCarrito.producto} con: \n{cremas} \n{ProductoCarrito.tipo_papas} \n{ProductoCarrito.ensalada} \n{ProductoCarrito.adicionales} \n{ProductoCarrito.opcionales}"
        else:
            textList = f"{ProductoCarrito.cantidad} --> {ProductoCarrito.producto} con: \n{cremas} \n{ProductoCarrito.tipo_papas} \n{ProductoCarrito.ensalada} \nSin Adicionales  \n{ProductoCarrito.opcionales}"
    else:
        opcionbebida = ProductoCarrito.opcionales.split(",")
        bebida = ""
        for elecbebida in opcionbebida:
            bebida = bebida + f"{elecbebida.strip()}\n"
        textList = f"{ProductoCarrito.cantidad} --> {ProductoCarrito.producto} con: \n{bebida} \n \n"
    return textList

