import turtle
import time

# Configuration de la fenêtre
screen = turtle.Screen()
screen.bgcolor("#0B0D17") # Bleu nuit profond
screen.title("Constellation du Papillon")

t = turtle.Turtle()
t.hideturtle()
t.speed(2)
t.color("white")

# Liste de tuples (x, y) pour le corps et les ailes
# On définit un côté, l'autre sera déduit par symétrie
etoiles = [
    (0, 0),    # Centre
    (0, 100),  # Tête
    (0, -100), # Queue
    (80, 120), # Sommet aile droite
    (120, 0),  # Pointe aile droite
    (80, -80), # Bas aile droite
    (-80, 120),# Sommet aile gauche
    (-120, 0), # Pointe aile gauche
    (-80, -80) # Bas aile gauche
]

# 1. Dessiner les étoiles
for pos in etoiles:
    t.penup()
    t.goto(pos)
    t.pendown()
    t.dot(8, "#FFD700") # Étoiles dorées

# 2. Relier pour former le papillon (Le tracé)
def relier_etoiles(p1, p2):
    t.penup()
    t.goto(etoiles[p1])
    t.pendown()
    t.goto(etoiles[p2])

t.pensize(1)
t.color("#5DADE2") # Couleur des liens célestes

# Tracé du corps
relier_etoiles(1, 0)
relier_etoiles(0, 2)

# Tracé aile droite
relier_etoiles(1, 3)
relier_etoiles(3, 4)
relier_etoiles(4, 5)
relier_etoiles(5, 0)

# Tracé aile gauche
relier_etoiles(1, 6)
relier_etoiles(6, 7)
relier_etoiles(7, 8)
relier_etoiles(8, 0)

# Effet dynamique : scintillement final
while True:
    t.color("white")
    for pos in etoiles:
        t.penup()
        t.goto(pos)
        t.dot(10)
    time.sleep(0.5)
    for pos in etoiles:
        t.penup()
        t.goto(pos)
        t.dot(10, "#FFD700")
    time.sleep(0.5)

screen.mainloop()
