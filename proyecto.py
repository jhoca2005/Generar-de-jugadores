# Importaciones necesarias para crear la aplicación web y utilizar funciones aleatorias
from flask import Flask, render_template, request
import random

# Inicialización de la aplicación Flask. Esto crea una instancia de la aplicación.
app = Flask(__name__)

# Lista de jugadores por posición (genes), estructura que almacena los posibles genes
# Además de los nombres, ahora cada jugador tendrá habilidades asignadas de manera aleatoria.
jugadores = {
    'portero': ['Alisson', 'Manuel Neuer', 'Marc-André ter Stegen', 'Éderson', 'Jan Oblak'],
    'defensa1': ['Virgil Van Dijk', 'Marquinhos', 'David Alaba', 'Eder Militao', 'Kalidou Koulibaly'],
    'defensa2': ['De Ligt', 'Antonio Rüdiger', 'Ronald Araújo', 'Rúben Dias', 'Daniel Muñoz'],
    'mediocampista': ['Luka Modric', 'Ngolo Kanté', 'Toni Kroos', 'Jude Bellingham', 'Rodri'],
    'delantero': ['Kylian Mbappé', 'Erling Haaland', 'Vinícius Júnior', 'Harry Kane', 'Luis Diaz'],
}

# Función para asignar habilidades a cada jugador
def asignar_habilidades():
    return {
        'Agilidad': random.randint(50, 100),
        'Velocidad': random.randint(50, 100),
        'Técnica': random.randint(50, 100),
        'Mentalidad': random.randint(50, 100),
        'Precisión en los pases': random.randint(50, 100),
        'Control de balón': random.randint(50, 100)
    }

# Cada jugador tendrá un conjunto de habilidades asignadas
jugadores_habilidades = {pos: {jug: asignar_habilidades() for jug in lista} for pos, lista in jugadores.items()}

# Función de aptitud (fitness) que evalúa la calidad de un equipo
# Suma la puntuación de cada habilidad de cada jugador para obtener un valor de aptitud total
def fitness(equipo):
    puntuacion_total = 0
    for jugador in equipo:
        habilidades = jugadores_habilidades[jugador[1]][jugador[0]]  # Obtiene las habilidades del jugador
        puntuacion_total += sum(habilidades.values())  # Suma todas las habilidades del jugador
    return puntuacion_total

# Genera un cromosoma (equipo) seleccionando aleatoriamente un jugador de cada posición
# Los cromosomas aquí son equipos de fútbol, compuestos por jugadores con habilidades.
def generar_cromosoma():
    cromosoma = [
        (random.choice(jugadores['portero']), 'portero'),
        (random.choice(jugadores['defensa1']), 'defensa1'),
        (random.choice(jugadores['defensa2']), 'defensa2'),
        (random.choice(jugadores['mediocampista']), 'mediocampista'),
        (random.choice(jugadores['delantero']), 'delantero')
    ]
    return cromosoma

# Genera una población inicial (conjunto de equipos)
def generar_equipo(tamano_equipo):
    return [generar_cromosoma() for _ in range(tamano_equipo)]

# Selección por torneo: selecciona 3 equipos aleatorios y elige el mejor (con mayor fitness)
def seleccion(equipo):
    torneo = random.sample(equipo, 3)
    torneo.sort(key=fitness, reverse=True)
    return torneo[0]

# Cruce (crossover) entre dos equipos (cromosomas)
def cruce(cromosoma1, cromosoma2):
    punto_cruce = random.randint(1, len(cromosoma1) - 1)
    hijo1 = cromosoma1[:punto_cruce] + cromosoma2[punto_cruce:]
    hijo2 = cromosoma2[:punto_cruce] + cromosoma1[punto_cruce:]
    return hijo1, hijo2

# Mutación de un cromosoma (equipo)
def mutacion(cromosoma, probabilidad_mutacion):
    for i in range(len(cromosoma)):
        if random.random() < probabilidad_mutacion:
            if cromosoma[i][1] == 'portero':
                cromosoma[i] = (random.choice(jugadores['portero']), 'portero')
            elif cromosoma[i][1] == 'defensa1':
                cromosoma[i] = (random.choice(jugadores['defensa1']), 'defensa1')
            elif cromosoma[i][1] == 'defensa2':
                cromosoma[i] = (random.choice(jugadores['defensa2']), 'defensa2')
            elif cromosoma[i][1] == 'mediocampista':
                cromosoma[i] = (random.choice(jugadores['mediocampista']), 'mediocampista')
            elif cromosoma[i][1] == 'delantero':
                cromosoma[i] = (random.choice(jugadores['delantero']), 'delantero')
    return cromosoma

# Algoritmo genético principal
def algoritmo_genetico(tamano_equipo, generaciones, prob_mutacion):
    equipo = generar_equipo(tamano_equipo)
    for _ in range(generaciones):
        nuevo_equipo = []
        while len(nuevo_equipo) < tamano_equipo:
            padre1 = seleccion(equipo)
            padre2 = seleccion(equipo)
            hijo1, hijo2 = cruce(padre1, padre2)
            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            nuevo_equipo.extend([hijo1, hijo2])
        equipo = nuevo_equipo[:tamano_equipo]
    mejor_equipo = max(equipo, key=fitness)
    return mejor_equipo

# Ruta de la aplicación Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mejor_equipo', methods=['POST'])
def mejor_equipo():
    mejor_equipo = algoritmo_genetico(6, 10, 0.05)
    return render_template('equipo.html', equipo=mejor_equipo, habilidades=jugadores_habilidades)

if __name__ == '__main__':
    app.run(debug=True)

