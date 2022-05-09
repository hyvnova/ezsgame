# EZSGAME
En general ezsgame Trata de hacer mas simple el proceso de Creacion y manipulacion de graficos 2D. Creando y simplificando el proceso lo mas posible. Tratando de hacerlo mas facil, divertido y comodo para el usuario.

## Instalacion 
- [ 1 ] Crea una carpeta dedica para ezsgame, asi sera mas facil de manejar la instalacion.

- [ 2 ]  Instalar las dependencias. con el comando:

```bash
pip install -r requirements.txt
```

- [ 3 ] Descargar el repositorio de ezsgame. Debe ir dentro de la carpeta que creaste en el paso 1.

    - Descargar ezsgame.zip  [aqui](https://github.com/NoxxDev/ezsgame)

    - Clonar repositorio [aqui](https://github.com/NoxxDev/ezsgame.git) (https)

- [ 4 ] Creando Archivos, los archivos que usaran ezsgame deben comenzar con la siguiente linea para importar ezsgame:

```python
from ezsgame.all import *

# Tu codigo aqui

```

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
mi_rect =  Rect(pos=["center", "center"], size=(100, 100), color="red", screen=screen)

# Bucle principal
while True:
    # Check de eventos
    screen.check_events()

    # llenar la pantalla de color
    screen.fill("black")

    # Dibujar el objeto
    mi_rect.draw()

    # Actualizar la pantalla
    screen.update()
```
#
#

# Documentacion (Aun no completa)
## Pagina : [>> Ir a la documentacion](https://ezsgame-doc.ezsnova.repl.co/)
## FigJam : [>> Ir a Figma](https://www.figma.com/file/EpJeUfdcxbwZSO5c4lr6rT/ezsgame-doc?node-id=1%3A2)


#
#
# Convicciones 
- ## archivos :
    - ### Los archivos que usan ezsgame que son el archivo "principal", suelen llamarse:
        - #### demo (Recomendado)
        - #### main
        - #### game
        - #### app


