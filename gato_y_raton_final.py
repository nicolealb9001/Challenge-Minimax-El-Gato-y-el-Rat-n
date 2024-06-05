import pygame
import sys
import numpy as np

# Inicializar Pygame
pygame.init()

# Dimensiones del tablero
tamanho_tablero = 7
tamanho_celda = 80
tablero = np.zeros((tamanho_tablero, tamanho_tablero), dtype=int)

# colores
rosa_claro = (255, 182, 193)
rosa = (255, 105, 180)
rosa_oscuro = (255, 20, 147)
negro = (0, 0, 0)

# Inicializar pantalla
pantalla = pygame.display.set_mode((tamanho_tablero * tamanho_celda, tamanho_tablero * tamanho_celda))
pygame.display.set_caption('Challenge Minimax: Gato y Ratón')

# Función para dibujar el tablero
def dibujar_tablero():
    pantalla.fill(rosa_claro)  # Rellenamos el fondo de rosa
    for fila in range(tamanho_tablero): #Recorre todas las filas del tablero
        for columna in range(tamanho_tablero): # Recorre todas las columnas del tablero
            # Definimos las casillas y las dibujamos
            #                          (posicion_x,             posicion_y,          ancho,          alto)
            borde_celda = pygame.Rect(columna * tamanho_celda, fila * tamanho_celda, tamanho_celda, tamanho_celda)
            # pygame.draw.rect dibuja cada celda en la pantalla
            #               (superficie, color,borde de la celda, grosor de la línea)
            pygame.draw.rect(pantalla, rosa_oscuro, borde_celda, 1)

# Cargar imágenes y darles un tamaño
gato_img = pygame.image.load('gato.png')  # Imagen del gato
raton_img = pygame.image.load('raton.png')  # Imagen del ratón
gato_img = pygame.transform.scale(gato_img, (tamanho_celda, tamanho_celda))
raton_img = pygame.transform.scale(raton_img, (tamanho_celda, tamanho_celda))

# Función para dibujar las piezas
def dibujar_piezas():
    for fila in range(tamanho_tablero):
        for columna in range(tamanho_tablero):
            #  tablero[indice][indice]
            if tablero[fila][columna] == 1:  # Gato
                # dibuja en pantalla(gato_img,(posicion_en_x, posicion_en_y))
                pantalla.blit(gato_img, (columna * tamanho_celda, fila * tamanho_celda))
            elif tablero[fila][columna] == 2:  # Ratón
                pantalla.blit(raton_img, (columna * tamanho_celda, fila * tamanho_celda))

# Posiciones iniciales
posicion_raton = (tamanho_tablero - 1, tamanho_tablero // 2)  # Centro de la parte inferior del tablero
posicion_gato = (0, tamanho_tablero // 2)  # Centro de la parte superior del tablero
tablero[posicion_gato] = 1  # 1 representa el gato
tablero[posicion_raton] = 2  # 2 representa el raton

# Función para calcular la distancia (distancia Manhattan) entre dos posiciones
def distancia(pos1, pos2): # pos1 y pos2 son tuplas de dos elementos cada una, representando las coordenadas (fila, columna) de dos posiciones en el tablero.
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Función para obtener movimientos válidos tipo torre
def movimientos_validos(posicion): 
    y, x = posicion
    movimientos = [] #Se inicializa una lista movimientos que almacenará todos los movimientos válidos desde la posición dada.

    # Movimientos hacia arriba
    for i in range(1, tamanho_tablero):
        if y - i >= 0:
            if tablero[y - i, x] == 0 or tablero[y - i, x] == 2:
                movimientos.append((y - i, x))
            if tablero[y - i, x] != 0:
                break
        else:
            break

    # Movimientos hacia abajo
    for i in range(1, tamanho_tablero):
        if y + i < tamanho_tablero:
            if tablero[y + i, x] == 0 or tablero[y + i, x] == 2:
                movimientos.append((y + i, x))
            if tablero[y + i, x] != 0:
                break
        else:
            break

    # Movimientos hacia la izquierda
    for i in range(1, tamanho_tablero):
        if x - i >= 0:
            if tablero[y, x - i] == 0 or tablero[y, x - i] == 2:
                movimientos.append((y, x - i))
            if tablero[y, x - i] != 0:
                break
        else:
            break

    # Movimientos hacia la derecha
    for i in range(1, tamanho_tablero):
        if x + i < tamanho_tablero:
            if tablero[y, x + i] == 0 or tablero[y, x + i] == 2:
                movimientos.append((y, x + i))
            if tablero[y, x + i] != 0:
                break
        else:
            break

    return movimientos

# Algoritmo minimax
def minimax(posicion_gato, posicion_raton, depth, maximizando, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or posicion_gato == posicion_raton:
        return distancia(posicion_gato, posicion_raton), None

    if maximizando:  # Turno del ratón
        max_eval = float('-inf')
        mejor_movimiento = None

        for mov in movimientos_validos(posicion_raton):
            eval, _ = minimax(posicion_gato, mov, depth - 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                mejor_movimiento = mov
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento
    else:  # Turno del gato
        min_eval = float('inf')
        mejor_movimiento = None

        for mov in movimientos_validos(posicion_gato):
            eval, _ = minimax(mov, posicion_raton, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                mejor_movimiento = mov
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento

# Función para mostrar mensaje en la pantalla
def draw_text(text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, negro)
    text_rect = text_surface.get_rect(center=(tamanho_tablero * tamanho_celda // 2, tamanho_tablero * tamanho_celda // 2))
    pantalla.blit(text_surface, text_rect)
    pygame.display.flip()

def draw_welcome_message():
    pantalla.fill(rosa_claro)  # Rellenamos el fondo de rosa.
    font = pygame.font.Font(None, 36)
    welcome_text = ["Bienvenido al juego del gato y del ratón:", 
                    "¡Tu misión es hacer que el ratón llegue",
                    "a salvo al otro lado del tablero! ",
                    "El gato no debe atrapar al ratón."]
    
    for i, line in enumerate(welcome_text):
        text_surface = font.render(line, True, rosa_oscuro)
        text_rect = text_surface.get_rect(center=(tamanho_tablero * tamanho_celda // 2, tamanho_tablero * tamanho_celda // 2 - 50 + i * 40))
        pantalla.blit(text_surface, text_rect)
    
    pygame.display.flip()  # Actualizamos la pantalla.
    pygame.time.wait(10000)  # Esperamos 10 segundos antes de empezar el juego.

# Función principal para ejecutar el juego
def ejecutar_juego(posicion_gato, posicion_raton, depth):
    draw_welcome_message()
    turno_raton = True
    juego_terminado = False
    mensaje = ""

    while not juego_terminado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and turno_raton:
                mouse_pos = pygame.mouse.get_pos()
                fila = mouse_pos[1] // tamanho_celda
                columna = mouse_pos[0] // tamanho_celda
                if (fila, columna) in movimientos_validos(posicion_raton):
                    posicion_raton = (fila, columna)
                    turno_raton = False

        if not turno_raton:
            _, mejor_mov = minimax(posicion_gato, posicion_raton, depth, False)
            if mejor_mov:
                posicion_gato = mejor_mov
            turno_raton = True

        if posicion_raton[0] == 0:
            juego_terminado = True
            mensaje = "¡GANASTE! El ratón logró escapar"
        if posicion_gato == posicion_raton:
            juego_terminado = True
            mensaje = "¡PERDISTE! El gato atrapó al ratón"
            tablero[posicion_raton] = 0

        tablero.fill(0)
        tablero[posicion_gato] = 1
        if not juego_terminado or (juego_terminado and mensaje != "¡PERDISTE! El gato atrapó al ratón"):
            tablero[posicion_raton] = 2

        dibujar_tablero()
        dibujar_piezas()
        pygame.display.flip()

    dibujar_tablero()
    dibujar_piezas()
    draw_text(mensaje)
    pygame.display.flip()
    pygame.time.wait(10000)

# Ejecutamos el juego
ejecutar_juego(posicion_gato, posicion_raton, 5)
