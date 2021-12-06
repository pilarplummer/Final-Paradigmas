import pygame

#Comienzo a confirgurar una pantalla de juego circular, en donde se da la forma.
#Luego se establece un bucle el cual verifica todo lo que hace el jugador (presionar teclas, mover el teclado, etc).

#CONSTANTES__________________________
ANCHO, ALTURA = 600, 600
FILAS, COLUMNAS = 8, 8
#Qué tan grande es un cuadrado del tablero.
TAMAGNO_CUADRADO = ANCHO//COLUMNAS

#PYGAME = RGB
ROJO = (255, 105 , 97) #ROJO PASTEL
BLANCO = (224, 176, 255) #MALVA
NEGRO = (20, 20, 20) #NEUTRO
GRIS = (128, 128, 128)
AZUL = (59, 131, 189) #AZUL COBALTO/LUMINOSO

CORONA = pygame.transform.scale(pygame.image.load("corona.png"), (45, 25)) #Se carga el activo 'corona'.
#Por defecto, la imagen es grande. Entonces el tamaño debe quepar en las piezas. Relación de aspecto.
#______________________________________

#Se crean "Clases", en la que coloco todas las funciones, atributos de cada parte del juego, incluidos __init__.
#El objetivo fundamental del método __init__ es inicializar los atributos del objeto que yo cree.

#PIEZAS________________________________
class Piezas:
    RELLENO = 15
    BORDE = 2

    def __init__(self, fil, col, color):
        self.fil = fil
        self.col = col
        self.color = color
        self.king = False #Esto nos dice si somos una pieza de Rey, eso significa que se puede ir hacia atrás.
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self): #Método que calcula la posición (en X e Y), basado en la columna y fila que la ficha se encuentra.
        self.x = TAMAGNO_CUADRADO * self.col + TAMAGNO_CUADRADO // 2
        self.y = TAMAGNO_CUADRADO * self.fil + TAMAGNO_CUADRADO // 2
        #Esto se hace para calcular que la ficha se encuentre en el medio del cuadrado que se cree, y no en una esquina, o fuera de él.

    def make_king(self): #Cambia la variable de King.
        self.king = True #La pieza se vuelve King una vez que llega al final.
    
    def draw(self, win): #Esto dibuja la pieza.
        radio = TAMAGNO_CUADRADO//2 - self.RELLENO
        pygame.draw.circle(win, GRIS, (self.x, self.y), radio + self.BORDE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radio) #Se agrega el círculo con color, haciendo así que quede resaltado.
        if self.king:
            win.blit(CORONA, (self.x - CORONA.get_width()//2, self.y - CORONA.get_height()//2)) #Blit = Pone una imagen/superficie en la pantalla.

    def move(self, fil, col): #Método de movimiento.
        self.fil = fil
        self.col = col
        self.calc_pos()

    def __repr__(self): #Por si se necesita un debug, depurar.
        return str(self.color) #Representación interna del objeto. Evita el "<object at x>"
#______________________________________

#TABLERO / CASILLAS____________________
class Tablero: #Acá se declara el tablero. Maneja el movimiento de piezas, las elimina, las coloca en la pantalla, etc.
    def __init__(self): #Representación interna del tablero.
        self.tablero = [] #Se almacenan objetos en una lista bidimensional/matriz.
        self.ROJO_left = self.BLANCO_left = 12 #Cantidad de piezas de ambos colores.
        self.ROJO_kings = self.BLANCO_kings = 0
        self.crear_tablero()
    
    def draw_cuadrados(self, win): #Orden: rojo, blanco, rojo, blanco, rojo...
        win.fill(NEGRO)
        for fil in range(FILAS):
            for col in range(fil % 2, COLUMNAS, 2): #Esto crea el patrón del tablero.
                pygame.draw.rect(win, ROJO, (fil*TAMAGNO_CUADRADO, col *TAMAGNO_CUADRADO, TAMAGNO_CUADRADO, TAMAGNO_CUADRADO))
                #(fila, columna, ancho, alto)

    def move(self, pieza, fil, col): #Para mover la pieza, hay que borrarla de su lugar y crerla en el siguiente.
        self.tablero[pieza.fil][pieza.col], self.tablero[fil][col] = self.tablero[fil][col], self.tablero[pieza.fil][pieza.col]
        pieza.move(fil, col) #La pieza que está en la posición, y la posición a la que queremos mover la pieza. Se cambian los valores invirtiéndolos.

        if fil == FILAS - 1 or fil == 0: #Si la casilla es cero o siete para la fila, significa que estamos al principio o al final del tablero.
            pieza.make_king() #Si la pieza llega a la última fila, se va a convertir en una pieza King.
            if pieza.color == BLANCO:
                self.BLANCO_kings += 1
            else:
                self.ROJO_kings += 1 

    def get_pieza(self, fil, col): #Función que llama fila de tablero autodidacta.
        return self.tablero[fil][col]

    def crear_tablero(self): #Se crea la actual representación del tablero, donde se agregan piezas a la lista.
        for fil in range(FILAS):
            self.tablero.append([]) #Representa lo que va a haber dentro de cada posición en la lista.
            for col in range(COLUMNAS):
                if col % 2 == ((fil +  1) % 2): #¿Va a dibujar una pieza roja o blanca?
                    if fil < 3:
                        self.tablero[fil].append(Piezas(fil, col, BLANCO))
                    elif fil > 4:
                        self.tablero[fil].append(Piezas(fil, col, ROJO))
                    else:
                        self.tablero[fil].append(0) #Espacio vacío.
                else:
                    self.tablero[fil].append(0)
        
    def draw(self, win):
        self.draw_cuadrados(win) #Se dibujan todas las piezas y los cuadrados.
        for fil in range(FILAS):
            for col in range(COLUMNAS):
                pieza = self.tablero[fil][col]
                if pieza != 0:
                    pieza.draw(win)

    def eliminar(self, piezas):
        for pieza in piezas:
            self.tablero[pieza.fil][pieza.col] = 0
            if pieza != 0:
                if pieza.color == ROJO:
                    self.ROJO_left -= 1
                else:
                    self.BLANCO_left -= 1
    
    def ganador(self):
        if self.ROJO_left <= 0:
            return BLANCO
        elif self.BLANCO_left <= 0:
            return ROJO
        return None 
    
    def get_movimientos_validos(self, pieza):
        movimientos = {}
        izq = pieza.col - 1
        der = pieza.col + 1
        fil = pieza.fil

        if pieza.color == ROJO or pieza.king: #Verifico la dirección en la que se pueden mover las piezas.
            movimientos.update(self.atravezar_izq(fil -1, max(fil-3, -1), -1, pieza.color, izq))
            movimientos.update(self.atravezar_der(fil -1, max(fil-3, -1), -1, pieza.color, der))
            #Se actualizan los movimientos con lo que se devuelva de ahí.
        if pieza.color == BLANCO or pieza.king:
            movimientos.update(self.atravezar_izq(fil +1, min(fil+3, FILAS), 1, pieza.color, izq))
            movimientos.update(self.atravezar_der(fil +1, min(fil+3, FILAS), 1, pieza.color, der))
            #Se actualizan los movimientos con lo que se devuelva de ahí.
        return movimientos

    def atravezar_izq(self, start, stop, step, color, izq, skipped=[]):
        movimientos = {} #(donde se empieza, donde se para, cuánto debería pasar, el color que, queda, y si se salteó una pieza o no)
        last = []
        for f in range(start, stop, step): #F = Fila
            if izq < 0:
                break
            
            current = self.tablero[f][izq]
            if current == 0: #Hay un cuadrado vacío.
                if skipped and not last:
                    break #No hay lugar donde moverse.
                elif skipped: #Verificar si se ha saltado.
                    movimientos[(f, izq)] = last + skipped #Situación de salto.
                else: #Se agrega como posible movimiento a las otras casillas.
                    movimientos[(f, izq)] = last
                if last:
                    if step == -1:
                        fil = max(f-3, 0)
                    else:
                        fil = min(f+3, FILAS)
                    movimientos.update(self.atravezar_izq(f+step, fil, step, color, izq-1,skipped=last))
                    movimientos.update(self.atravezar_der(f+step, fil, step, color, izq+1,skipped=last))
                break
            elif current.color == color: #No me puedo mover a un lugar que está ocupado.
                break
            else:
                last = [current] #De ser el color contrario, podría moverse sobre él (asumiéndolo como 'vacío').
            izq -= 1
        return movimientos

    def atravezar_der(self, start, stop, step, color, der, skipped=[]):
        movimientos = {}
        last = [] 
        for f in range(start, stop, step): #F = Fila
            if der >= COLUMNAS:
                break
            
            current = self.tablero[f][der]
            if current == 0: #Hay un cuadrado vacío.
                if skipped and not last:
                    break #No hay lugar donde moverse.
                elif skipped: #Verificar si se ha saltado.
                    movimientos[(f,der)] = last + skipped #Situación de salto.
                else: #Se agrega como posible movimiento a las otras casillas.
                    movimientos[(f, der)] = last
                
                if last:
                    if step == -1:
                        fil = max(f-3, 0)
                    else:
                        fil = min(f+3, FILAS)
                    movimientos.update(self.atravezar_izq(f+step, fil, step, color, der-1,skipped=last))
                    movimientos.update(self.atravezar_der(f+step, fil, step, color, der+1,skipped=last))
                break
            elif current.color == color: #No me puedo mover a un lugar que está ocupado.
                break
            else:
                last = [current] #De ser el color contrario, podría moverse sobre él (asumiéndolo como 'vacío').
            der += 1
        return movimientos
#______________________________________

#MANEJO DEL JUEGO______________________
#¿De quién es el turno? ¿seleccioné una pieza? ¿puedo moverme a x lugar?
class Juego:
    def __init__(self, win):
        self._init() #Se puso en otra función ya que se utiliza casi lo mismo para el método de reinicio.
        self.win = win
    
    def update(self): #Update (actualización) de la pantalla del Pygame.
        self.tablero.draw(self.win)
        self.draw_movimientos_validos(self.movimientos_validos)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.tablero = Tablero()
        self.turn = ROJO
        self.movimientos_validos = {}

    def ganador(self):
        return self.tablero.ganador()

    def reset(self): #Método para reiniciar el juego.
        self._init()

    def select(self, fil, col):
        if self.selected:
            result = self._move(fil, col) #Se mueve lo seleccionado.
            if not result:
                self.selected = None
                self.select(fil, col)
        
        pieza = self.tablero.get_pieza(fil, col)
        if pieza != 0 and pieza.color == self.turn:
            self.selected = pieza
            self.movimientos_validos = self.tablero.get_movimientos_validos(pieza)
            return True   
        return False

    def _move(self, fil, col):
        pieza = self.tablero.get_pieza(fil, col)
        if self.selected and pieza == 0 and (fil, col) in self.movimientos_validos:
            self.tablero.move(self.selected, fil, col)
            skipped = self.movimientos_validos[(fil, col)]
            if skipped:
                self.tablero.eliminar(skipped)
            self.change_turn()
        else:
            return False
        return True

    def draw_movimientos_validos(self, movimientos):
        for move in movimientos:
            fil, col = move
            pygame.draw.circle(self.win, AZUL, (col * TAMAGNO_CUADRADO + TAMAGNO_CUADRADO//2, fil * TAMAGNO_CUADRADO + TAMAGNO_CUADRADO//2), 15)

    def change_turn(self):
        self.movimientos_validos = {}
        if self.turn == ROJO:
            self.turn = BLANCO
        else:
            self.turn = ROJO

#MAIN__________________________________
FPS = 60 #Se declaran los fotogramas por segundo/frames per second.
#Los FPS no se encuentran en el módulo de constantes, ya que es un dato específico para renderizar y darle forma al juego.

WIN = pygame.display.set_mode((ANCHO, ALTURA))
#WIN = Valor constante (conjunto de puntos de visualización). Se elige el ancho y altura.
pygame.display.set_caption('DAMAS - PILAR PLUMMER') #Nombre del juego.

def get_fil_col_from_mouse(pos): #Se toma la posición del mouse.
    x, y = pos #Se calcula en que fila y columna nos encontramos.
    fil = y // TAMAGNO_CUADRADO #Si el TC es 100, y quiero averiguar en qué fila estoy, 'y' está en 650, por ende estoy en la fila 6.
    col = x // TAMAGNO_CUADRADO #Se hace lo mismo con la posición en x de la columna.
    return fil, col

def main(): #Defino la función principal para ejecutar el juego.
    run = True #Se crea el "bucle de eventos".
    clock = pygame.time.Clock() #El reloj se asegura de que el bucle no se ejecute ni demasiado rápido o demasiado lento.
    game = Juego(WIN)

    while run:
        clock.tick(FPS)

        if game.ganador() != None:
            print(game.ganador())
            run = False

        for event in pygame.event.get(): #El punto de evento consigue comprobar qué es lo que está sucediendo en el juego.
            if event.type == pygame.QUIT: #Se da la opción de cerrar el juego.
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: #Esto quiere decir que presioné una tecla del mouse.
                #Esto responde a: ¿me estoy moviendo?, ¿toqué una pieza roja?, ¿de quién es el turno?, entre otros.
                pos = pygame.mouse.get_pos()
                fil, col = get_fil_col_from_mouse(pos)
                game.select(fil, col)
        game.update() #game.update
    pygame.quit()
main()
