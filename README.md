# EZSGAME
En general ezsgame Trata de hacer mas simple el proceso de Creacion y manipulacion de graficos 2D. Creando y simplificando el proceso lo mas posible. Tratando de hacerlo mas facil, divertudo y comodo para el usuario.

## Instalacion 

- Descargar ezsgame.zip  [aqui](https://github.com/NoxxDev/ezsgame)

- Clonar repositorio [aqui](https://github.com/NoxxDev/ezsgame.git) (https)

#
#
## Conceptos 
- pos - Posicion del objeto en el espacio.  (x,y)

- size - Tamaño del objeto en el espacio.  (ancho,alto)

- color - Color del objeto.  (r,g,b) o "Nombre del color"

- Screen - Pantalla en la que se dibuja el objeto. Todo sucede en una pantalla.


#
#
# Inicio

```python
# Declara la pantalla
screen = Screen(size=(640, 480), title="Mi App")

# Declarar un objeto
mi_rect =  Rect(pos=["center", "center"], size=(100, 100), color="red")

# Bucle principal
while True:
    # Check de eventos
    screen.check_events()

    # llenar la pantalla de color
    screen.fill("black")

    # Dibujar el objeto
    mi_rect.draw(screen)

    # Actualizar la pantalla
    screen.update()
```
#
#

# Documentacion 
## [>> Ir a la documentacion](https://ezsgame-doc.ezsnova.repl.co/)