import numpy as np
import matplotlib.pyplot as plt

def f(x):
    d = -2 *x + 7
    return d

def afficherDichotomie(a,b,e):
    debut = a
    fin = b
    ecart = np.sqrt((b-a)**2)
    n = 0
    lst1=[]
    while ecart>e:
        m = (debut+fin)/2
        if f(m)*f(a)<0:
            fin = m
        else:
            debut = m
            ecart = fin-debut
        lst1.append(m)
        n+=1
    lst = [lst1,n]
    return lst


l = afficherDichotomie(-10,12,10**(-5))
print(l)
xs = np.arange(0, l[1], 1)

ys = l[0]
plt.xlabel("itérations")
plt.ylabel("tirant d'eau")
plt.plot(xs, ys)


plt.show()


