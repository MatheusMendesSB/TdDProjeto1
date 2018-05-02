import numpy as np
import glob
from numba import jit #isso e usado em funcoes e vai fazer o codigo rodar mais rapido.
from astropy.io import fits


datapath = input('Qual e o caminho da localizacao das imagens?\n') #Este codigo comeca pedindo a localizacao das imagens.
sci = input('Digite o nome que aparece em suas imagens de ciencia:\n') #O usuario tambem precisa especificar o nome usado para identificar suas imagens de ciencia.


@jit
def masterBias(lista_bias):
    '''Essa funcao cria o Master Bias que sera usado na correcao das imagens de ciencia'''
    nlista_bias = [] #criando lista vazia para colocar os bias em caracteres numericos
    for i in lista_bias: 
       img,hdr = fits.getdata(i, header = True) #abrindo as imagens de bias.
       img = img.astype(np.float64) #transformando os elementos "string" em elementos numericos.
       nlista_bias.append(img) #introduzindo os bias em caracteres numericos na lista vazia.
    masterbias = np.median(nlista_bias,axis=0) #Criando o Master Bias, axis=0 calcula a mediana pixel a pixel.
    return masterbias

@jit
def corrFlat(lista_flat, masterbias):
    '''Essa funcao corrige o flat'''
    nlista_flat = [] #criando lista vazia para colocar os flat em caracteres numericos.
    flat_bias = [] #criando lista vazia para colocar os flat corrigidos do bias.
    for i in lista_flat:
       img,hdr = fits.getdata(i, header = True) #abrindo as imagens de flat.
       img = img.astype(np.float64) #transformando os elementos "string" em elementos numericos.
       nlista_flat.append(img) #introduzindo os flat em caracteres numericos na lista vazia.
    for i in nlista_flat:
       j = i - masterbias #corrigindo os flat.
       flat_bias.append(j) #introduzindo os flat corrigidos na lista vazia
    return flat_bias

@jit
def masterFlat(flat_bias):
    '''Essa funcao cria o Master Flat que sera usado na correcao das imagens de ciencia e na correcao do bias'''
    mediaflat = np.mean(flat_bias,axis=0) #criando uma matriz com a média entre os flat.
    for i in flat_bias:
       j = i/mediaflat #normalizando os flat corrigidos.
       masterflat = np.median(flat_bias,axis=0) #Criando o master flat.
       return masterflat

@jit
def sciBias(lista_sci, masterbias):
    '''Essa funcao corrige as imagens de ciencia do bias'''
    sci_bias = [] #criando lista vazia para colocar as imagens de ciencia corrigidas do bias.
    nlista_sci = [] #criando lista vazia para colocar as imagens de ciencia em caracteres numericos.
    for i in lista_sci: 
       img,hdr = fits.getdata(i, header = True) #abrindo as imagens de ciencia.
       img = img.astype(np.float64) #transformando os elementos "string" em elementos numericos.
       nlista_sci.append(img) #introduzindo as imagens de ciencia em caracteres numericos na lista vazia.
    for i in nlista_sci:
       j = i - masterbias #corrigindo as imagens de ciencia do bias.
       sci_bias.append(j) #introduzindo as imagens de ciencia corrigidas na lista vazia.
       return sci_bias

@jit
def sciFlat(sci_bias, masterflat):
    sci_flat = [] #criando lista vazia para colocar as imagens de ciencia corrigidas do flat.
    '''Essa funcao corrige as imagens de ciencia do flat'''
    for i in sci_bias:
       j = i/masterflat #corrigindo as imagens de ciencia do flat.
       sci_flat.append(j) #introduzindo as imagens de ciencia corrigidas na lista vazia.
       return sci_flat    
       

lista_bias = glob.glob(datapath+'bias*.fits') #criando uma lista contendo todas as imagens bias.
lista_flat = glob.glob(datapath+'flat*.fits') #criando uma lista contendo todas as imagens flat.
lista_sci = glob.glob(datapath+sci+'*.fits') #criando uma lista contendo todas as imagens de ciência.


masterbias = masterBias(lista_bias)
flat_bias = corrFlat(lista_flat, masterbias)
masterflat = masterFlat(flat_bias)
sci_bias = sciBias(lista_sci, masterbias)
sci_flat = sciFlat(sci_bias, masterflat)
print(sci_flat)











   








