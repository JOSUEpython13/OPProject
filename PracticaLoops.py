'''
while loops: execute until some condition is met
for loops: iterate through an object a certain number of times.

WHILE
while condition1: statement



'''
'''
answer = input(f"Quieres jugar un juego? (y/n)")
while not (answer == "y" or answer == "n"):
    print(f"Respuesta Invalida. Tiene que ingresar un 'y' o un 'n'")
    answer = input(f"Quieres jugar un juego? (y/n)")


answer = input(f"Ingrese una palabra")
value = 0
for l in answer:
    value += 1

print(f"La plabra tiene {value} letras")
'''







