#!/usr/bin/env python
# coding: utf-8

# In[103]:



import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

imagem = cv2.imread("goku-jr.jpg")
imagem2 = imagem
tamanho_completa = (100,100)
tamanho_parcial = (25,25)
#bloco = int((tamanho_completa[0]/tamanho_parcial[0])*(tamanho_completa[1]/tamanho_parcial[1]))


# In[104]:


for i in imagem2:
    for j in i:
        a = int(sum(j)/3)
        if (j[2] > 190 and j[1]>80 and j[1]<220 and j[0]>30 and j[0]<170):
            j[0] = 255
            j[1] = 0
            j[2] = 0
        else:
            j[0] = 255
            j[1] = 255
            j[2] = 255


# In[105]:


cv2.imwrite("teste_cinza1.jpg",imagem2)


# In[8]:


lista = []
for i in imagem:
    for a in i:
        b = int(sum(a)/3)
        lista.append(b)


# In[11]:


seting = set(lista)


# In[12]:


chamado = {i:lista.count(i) for i in seting}


# In[15]:


pixel = []
j = list(seting)
for i in seting:
    pixel.append(lista.count(i))


# In[17]:


plt.figure(figsize=(12,10))
plt.bar(j,pixel)


# In[19]:


plt.show(imagem)


# In[21]:


for i in imagem:
    for a in i:
        print(a)
        b = int(sum(a)/3)
        print(b)
        for i in a


# In[ ]:




