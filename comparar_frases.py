# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:14:47 2022

Compara dos textos y devuelve cuan parecido son.


@author: Pablo
"""
#%%
from fuzzywuzzy import fuzz

def validar(a):
    """ 
    La función validar sirve para colocar unos principios de si es comparable el dato
    Devuelve verdader en caso de que sea válido
    """
    a_ = a.strip().replace(' ','')
    if len(a_) < 3:
        return False
    else:
        return True
    
def control_texto( frase1, frase2,validar = validar):
    """ Validar es una función que determina si una frase es válida
    frase1 y frase2 son las dos frases que se quieren comparar"""
    
    
    #coincidencias = []
    #for i in range(len(frase1)):
    a = frase1.upper().strip()
    b = frase2.upper().strip()
        
    if validar(a) and validar(b):
        if a == b:
            coinc = 1
            
        else:
            coinc = 0
            aa = a.replace('_',' ').replace('-',' ').split()
            bb = b.replace('_',' ').replace('-',' ').split()
            res1 = 1 if len(aa) == len(bb) else 0
            res2 = len(set(aa).intersection(set(bb))) /len(set(aa).union(set(bb)))
            coinc = (res1*0.01+res2*0.99)
            
            if res2 < 1:
                a_dif = list(set(aa).difference(set(bb)))
                b_dif = list(set(bb).difference(set(aa)))
                #res1_ = 1 if len(a_dif) == len(b_dif) else 0
                if len(a_dif) == 0 or len(b_dif) == 0:
                    res2_ = 1
                else:
                    a_dif_ = []
                    for j in a_dif:
                        a_dif_.extend(list(j))
                    b_dif_ = []
                    for j in b_dif:
                        b_dif_.extend(list(j))
                    res2_ = len(set(a_dif_).intersection(set(b_dif_)))/len(set(a_dif_).union(set(b_dif_)))
                coinc += (1-res2)*(res2_)
    else:
        coinc = 0
    #coincidencias.append(coinc)

    return coinc

def control_texto_2( frase1, frase2):
    """ Validar es una función que determina si una frase es válida
    frase1 y frase2 son las dos frases que se quieren comparar"""
    
    a = frase1.upper().strip()
    b = frase2.upper().strip()
    if a == b:
        coinc = 100
            
    else:
        coinc = fuzz.ratio(a, b)
            
    return coinc

def buscar_frase(frase, lista, *args, **kwargs):
    """Compara una frase en una lista de frases y compara con cada una """
    
    n = len(lista)
    coincidencias = []
    for i in range(n):
        v = control_texto_2(frase, lista[i], *args, **kwargs)
        coincidencias.append(v)
        
    return coincidencias
    


#%%

f1 = "Pablo va a la esquina"
f2 = "Pablo va la esquina"
f3 = "uh!! que frio"
f4 = "Pablo no fue a la esquina"

l = [f3,f4,f1,f2]
control_texto(f1,f2)
print(buscar_frase(f1,l))






# %%
