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
from ezsgame.main import *

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

# Documentacion (Aun no completa)
## [>> Ir a la documentacion](https://ezsgame-doc.ezsnova.repl.co/)


#
#
# Convicciones 
- # archivos :
    - ### Los archivos que usan ezsgame que son el archivo "principal", suelen llamarse:
        ## demo.py (Recomendado)
        ## main.py
        ## game.py
        ## app.py


