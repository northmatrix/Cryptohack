import fastecdsa
from fastecdsa.point import Point
from fastecdsa.curve import P256

print("START")
G = P256.G
print(G.x)
print(G.y)
print("G DEFINED")
Nme = 5214
print("X DEFINED")
x = Nme * G
print("FINISHED")
print(hex(x.x))
print((x.y))
