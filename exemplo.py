import numpy as np
import glob
from numba import jit #isso e usado em funcoes e faz o codigo rodar mais rapido.
from astropy.io import fits


datapath = '/home2/matheus13/Projeto1/ImagensTeste/' #caminho da localização das imagens fits.


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
def corrSci(lista_sci, lista_bias, masterbias, masterflat):
    '''Essa funcao corrige as imagens de ciencia'''
    sci_flatbias = [] #criando lista vazia para colocar as imagens de ciencia corrigidas.
    for i in lista_sci:
       img,hdr = fits.getdata(i, header = True) #abrindo as imagens de ciencia.
       img = img.astype(np.float64) #transformando os elementos "string" em elementos numericos.
       j = (img - masterbias)/masterflat #corrigindo as imagens de ciencia.
       sci_flatbias.append(j) #introduzindo as imagens de ciencia na lista vazia.
    return sci_flatbias


#Criando as listas com os dados:

lista_bias = glob.glob(datapath+'bias*.fits') #criando uma lista contendo todas as imagens bias.
lista_flat = glob.glob(datapath+'flat*.fits') #criando uma lista contendo todas as imagens flat.
lista_sci = glob.glob(datapath+'xo2b*.fits') #criando uma lista contendo todas as imagens de ciência.


#Rodando as funcoes do codigo e printando a lista de matrizes das imagens de ciencia corrigidas de bias e de flat:

masterbias = masterBias(lista_bias)
flat_bias = corrFlat(lista_flat, masterbias)
masterflat = masterFlat(flat_bias)
sci_flatbias = corrSci(lista_sci, lista_bias, masterbias, masterflat)
#print(sci_flatbias)


#Testes estatisticos para o Master Bias e Master Flat:

a = np.mean(masterbias, axis=0) #Tirando a média do Master Bias.

b = np.mean(masterflat, axis=0) #Tirando a média do Master Flat.

if 0 < a.all() < 30: #A média do Master Bias deve estar dentro desse intervalo para ser considerado um resultado aceitável. 
 print("Master Bias: passou no teste!")
else:
 print ("Master Bias: nao passou no teste...")

if 0 < b.all() < 2: #A média do Master Flat deve estar dentro desse intervalo para ser considerado um resultado aceitável. 
 print ("Master Flat: passou no teste!")
else:
 print ("Master Flat: nao passou no teste...")


#Salvando o output do codigo em um arquivo .fits:

outfile = 'pipeline.fits' #nome do arquivo que sera criado.

for i in range(len(sci_flatbias)):
    hdu = fits.PrimaryHDU() #criando o HDU 
    hdu.data = sci_flatbias[i] #adicionando a matriz numerica.
    hdr = fits.getheader(lista_sci[i]) #lendo os headers das imagens de ciencia originais.
    hdu.header = hdr #adicionando a tabela de informacoes.
    hdu.header['BIAS_RED'] = 'True' #acrescentando header BIAS_REDUCTION na tabela de informacoes.
    hdu.header.comments['BIAS_RED'] = 'Reducao Bias'
    hdu.header['FLAT_RED'] = 'True' #acrescentando header FLAT_REDUCTION na tabela de informacoes.
    hdu.header.comments['FLAT_RED'] = 'Reducao Flat'
    hdu.writeto(str(i)+outfile)










