# EZSGAME
En general ezsgame Trata de hacer mas simple el proceso de Creacion y manipulacion de graficos 2D. Creando y simplificando el proceso lo mas posible. Tratando de hacerlo mas facil, divertudo y comodo para el usuario.

## Conceptos 
- pos - Posicion del objeto en el espacio.  (x,y)

- size - Tamaño del objeto en el espacio.  (ancho,alto)

- color - Color del objeto.  (r,g,b) o "nombre de color"

- Screen - Pantalla en la que se dibuja el objeto. Todo sucede en una pantalla.

- IScreen - Interface Screen. Pantalla de interfaz. Permite usar otro tipo de caracteristicas en la pantalla.

# Instalar requeriments
```bash
pip install -r requirements.txt
```

# Inicio

```python
# declare a  Screen object
screen = Screen(size=(640, 480), title="My Game")

# Declarar un objeto
mi_rect =  Rect(pos=["center", "center"], size=(100, 100), color="red")

# Bucle principal
while True:
    # Check de eventos
    screen.check()

    # llenar la pantalla de color
    screen.fill((0, 0, 0))

    # Dibujar el objeto
    mi_rect.draw(screen)

    # Actualizar la pantalla
    screen.update()
```

