# This is for a Weistersass curve of the form 
# Y^2 = X^3 + aX + b mod p 

a = 2
b = 3
p = 310717010502520989590157367261876774703 


# Generator point 
G_x = 179210853392303317793440285562762725654
G_y = 105268671499942631758568591033409611165

# Bobs public key
Qb_x = 272640099140026426377756188075937988094 
Qb_y = 51062462309521034358726608268084433317

# Senders public key 
Qs_x = 280810182131414898730378982766101210916
Qs_y = 291506490768054478159835604632710368904

# Now lets write some sage code to solve this 
F = GF(p) # define the fininte field 
E = EllipticCurve(F,[a,b]) # define the elliptic curve
G = E(G_x,G_y) # define generator
Qb = E(Qb_x,Qb_y) # define bobs public key
Qs = E(Qs_x,Qs_y) # define senders public key

n = discrete_log(Qs,G,operation='+')
print("N: ", n)


