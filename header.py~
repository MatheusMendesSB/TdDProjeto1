import numpy as np
import glob
from numba import jit 
from astropy.io import fits

datapath = '/home2/matheus13/Projeto1/xo2b/' #caminho da localização das imagens fits.

lista_sci = glob.glob(datapath+'xo2b*.fits') #criando uma lista contendo todas as imagens de ciência.

hdr = fits.getheader(lista_sci[0])
print(hdr)
