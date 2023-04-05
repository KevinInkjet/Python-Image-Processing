from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog
import os
from os import remove
from os import path
from urllib.request import *
from functools import partial
import linecache
from automata.base.automaton import Automaton
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from tkinter import Tk, Canvas
from PIL import ImageTk, Image
from PIL import Image, ImageFont
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as mpimg
from skimage import io
import cv2
from math import log

def cargar():
    global gris
    gris = False
    print("Cargar")
    file = filedialog.askopenfilename()
    im = Image.open(file)
    im = im.resize((320, 180), Image.ANTIALIAS)
    canvas.image = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')
    image = cv2.imread(os.path.abspath(file), cv2.IMREAD_COLOR)
    cv2.imwrite('current.jpg', image)

def cargargris():
    global gris
    gris = True
    print("Cargar")
    file = filedialog.askopenfilename()
    image = cv2.imread(os.path.abspath(file), cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('current.jpg', image)
    im = Image.open("current.jpg")
    im = im.resize((320, 180), Image.ANTIALIAS)
    canvas.image = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

def invertir():
    print("Invertir")

    rise = Toplevel()
    rise.title("Inversión")
    rise.geometry("320x250")

    txtnom = Entry(rise, width=25) # Crea un campo de entrada de datos
    txtnom.grid(column=1, row=0) # Posiciona la entrada de texto
    txtnom.insert(END, "edit.jpg")

    canvasres = Canvas(rise, width=320, height=180)
    canvasres.grid(column=1, row=2)
    
    img1 = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
    #gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    q = 255 - img1
    cv2.imwrite("edit.jpg", q)

    im = Image.open("edit.jpg")
    im = im.resize((320, 180), Image.ANTIALIAS)
    canvasres.image = ImageTk.PhotoImage(im)
    canvasres.create_image(0, 0, image=canvasres.image, anchor='nw')

    def descargainv(txtnom):
        image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
        cv2.imwrite(txtnom, image)
        print("descargada")
        rise.destroy()
        rise.update()

    btn_descargainv = Button(rise, text="Descargar", command=lambda: descargainv(str(txtnom.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_descargainv.grid(column=1, row=30) # Posiciona el botón

    return

def umbral():

    rise2 = Toplevel()
    rise2.title("Umbral")
    rise2.geometry("230x150")

    lblespacio = Label(rise2, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio.grid(column=0, row=0) # Posiciona la etiqueta

    lbl = Label(rise2, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl.grid(column=1, row=1) # Posiciona la etiqueta

    txtt = Entry(rise2, width=25) # Crea un campo de entrada de datos
    txtt.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbral(t):

        rise2.destroy()
        rise2.update()

        rise3 = Toplevel()
        rise3.title("Umbral")
        rise3.geometry("320x250")

        int(t)

        p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)

        q = p
        idx = p <= t 
        q[idx] = 0
        idx = p > t
        q[idx] = 255

        cv2.imwrite("edit.jpg", q)

        txtnomum = Entry(rise3, width=25) # Crea un campo de entrada de datos
        txtnomum.grid(column=1, row=0) # Posiciona la entrada de texto ppersona 5
        txtnomum.insert(END, "edit.jpg")

        canvasum = Canvas(rise3, width=320, height=180)
        canvasum.grid(column=1, row=2)

        im = Image.open("edit.jpg")
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvasum.image = ImageTk.PhotoImage(im)
        canvasum.create_image(0, 0, image=canvasum.image, anchor='nw')

        def descargainv(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise3.destroy()
            rise3.update()

        btn_descargaum = Button(rise3, text="Descargar", command=lambda: descargainv(str(txtnomum.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptar = Button(rise2, text="Ok", command=lambda: funcionumbral(int(txtt.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar.grid(column="1", row="3") # Posiciona el botón

def umbralinv():

    global gris

    rise4 = Toplevel()
    rise4.title("Umbral Invertido")
    rise4.geometry("230x150")

    lblespacio2 = Label(rise4, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio2.grid(column=0, row=0) # Posiciona la etiqueta

    lbl2 = Label(rise4, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl2.grid(column=1, row=1) # Posiciona la etiqueta

    txtt2 = Entry(rise4, width=25) # Crea un campo de entrada de datos
    txtt2.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbral2(t):

        rise4.destroy()
        rise4.update()

        rise5 = Toplevel()
        rise5.title("Umbral Invertido")
        rise5.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (p[row,col]) <= t:
                        q[row,col] = 255
                    else:
                        q[row,col] = 0
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (p[row,col,color]) <= t:
                            q[row,col,color] = 255
                        else:
                            q[row,col,color] = 0
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomum2 = Entry(rise5, width=25) # Crea un campo de entrada de datos
        txtnomum2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum2.insert(END, "edit.jpg")

        canvasum2 = Canvas(rise5, width=320, height=180)
        canvasum2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvasum2.image = ImageTk.PhotoImage(im2)
        canvasum2.create_image(0, 0, image=canvasum2.image, anchor='nw')

        def descargainv2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise5.destroy()
            rise5.update()

        btn_descargaum2 = Button(rise5, text="Descargar", command=lambda: descargainv2(str(txtnomum2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum2.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptar2 = Button(rise4, text="Ok", command=lambda: funcionumbral2(int(txtt2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar2.grid(column="1", row="3") # Posiciona el botón

def umbralbin():
    global gris
    print("Umbral binario")

    rise6 = Toplevel()
    rise6.title("Umbral Binario")
    rise6.geometry("230x150")

    lblespacio3 = Label(rise6, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio3.grid(column=0, row=0) # Posiciona la etiqueta

    lbl3 = Label(rise6, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl3.grid(column=1, row=1) # Posiciona la etiqueta

    txtt3 = Entry(rise6, width=25) # Crea un campo de entrada de datos
    txtt3.grid(column=1, row=2) # Posiciona la entrada de texto

    lbl32 = Label(rise6, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl32.grid(column=1, row=3) # Posiciona la etiqueta

    txtt32 = Entry(rise6, width=25) # Crea un campo de entrada de datos
    txtt32.grid(column=1, row=4) # Posiciona la entrada de texto

    def funcionumbral3(t1, t2):

        rise6.destroy()
        rise6.update()

        rise7 = Toplevel()
        rise7.title("Umbral Binario")
        rise7.geometry("320x250")

        if t1 < t2:
            tuno = t1
            tdos = t2
        else:
            tuno = t2
            tdos = t1

        int(t)

        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (int(p[row,col]) < tuno) or (int(p[row,col] > tdos)):
                        q[row,col] = 255
                    else:
                        q[row,col] = 0
            img = q
        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (int(p[row,col,color]) < tuno) or (int(p[row,col,color] > tdos)):
                            q[row,col,color] = 255
                        else:
                            q[row,col,color] = 0
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", q)

        txtnomum = Entry(rise7, width=25) # Crea un campo de entrada de datos
        txtnomum.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum.insert(END, "edit.jpg")

        canvasum = Canvas(rise7, width=320, height=180)
        canvasum.grid(column=1, row=2)

        im = Image.open("edit.jpg")
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvasum.image = ImageTk.PhotoImage(im)
        canvasum.create_image(0, 0, image=canvasum.image, anchor='nw')

        def descargainv3(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise7.destroy()
            rise7.update()

        btn_descargaum3 = Button(rise7, text="Descargar", command=lambda: descargainv3(str(txtnomum.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum3.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150
    #u = 2

    #lista = []
    #lista.append(txtt3)
    #lista.append(txtt32)

    btn_aceptar3 = Button(rise6, text="Ok", command=lambda: funcionumbral3(int(txtt3.get()), int(txtt32.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar3.grid(column="1", row="5") # Posiciona el botón

def umbralbininv():
    global gris
    print("Umbral bin inv")
    print("Umbral binario")

    rise8 = Toplevel()
    rise8.title("Umbral Binario Invertido")
    rise8.geometry("230x150")

    lblespacio4 = Label(rise8, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio4.grid(column=0, row=0) # Posiciona la etiqueta

    lbl4 = Label(rise8, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl4.grid(column=1, row=1) # Posiciona la etiqueta

    txtt42 = Entry(rise8, width=25) # Crea un campo de entrada de datos
    txtt42.grid(column=1, row=2) # Posiciona la entrada de texto

    lbl322 = Label(rise8, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl322.grid(column=1, row=3) # Posiciona la etiqueta

    txtt322 = Entry(rise8, width=25) # Crea un campo de entrada de datos
    txtt322.grid(column=1, row=4) # Posiciona la entrada de texto

    def funcionumbral4(t1, t2):

        rise8.destroy()
        rise8.update()

        rise9 = Toplevel()
        rise9.title("Umbral Binario Invertido")
        rise9.geometry("320x250")

        if t1 < t2:
            tuno = t1
            tdos = t2
        else:
            tuno = t2
            tdos = t1

        int(t)

        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (int(p[row,col]) < tuno):
                        q[row,col] = 0
                    elif ((int(p[row,col]) >= tuno) and (int(p[row,col]) <= tdos)):
                        q[row,col] = 255
                    else:
                        q[row,col] = 0
            img = q
        else:
            q = p
            #for color in range(0,2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (int(p[row,col,color]) < tuno):
                            q[row,col,color] = 0
                        elif ((int(p[row,col,color]) >= tuno) and (int(p[row,col,color]) <= tdos)):
                            q[row,col,color] = 255
                        else:
                            q[row,col,color] = 0
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", q)

        txtnomum3 = Entry(rise9, width=25) # Crea un campo de entrada de datos
        txtnomum3.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum3.insert(END, "edit.jpg")

        canvasum3 = Canvas(rise9, width=320, height=180)
        canvasum3.grid(column=1, row=2)

        im3 = Image.open("edit.jpg")
        im3 = im3.resize((320, 180), Image.ANTIALIAS)
        canvasum3.image = ImageTk.PhotoImage(im3)
        canvasum3.create_image(0, 0, image=canvasum3.image, anchor='nw')

        def descargainv4(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise9.destroy()
            rise9.update()

        btn_descargaum4 = Button(rise9, text="Descargar", command=lambda: descargainv4(str(txtnomum3.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum4.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150
    #u = 2

    #lista = []
    #lista.append(txtt3)
    #lista.append(txtt32)

    btn_aceptar4 = Button(rise8, text="Ok", command=lambda: funcionumbral4(int(txtt322.get()), int(txtt42.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar4.grid(column="1", row="5") # Posiciona el botón

def umbralgray():
    global gris
    print("Umbral escala de grises")

    rise10 = Toplevel()
    rise10.title("Umbral escala de grises")
    rise10.geometry("230x150")

    lblespacio5 = Label(rise10, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio5.grid(column=0, row=0) # Posiciona la etiqueta

    lbl5 = Label(rise10, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl5.grid(column=1, row=1) # Posiciona la etiqueta

    txtt45 = Entry(rise10, width=25) # Crea un campo de entrada de datos
    txtt45.grid(column=1, row=2) # Posiciona la entrada de texto

    lbl35 = Label(rise10, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl35.grid(column=1, row=3) # Posiciona la etiqueta

    txtt35 = Entry(rise10, width=25) # Crea un campo de entrada de datos
    txtt35.grid(column=1, row=4) # Posiciona la entrada de texto

    def funcionumbral5(t1, t2):

        rise10.destroy()
        rise10.update()

        rise11 = Toplevel()
        rise11.title("Umbral de la escala de grises")
        rise11.geometry("320x250")

        if t1 < t2:
            tuno = t1
            tdos = t2
        else:
            tuno = t2
            tdos = t1

        int(t)

        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (int(p[row,col]) <= tuno):
                        q[row,col] = 255
                    elif ((int(p[row,col]) > tuno) and (int(p[row,col]) < tdos)):
                        q[row,col] = p[row,col]
                    else:
                        q[row,col] = 255
            img = q
        else:
            q = p
            #for color in range(0,2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (int(p[row,col,color]) <= tuno):
                            q[row,col,color] = 255
                        elif ((int(p[row,col,color]) > tuno) and (int(p[row,col,color]) < tdos)):
                            q[row,col,color] = p[row,col,color]
                        else:
                            q[row,col,color] = 255
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", q)

        txtnomum5 = Entry(rise11, width=25) # Crea un campo de entrada de datos
        txtnomum5.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum5.insert(END, "edit.jpg")

        canvasum5 = Canvas(rise11, width=320, height=180)
        canvasum5.grid(column=1, row=2)

        im5 = Image.open("edit.jpg")
        im5 = im5.resize((320, 180), Image.ANTIALIAS)
        canvasum5.image = ImageTk.PhotoImage(im5)
        canvasum5.create_image(0, 0, image=canvasum5.image, anchor='nw')

        def descargainv5(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise11.destroy()
            rise11.update()

        btn_descargaum5 = Button(rise11, text="Descargar", command=lambda: descargainv5(str(txtnomum5.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum5.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150
    #u = 2

    #lista = []
    #lista.append(txtt3)
    #lista.append(txtt32)

    btn_aceptar5 = Button(rise10, text="Ok", command=lambda: funcionumbral5(int(txtt35.get()), int(txtt45.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar5.grid(column="1", row="5") # Posiciona el botón

def umbralgrayinv():
    global gris
    print("Umbral escala de grises invertido")

    rise12 = Toplevel()
    rise12.title("Umbral escala de grises invertido")
    rise12.geometry("230x150")

    lblespacio6 = Label(rise12, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio6.grid(column=0, row=0) # Posiciona la etiqueta

    lbl6 = Label(rise12, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl6.grid(column=1, row=1) # Posiciona la etiqueta

    txtt46 = Entry(rise12, width=25) # Crea un campo de entrada de datos
    txtt46.grid(column=1, row=2) # Posiciona la entrada de texto

    lbl36 = Label(rise12, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl36.grid(column=1, row=3) # Posiciona la etiqueta

    txtt36 = Entry(rise12, width=25) # Crea un campo de entrada de datos
    txtt36.grid(column=1, row=4) # Posiciona la entrada de texto

    def funcionumbral6(t1, t2):

        rise12.destroy()
        rise12.update()

        rise13 = Toplevel()
        rise13.title("Umbral de la escala de grises inv")
        rise13.geometry("320x250")

        if t1 < t2:
            tuno = t1
            tdos = t2
        else:
            tuno = t2
            tdos = t1

        int(t)

        p = io.imread("current.jpg")


        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (int(p[row,col]) <= tuno):
                        q[row,col] = 255
                    elif ((int(p[row,col]) > tuno) and (int(p[row,col]) < tdos)):
                        q[row,col] = 255 - p[row,col]
                    else:
                        q[row,col] = 255
            img = q
        else:
            q = p
            #for color in range(0,2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (int(p[row,col,color]) <= tuno):
                            q[row,col,color] = 255
                        elif ((int(p[row,col,color]) > tuno) and (int(p[row,col,color]) < tdos)):
                            q[row,col,color] = 255 - p[row,col,color]
                        else:
                            q[row,col,color] = 255
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", q)

        txtnomum6 = Entry(rise13, width=25) # Crea un campo de entrada de datos
        txtnomum6.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum6.insert(END, "edit.jpg")

        canvasum6 = Canvas(rise13, width=320, height=180)
        canvasum6.grid(column=1, row=2)

        im6 = Image.open("edit.jpg")
        im6 = im6.resize((320, 180), Image.ANTIALIAS)
        canvasum6.image = ImageTk.PhotoImage(im6)
        canvasum6.create_image(0, 0, image=canvasum6.image, anchor='nw')

        def descargainv6(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise13.destroy()
            rise13.update()

        btn_descargaum6 = Button(rise13, text="Descargar", command=lambda: descargainv6(str(txtnomum6.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum6.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150
    #u = 2

    #lista = []
    #lista.append(txtt3)
    #lista.append(txtt32)

    btn_aceptar6 = Button(rise12, text="Ok", command=lambda: funcionumbral6(int(txtt36.get()), int(txtt46.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar6.grid(column="1", row="5") # Posiciona el botón

def extension():
    global gris
    print("Extensión")

    rise14 = Toplevel()
    rise14.title("Extensión")
    rise14.geometry("230x150")

    lblespacio7 = Label(rise14, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio7.grid(column=0, row=0) # Posiciona la etiqueta

    lbl7 = Label(rise14, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl7.grid(column=1, row=1) # Posiciona la etiqueta

    txtt47 = Entry(rise14, width=25) # Crea un campo de entrada de datos
    txtt47.grid(column=1, row=2) # Posiciona la entrada de texto

    lbl37 = Label(rise14, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl37.grid(column=1, row=3) # Posiciona la etiqueta

    txtt37 = Entry(rise14, width=25) # Crea un campo de entrada de datos
    txtt37.grid(column=1, row=4) # Posiciona la entrada de texto

    def funcionumbral7(t1, t2):

        rise14.destroy()
        rise14.update()

        rise15 = Toplevel()
        rise15.title("Extensión")
        rise15.geometry("320x250")

        if t1 < t2:
            tuno = t1
            tdos = t2
        else:
            tuno = t2
            tdos = t1

        int(t)

        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(p[row,col]) <= tuno) or (int(p[row,col]) >= tdos)):
                        q[row,col] = 0
                    else:
                        q[row,col] = (p[row,col]-tuno)*(255/tdos-tuno)
            img = q
        else:
            q = p
            #for color in range(0,2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(p[row,col,color]) <= tuno) or (int(p[row,col,color]) >= tdos)):
                            q[row,col,color] = 0
                        else:
                            q[row,col,color] = (p[row,col,color]-tuno)*(255/tdos-tuno)
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", q)

        txtnomum7 = Entry(rise15, width=25) # Crea un campo de entrada de datos
        txtnomum7.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum7.insert(END, "edit.jpg")

        canvasum7 = Canvas(rise15, width=320, height=180)
        canvasum7.grid(column=1, row=2)

        im7 = Image.open("edit.jpg")
        im7 = im7.resize((320, 180), Image.ANTIALIAS)
        canvasum7.image = ImageTk.PhotoImage(im7)
        canvasum7.create_image(0, 0, image=canvasum7.image, anchor='nw')

        def descargainv7(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise15.destroy()
            rise15.update()

        btn_descargaum7 = Button(rise15, text="Descargar", command=lambda: descargainv7(str(txtnomum7.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum7.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150
    #u = 2

    #lista = []
    #lista.append(txtt3)
    #lista.append(txtt32)

    btn_aceptar7 = Button(rise14, text="Ok", command=lambda: funcionumbral7(int(txtt37.get()), int(txtt47.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar7.grid(column="1", row="5") # Posiciona el botón

def niveles():
    print("Reducción de niveles")
    global gris
    print("Reducción de niveles")

    rise16 = Toplevel()
    rise16.title("Reducción de niveles")
    rise16.geometry("210x130")

    lblespacio8 = Label(rise16, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacio8.grid(column=0, row=0) # Posiciona la etiqueta

    lbl8 = Label(rise16, text="Selecciona una opción", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbl8.grid(column=1, row=1) # Posiciona la etiqueta

    #txtt48 = Entry(rise16, width=25) # Crea un campo de entrada de datos
    #txtt48.grid(column=1, row=2) # Posiciona la entrada de texto

    #lbl38 = Label(rise16, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    #lbl38.grid(column=1, row=3) # Posiciona la etiqueta

    combo = ttk.Combobox(rise16, values=[2,4,8,16,32,64,128], state="readonly")
    combo.grid(column=1, row=2)

    #txtt38 = Entry(rise16, width=25) # Crea un campo de entrada de datos
    #txtt38.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbral8(v):

        rise16.destroy()
        rise16.update()

        rise17 = Toplevel()
        rise17.title("Reducción de Niveles")
        rise17.geometry("320x250")

        #if t1 < t2:
        #    tuno = t1
        #    tdos = t2
        #else:
        #    tuno = t2
        #    tdos = t1

        int(t)
        print("El v:", v)

        p = io.imread("current.jpg")

        q = p
        if gris == True:
            if v == 2:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) <= 128):
                            q[row,col] = 0
                        else:
                            q[row,col] = 255
                img = q
            elif v == 4:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) >= 0) and ((int(p[row,col])) <= 64):
                            q[row,col] = 0
                        elif ((int(p[row,col])) > 64) and ((int(p[row,col])) <= 128):
                            q[row,col] = 85
                        elif ((int(p[row,col])) > 128) and ((int(p[row,col])) <= 192):
                            q[row,col] = 170
                        else:
                            q[row,col] = 255
                img = q
            elif v == 8:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) >= 0) and ((int(p[row,col])) <= 32):
                            q[row,col] = 0
                        elif ((int(p[row,col])) > 32) and ((int(p[row,col])) <= 64):
                            q[row,col] = 37
                        elif ((int(p[row,col])) > 64) and ((int(p[row,col])) <= 96):
                            q[row,col] = 74
                        elif ((int(p[row,col])) > 96) and ((int(p[row,col])) <= 128):
                            q[row,col] = 111
                        elif ((int(p[row,col])) > 128) and ((int(p[row,col])) <= 160):
                            q[row,col] = 148
                        elif ((int(p[row,col])) > 160) and ((int(p[row,col])) <= 192):
                            q[row,col] = 185
                        elif ((int(p[row,col])) > 192) and ((int(p[row,col])) <= 224):
                            q[row,col] = 222
                        else:
                            q[row,col] = 255
                img = q
            elif v == 16:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) >= 0) and ((int(p[row,col])) <= 16):
                            q[row,col] = 0
                        elif ((int(p[row,col])) > 16) and ((int(p[row,col])) <= 32):
                            q[row,col] = 17
                        elif ((int(p[row,col])) > 32) and ((int(p[row,col])) <= 48):
                            q[row,col] = 34
                        elif ((int(p[row,col])) > 48) and ((int(p[row,col])) <= 64):
                            q[row,col] = 51
                        elif ((int(p[row,col])) > 64) and ((int(p[row,col])) <= 80):
                            q[row,col] = 68
                        elif ((int(p[row,col])) > 80) and ((int(p[row,col])) <= 96):
                            q[row,col] = 85
                        elif ((int(p[row,col])) > 96) and ((int(p[row,col])) <= 112):
                            q[row,col] = 102
                        elif ((int(p[row,col])) > 112) and ((int(p[row,col])) <= 128):
                            q[row,col] = 119
                        elif ((int(p[row,col])) > 128) and ((int(p[row,col])) <= 144):
                            q[row,col] = 136
                        elif ((int(p[row,col])) > 144) and ((int(p[row,col])) <= 160):
                            q[row,col] = 153
                        elif ((int(p[row,col])) > 160) and ((int(p[row,col])) <= 176):
                            q[row,col] = 170
                        elif ((int(p[row,col])) > 176) and ((int(p[row,col])) <= 192):
                            q[row,col] = 187
                        elif ((int(p[row,col])) > 192) and ((int(p[row,col])) <= 208):
                            q[row,col] = 204
                        elif ((int(p[row,col])) > 208) and ((int(p[row,col])) <= 224):
                            q[row,col] = 221
                        elif ((int(p[row,col])) > 224) and ((int(p[row,col])) <= 240):
                            q[row,col] = 238
                        else:
                            q[row,col] = 255
                img = q
            elif v == 32:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) >= 0) and ((int(p[row,col])) <= 8):
                            q[row,col] = 0
                        elif ((int(p[row,col])) > 8) and ((int(p[row,col])) <= 16):
                            q[row,col] = 8
                        elif ((int(p[row,col])) > 16) and ((int(p[row,col])) <= 24):
                            q[row,col] = 16
                        elif ((int(p[row,col])) > 24) and ((int(p[row,col])) <= 32):
                            q[row,col] = 24
                        elif ((int(p[row,col])) > 32) and ((int(p[row,col])) <= 40):
                            q[row,col] = 32
                        elif ((int(p[row,col])) > 40) and ((int(p[row,col])) <= 48):
                            q[row,col] = 40
                        elif ((int(p[row,col])) > 48) and ((int(p[row,col])) <= 56):
                            q[row,col] = 48
                        elif ((int(p[row,col])) > 56) and ((int(p[row,col])) <= 64):
                            q[row,col] = 56
                        elif ((int(p[row,col])) > 64) and ((int(p[row,col])) <= 72):
                            q[row,col] = 64
                        elif ((int(p[row,col])) > 72) and ((int(p[row,col])) <= 80):
                            q[row,col] = 72
                        elif ((int(p[row,col])) > 80) and ((int(p[row,col])) <= 88):
                            q[row,col] = 80
                        elif ((int(p[row,col])) > 88) and ((int(p[row,col])) <= 96):
                            q[row,col] = 88
                        elif ((int(p[row,col])) > 96) and ((int(p[row,col])) <= 104):
                            q[row,col] = 96
                        elif ((int(p[row,col])) > 104) and ((int(p[row,col])) <= 112):
                            q[row,col] = 104
                        elif ((int(p[row,col])) > 112) and ((int(p[row,col])) <= 120):
                            q[row,col] = 112
                        elif ((int(p[row,col])) > 120) and ((int(p[row,col])) <= 128):
                            q[row,col] = 120
                        elif ((int(p[row,col])) > 128) and ((int(p[row,col])) <= 136):
                            q[row,col] = 128
                        elif ((int(p[row,col])) > 136) and ((int(p[row,col])) <= 144):
                            q[row,col] = 136
                        elif ((int(p[row,col])) > 144) and ((int(p[row,col])) <= 152):
                            q[row,col] = 144
                        elif ((int(p[row,col])) > 152) and ((int(p[row,col])) <= 160):
                            q[row,col] = 152
                        elif ((int(p[row,col])) > 160) and ((int(p[row,col])) <= 168):
                            q[row,col] = 160
                        elif ((int(p[row,col])) > 168) and ((int(p[row,col])) <= 176):
                            q[row,col] = 168
                        elif ((int(p[row,col])) > 176) and ((int(p[row,col])) <= 184):
                            q[row,col] = 176
                        elif ((int(p[row,col])) > 184) and ((int(p[row,col])) <= 192):
                            q[row,col] = 184
                        elif ((int(p[row,col])) > 192) and ((int(p[row,col])) <= 200):
                            q[row,col] = 192
                        elif ((int(p[row,col])) > 200) and ((int(p[row,col])) <= 208):
                            q[row,col] = 200
                        elif ((int(p[row,col])) > 208) and ((int(p[row,col])) <= 216):
                            q[row,col] = 208
                        elif ((int(p[row,col])) > 216) and ((int(p[row,col])) <= 224):
                            q[row,col] = 216
                        elif ((int(p[row,col])) > 224) and ((int(p[row,col])) <= 232):
                            q[row,col] = 224
                        elif ((int(p[row,col])) > 232) and ((int(p[row,col])) <= 240):
                            q[row,col] = 232
                        elif ((int(p[row,col])) > 240) and ((int(p[row,col])) <= 248):
                            q[row,col] = 240
                        else:
                            q[row,col] = 255
                img = q
            elif v == 64:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) >= 0) and ((int(p[row,col])) <= 4):
                            q[row,col] = 0
                        elif ((int(p[row,col])) > 4) and ((int(p[row,col])) <= 8):
                            q[row,col] = 4
                        elif ((int(p[row,col])) > 8) and ((int(p[row,col])) <= 12):
                            q[row,col] = 8
                        elif ((int(p[row,col])) > 12) and ((int(p[row,col])) <= 16):
                            q[row,col] = 12
                        elif ((int(p[row,col])) > 16) and ((int(p[row,col])) <= 20):
                            q[row,col] = 16
                        elif ((int(p[row,col])) > 20) and ((int(p[row,col])) <= 24):
                            q[row,col] = 20
                        elif ((int(p[row,col])) > 24) and ((int(p[row,col])) <= 28):
                            q[row,col] = 24
                        elif ((int(p[row,col])) > 28) and ((int(p[row,col])) <= 32):
                            q[row,col] = 28
                        elif ((int(p[row,col])) > 32) and ((int(p[row,col])) <= 36):
                            q[row,col] = 32
                        elif ((int(p[row,col])) > 36) and ((int(p[row,col])) <= 40):
                            q[row,col] = 36
                        elif ((int(p[row,col])) > 40) and ((int(p[row,col])) <= 44):
                            q[row,col] = 40
                        elif ((int(p[row,col])) > 44) and ((int(p[row,col])) <= 48):
                            q[row,col] = 44
                        elif ((int(p[row,col])) > 48) and ((int(p[row,col])) <= 52):
                            q[row,col] = 48
                        elif ((int(p[row,col])) > 52) and ((int(p[row,col])) <= 56):
                            q[row,col] = 52
                        elif ((int(p[row,col])) > 56) and ((int(p[row,col])) <= 60):
                            q[row,col] = 56
                        elif ((int(p[row,col])) > 60) and ((int(p[row,col])) <= 64):
                            q[row,col] = 60
                        elif ((int(p[row,col])) > 64) and ((int(p[row,col])) <= 68):
                            q[row,col] = 64
                        elif ((int(p[row,col])) > 68) and ((int(p[row,col])) <= 72):
                            q[row,col] = 68
                        elif ((int(p[row,col])) > 72) and ((int(p[row,col])) <= 76):
                            q[row,col] = 72
                        elif ((int(p[row,col])) > 76) and ((int(p[row,col])) <= 80):
                            q[row,col] = 76
                        elif ((int(p[row,col])) > 80) and ((int(p[row,col])) <= 84):
                            q[row,col] = 80
                        elif ((int(p[row,col])) > 84) and ((int(p[row,col])) <= 88):
                            q[row,col] = 84
                        elif ((int(p[row,col])) > 88) and ((int(p[row,col])) <= 92):
                            q[row,col] = 88
                        elif ((int(p[row,col])) > 92) and ((int(p[row,col])) <= 96):
                            q[row,col] = 92
                        elif ((int(p[row,col])) > 96) and ((int(p[row,col])) <= 100):
                            q[row,col] = 96
                        elif ((int(p[row,col])) > 100) and ((int(p[row,col])) <= 104):
                            q[row,col] = 100
                        elif ((int(p[row,col])) > 104) and ((int(p[row,col])) <= 108):
                            q[row,col] = 104
                        elif ((int(p[row,col])) > 108) and ((int(p[row,col])) <= 112):
                            q[row,col] = 108
                        elif ((int(p[row,col])) > 112) and ((int(p[row,col])) <= 116):
                            q[row,col] = 112
                        elif ((int(p[row,col])) > 116) and ((int(p[row,col])) <= 120):
                            q[row,col] = 116
                        elif ((int(p[row,col])) > 120) and ((int(p[row,col])) <= 124):
                            q[row,col] = 120
                        elif ((int(p[row,col])) > 124) and ((int(p[row,col])) <= 128):
                            q[row,col] = 124
                        elif ((int(p[row,col])) > 128) and ((int(p[row,col])) <= 132):
                            q[row,col] = 128
                        elif ((int(p[row,col])) > 132) and ((int(p[row,col])) <= 136):
                            q[row,col] = 132
                        elif ((int(p[row,col])) > 136) and ((int(p[row,col])) <= 140):
                            q[row,col] = 136
                        elif ((int(p[row,col])) > 140) and ((int(p[row,col])) <= 144):
                            q[row,col] = 140
                        elif ((int(p[row,col])) > 144) and ((int(p[row,col])) <= 148):
                            q[row,col] = 144
                        elif ((int(p[row,col])) > 148) and ((int(p[row,col])) <= 152):
                            q[row,col] = 148
                        elif ((int(p[row,col])) > 152) and ((int(p[row,col])) <= 156):
                            q[row,col] = 152
                        elif ((int(p[row,col])) > 156) and ((int(p[row,col])) <= 160):
                            q[row,col] = 156
                        elif ((int(p[row,col])) > 160) and ((int(p[row,col])) <= 164):
                            q[row,col] = 160
                        elif ((int(p[row,col])) > 164) and ((int(p[row,col])) <= 168):
                            q[row,col] = 164
                        elif ((int(p[row,col])) > 168) and ((int(p[row,col])) <= 172):
                            q[row,col] = 168
                        elif ((int(p[row,col])) > 172) and ((int(p[row,col])) <= 176):
                            q[row,col] = 172
                        elif ((int(p[row,col])) > 176) and ((int(p[row,col])) <= 180):
                            q[row,col] = 176
                        elif ((int(p[row,col])) > 180) and ((int(p[row,col])) <= 184):
                            q[row,col] = 180
                        elif ((int(p[row,col])) > 184) and ((int(p[row,col])) <= 188):
                            q[row,col] = 184
                        elif ((int(p[row,col])) > 188) and ((int(p[row,col])) <= 192):
                            q[row,col] = 188
                        elif ((int(p[row,col])) > 192) and ((int(p[row,col])) <= 196):
                            q[row,col] = 192
                        elif ((int(p[row,col])) > 196) and ((int(p[row,col])) <= 200):
                            q[row,col] = 196
                        elif ((int(p[row,col])) > 200) and ((int(p[row,col])) <= 204):
                            q[row,col] = 200
                        elif ((int(p[row,col])) > 204) and ((int(p[row,col])) <= 208):
                            q[row,col] = 204
                        elif ((int(p[row,col])) > 208) and ((int(p[row,col])) <= 212):
                            q[row,col] = 208
                        elif ((int(p[row,col])) > 212) and ((int(p[row,col])) <= 216):
                            q[row,col] = 212
                        elif ((int(p[row,col])) > 216) and ((int(p[row,col])) <= 220):
                            q[row,col] = 216
                        elif ((int(p[row,col])) > 220) and ((int(p[row,col])) <= 224):
                            q[row,col] = 220
                        elif ((int(p[row,col])) > 224) and ((int(p[row,col])) <= 228):
                            q[row,col] = 224
                        elif ((int(p[row,col])) > 228) and ((int(p[row,col])) <= 232):
                            q[row,col] = 228
                        elif ((int(p[row,col])) > 232) and ((int(p[row,col])) <= 236):
                            q[row,col] = 232
                        elif ((int(p[row,col])) > 236) and ((int(p[row,col])) <= 240):
                            q[row,col] = 236
                        elif ((int(p[row,col])) > 240) and ((int(p[row,col])) <= 244):
                            q[row,col] = 240
                        elif ((int(p[row,col])) > 244) and ((int(p[row,col])) <= 248):
                            q[row,col] = 244
                        elif ((int(p[row,col])) > 248) and ((int(p[row,col])) <= 252):
                            q[row,col] = 248
                        else:
                            q[row,col] = 255
                img = q
            elif v == 128:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) >= 0) and ((int(p[row,col])) <= 2):
                            q[row,col] = 0
                        elif ((int(p[row,col])) > 2) and ((int(p[row,col])) <= 4):
                            q[row,col] = 2
                        elif ((int(p[row,col])) > 4) and ((int(p[row,col])) <= 6):
                            q[row,col] = 3
                        elif ((int(p[row,col])) > 6) and ((int(p[row,col])) <= 8):
                            q[row,col] = 6
                        elif ((int(p[row,col])) > 8) and ((int(p[row,col])) <= 10):
                            q[row,col] = 8
                        elif ((int(p[row,col])) > 10) and ((int(p[row,col])) <= 12):
                            q[row,col] = 10
                        elif ((int(p[row,col])) > 12) and ((int(p[row,col])) <= 14):
                            q[row,col] = 12
                        elif ((int(p[row,col])) > 14) and ((int(p[row,col])) <= 16):
                            q[row,col] = 14
                        elif ((int(p[row,col])) > 16) and ((int(p[row,col])) <= 18):
                            q[row,col] = 16
                        elif ((int(p[row,col])) > 18) and ((int(p[row,col])) <= 20):
                            q[row,col] = 18
                        elif ((int(p[row,col])) > 20) and ((int(p[row,col])) <= 22):
                            q[row,col] = 20
                        elif ((int(p[row,col])) > 22) and ((int(p[row,col])) <= 24):
                            q[row,col] = 22
                        elif ((int(p[row,col])) > 24) and ((int(p[row,col])) <= 26):
                            q[row,col] = 24
                        elif ((int(p[row,col])) > 26) and ((int(p[row,col])) <= 28):
                            q[row,col] = 26
                        elif ((int(p[row,col])) > 28) and ((int(p[row,col])) <= 30):
                            q[row,col] = 28
                        elif ((int(p[row,col])) > 30) and ((int(p[row,col])) <= 32):
                            q[row,col] = 30
                        elif ((int(p[row,col])) > 32) and ((int(p[row,col])) <= 34):
                            q[row,col] = 32
                        elif ((int(p[row,col])) > 34) and ((int(p[row,col])) <= 36):
                            q[row,col] = 34
                        elif ((int(p[row,col])) > 36) and ((int(p[row,col])) <= 38):
                            q[row,col] = 36
                        elif ((int(p[row,col])) > 38) and ((int(p[row,col])) <= 40):
                            q[row,col] = 38
                        elif ((int(p[row,col])) > 40) and ((int(p[row,col])) <= 42):
                            q[row,col] = 40
                        elif ((int(p[row,col])) > 42) and ((int(p[row,col])) <= 44):
                            q[row,col] = 42
                        elif ((int(p[row,col])) > 44) and ((int(p[row,col])) <= 46):
                            q[row,col] = 44
                        elif ((int(p[row,col])) > 46) and ((int(p[row,col])) <= 48):
                            q[row,col] = 46
                        elif ((int(p[row,col])) > 48) and ((int(p[row,col])) <= 50):
                            q[row,col] = 48
                        elif ((int(p[row,col])) > 50) and ((int(p[row,col])) <= 52):
                            q[row,col] = 50
                        elif ((int(p[row,col])) > 52) and ((int(p[row,col])) <= 54):
                            q[row,col] = 52
                        elif ((int(p[row,col])) > 54) and ((int(p[row,col])) <= 56):
                            q[row,col] = 54
                        elif ((int(p[row,col])) > 56) and ((int(p[row,col])) <= 58):
                            q[row,col] = 56
                        elif ((int(p[row,col])) > 58) and ((int(p[row,col])) <= 60):
                            q[row,col] = 58
                        elif ((int(p[row,col])) > 60) and ((int(p[row,col])) <= 62):
                            q[row,col] = 60
                        elif ((int(p[row,col])) > 62) and ((int(p[row,col])) <= 64):
                            q[row,col] = 62
                        elif ((int(p[row,col])) > 64) and ((int(p[row,col])) <= 66):
                            q[row,col] = 64
                        elif ((int(p[row,col])) > 66) and ((int(p[row,col])) <= 68):
                            q[row,col] = 66
                        elif ((int(p[row,col])) > 68) and ((int(p[row,col])) <= 70):
                            q[row,col] = 68
                        elif ((int(p[row,col])) > 70) and ((int(p[row,col])) <= 72):
                            q[row,col] = 70
                        elif ((int(p[row,col])) > 72) and ((int(p[row,col])) <= 74):
                            q[row,col] = 72
                        elif ((int(p[row,col])) > 74) and ((int(p[row,col])) <= 76):
                            q[row,col] = 74
                        elif ((int(p[row,col])) > 76) and ((int(p[row,col])) <= 78):
                            q[row,col] = 76
                        elif ((int(p[row,col])) > 78) and ((int(p[row,col])) <= 80):
                            q[row,col] = 78
                        elif ((int(p[row,col])) > 80) and ((int(p[row,col])) <= 82):
                            q[row,col] = 80
                        elif ((int(p[row,col])) > 82) and ((int(p[row,col])) <= 84):
                            q[row,col] = 82
                        elif ((int(p[row,col])) > 84) and ((int(p[row,col])) <= 86):
                            q[row,col] = 84
                        elif ((int(p[row,col])) > 86) and ((int(p[row,col])) <= 88):
                            q[row,col] = 86
                        elif ((int(p[row,col])) > 88) and ((int(p[row,col])) <= 90):
                            q[row,col] = 88
                        elif ((int(p[row,col])) > 90) and ((int(p[row,col])) <= 92):
                            q[row,col] = 90
                        elif ((int(p[row,col])) > 92) and ((int(p[row,col])) <= 94):
                            q[row,col] = 92
                        elif ((int(p[row,col])) > 94) and ((int(p[row,col])) <= 96):
                            q[row,col] = 94
                        elif ((int(p[row,col])) > 96) and ((int(p[row,col])) <= 98):
                            q[row,col] = 96
                        elif ((int(p[row,col])) > 98) and ((int(p[row,col])) <= 100):
                            q[row,col] = 98
                        elif ((int(p[row,col])) > 100) and ((int(p[row,col])) <= 102):
                            q[row,col] = 100
                        elif ((int(p[row,col])) > 102) and ((int(p[row,col])) <= 104):
                            q[row,col] = 102
                        elif ((int(p[row,col])) > 104) and ((int(p[row,col])) <= 106):
                            q[row,col] = 104
                        elif ((int(p[row,col])) > 106) and ((int(p[row,col])) <= 108):
                            q[row,col] = 106
                        elif ((int(p[row,col])) > 108) and ((int(p[row,col])) <= 110):
                            q[row,col] = 108
                        elif ((int(p[row,col])) > 110) and ((int(p[row,col])) <= 112):
                            q[row,col] = 110
                        elif ((int(p[row,col])) > 112) and ((int(p[row,col])) <= 114):
                            q[row,col] = 112
                        elif ((int(p[row,col])) > 114) and ((int(p[row,col])) <= 116):
                            q[row,col] = 114
                        elif ((int(p[row,col])) > 116) and ((int(p[row,col])) <= 118):
                            q[row,col] = 116
                        elif ((int(p[row,col])) > 118) and ((int(p[row,col])) <= 120):
                            q[row,col] = 118
                        elif ((int(p[row,col])) > 120) and ((int(p[row,col])) <= 122):
                            q[row,col] = 120
                        elif ((int(p[row,col])) > 122) and ((int(p[row,col])) <= 124):
                            q[row,col] = 122
                        elif ((int(p[row,col])) > 124) and ((int(p[row,col])) <= 126):
                            q[row,col] = 124
                        elif ((int(p[row,col])) > 126) and ((int(p[row,col])) <= 128):
                            q[row,col] = 126
                        elif ((int(p[row,col])) > 128) and ((int(p[row,col])) <= 130):
                            q[row,col] = 128
                        elif ((int(p[row,col])) > 130) and ((int(p[row,col])) <= 132):
                            q[row,col] = 130
                        elif ((int(p[row,col])) > 132) and ((int(p[row,col])) <= 134):
                            q[row,col] = 132
                        elif ((int(p[row,col])) > 134) and ((int(p[row,col])) <= 136):
                            q[row,col] = 134
                        elif ((int(p[row,col])) > 136) and ((int(p[row,col])) <= 138):
                            q[row,col] = 136
                        elif ((int(p[row,col])) > 138) and ((int(p[row,col])) <= 140):
                            q[row,col] = 138
                        elif ((int(p[row,col])) > 140) and ((int(p[row,col])) <= 142):
                            q[row,col] = 140
                        elif ((int(p[row,col])) > 142) and ((int(p[row,col])) <= 144):
                            q[row,col] = 142
                        elif ((int(p[row,col])) > 144) and ((int(p[row,col])) <= 146):
                            q[row,col] = 144
                        elif ((int(p[row,col])) > 146) and ((int(p[row,col])) <= 148):
                            q[row,col] = 146
                        elif ((int(p[row,col])) > 148) and ((int(p[row,col])) <= 150):
                            q[row,col] = 148
                        elif ((int(p[row,col])) > 150) and ((int(p[row,col])) <= 152):
                            q[row,col] = 150
                        elif ((int(p[row,col])) > 152) and ((int(p[row,col])) <= 154):
                            q[row,col] = 152
                        elif ((int(p[row,col])) > 154) and ((int(p[row,col])) <= 156):
                            q[row,col] = 154
                        elif ((int(p[row,col])) > 156) and ((int(p[row,col])) <= 158):
                            q[row,col] = 156
                        elif ((int(p[row,col])) > 158) and ((int(p[row,col])) <= 160):
                            q[row,col] = 158
                        elif ((int(p[row,col])) > 160) and ((int(p[row,col])) <= 162):
                            q[row,col] = 160
                        elif ((int(p[row,col])) > 162) and ((int(p[row,col])) <= 164):
                            q[row,col] = 162
                        elif ((int(p[row,col])) > 164) and ((int(p[row,col])) <= 166):
                            q[row,col] = 164
                        elif ((int(p[row,col])) > 166) and ((int(p[row,col])) <= 168):
                            q[row,col] = 166
                        elif ((int(p[row,col])) > 168) and ((int(p[row,col])) <= 170):
                            q[row,col] = 168
                        elif ((int(p[row,col])) > 170) and ((int(p[row,col])) <= 172):
                            q[row,col] = 170
                        elif ((int(p[row,col])) > 172) and ((int(p[row,col])) <= 174):
                            q[row,col] = 172
                        elif ((int(p[row,col])) > 174) and ((int(p[row,col])) <= 176):
                            q[row,col] = 174
                        elif ((int(p[row,col])) > 176) and ((int(p[row,col])) <= 178):
                            q[row,col] = 176
                        elif ((int(p[row,col])) > 178) and ((int(p[row,col])) <= 180):
                            q[row,col] = 178
                        elif ((int(p[row,col])) > 180) and ((int(p[row,col])) <= 182):
                            q[row,col] = 180
                        elif ((int(p[row,col])) > 182) and ((int(p[row,col])) <= 184):
                            q[row,col] = 182
                        elif ((int(p[row,col])) > 184) and ((int(p[row,col])) <= 186):
                            q[row,col] = 184
                        elif ((int(p[row,col])) > 186) and ((int(p[row,col])) <= 188):
                            q[row,col] = 186
                        elif ((int(p[row,col])) > 188) and ((int(p[row,col])) <= 190):
                            q[row,col] = 188
                        elif ((int(p[row,col])) > 190) and ((int(p[row,col])) <= 192):
                            q[row,col] = 190
                        elif ((int(p[row,col])) > 192) and ((int(p[row,col])) <= 194):
                            q[row,col] = 192
                        elif ((int(p[row,col])) > 194) and ((int(p[row,col])) <= 196):
                            q[row,col] = 194
                        elif ((int(p[row,col])) > 196) and ((int(p[row,col])) <= 198):
                            q[row,col] = 196
                        elif ((int(p[row,col])) > 198) and ((int(p[row,col])) <= 200):
                            q[row,col] = 198
                        elif ((int(p[row,col])) > 200) and ((int(p[row,col])) <= 202):
                            q[row,col] = 200
                        elif ((int(p[row,col])) > 202) and ((int(p[row,col])) <= 204):
                            q[row,col] = 202
                        elif ((int(p[row,col])) > 204) and ((int(p[row,col])) <= 206):
                            q[row,col] = 204
                        elif ((int(p[row,col])) > 206) and ((int(p[row,col])) <= 208):
                            q[row,col] = 206
                        elif ((int(p[row,col])) > 208) and ((int(p[row,col])) <= 210):
                            q[row,col] = 208
                        elif ((int(p[row,col])) > 210) and ((int(p[row,col])) <= 212):
                            q[row,col] = 210
                        elif ((int(p[row,col])) > 212) and ((int(p[row,col])) <= 214):
                            q[row,col] = 212
                        elif ((int(p[row,col])) > 214) and ((int(p[row,col])) <= 216):
                            q[row,col] = 214
                        elif ((int(p[row,col])) > 216) and ((int(p[row,col])) <= 218):
                            q[row,col] = 216
                        elif ((int(p[row,col])) > 218) and ((int(p[row,col])) <= 220):
                            q[row,col] = 218
                        elif ((int(p[row,col])) > 220) and ((int(p[row,col])) <= 222):
                            q[row,col] = 220
                        elif ((int(p[row,col])) > 222) and ((int(p[row,col])) <= 224):
                            q[row,col] = 222
                        elif ((int(p[row,col])) > 224) and ((int(p[row,col])) <= 226):
                            q[row,col] = 224
                        elif ((int(p[row,col])) > 226) and ((int(p[row,col])) <= 228):
                            q[row,col] = 226
                        elif ((int(p[row,col])) > 228) and ((int(p[row,col])) <= 230):
                            q[row,col] = 228
                        elif ((int(p[row,col])) > 230) and ((int(p[row,col])) <= 232):
                            q[row,col] = 230
                        elif ((int(p[row,col])) > 232) and ((int(p[row,col])) <= 234):
                            q[row,col] = 232
                        elif ((int(p[row,col])) > 234) and ((int(p[row,col])) <= 236):
                            q[row,col] = 234
                        elif ((int(p[row,col])) > 236) and ((int(p[row,col])) <= 238):
                            q[row,col] = 236
                        elif ((int(p[row,col])) > 238) and ((int(p[row,col])) <= 240):
                            q[row,col] = 238
                        elif ((int(p[row,col])) > 240) and ((int(p[row,col])) <= 242):
                            q[row,col] = 240
                        elif ((int(p[row,col])) > 242) and ((int(p[row,col])) <= 244):
                            q[row,col] = 242
                        elif ((int(p[row,col])) > 244) and ((int(p[row,col])) <= 246):
                            q[row,col] = 244
                        elif ((int(p[row,col])) > 246) and ((int(p[row,col])) <= 248):
                            q[row,col] = 246
                        elif ((int(p[row,col])) > 248) and ((int(p[row,col])) <= 250):
                            q[row,col] = 248
                        elif ((int(p[row,col])) > 250) and ((int(p[row,col])) <= 252):
                            q[row,col] = 250
                        elif ((int(p[row,col])) > 252) and ((int(p[row,col])) <= 254):
                            q[row,col] = 252
                        else:
                            q[row,col] = 255
            img = q
        else:
            if v == 2:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) <= 128):
                                q[row,col,color] = 0
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
            elif v == 4:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) >= 0) and ((int(p[row,col,color])) <= 64):
                                q[row,col,color] = 0
                            elif ((int(p[row,col,color])) > 64) and ((int(p[row,col,color])) <= 128):
                                q[row,col] = 85
                            elif ((int(p[row,col,color])) > 128) and ((int(p[row,col,color])) <= 192):
                                q[row,col,color] = 170
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
            elif v == 8:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) >= 0) and ((int(p[row,col,color])) <= 32):
                                q[row,col,color] = 0
                            elif ((int(p[row,col,color])) > 32) and ((int(p[row,col,color])) <= 64):
                                q[row,col,color] = 37
                            elif ((int(p[row,col,color])) > 64) and ((int(p[row,col,color])) <= 96):
                                q[row,col,color] = 74
                            elif ((int(p[row,col,color])) > 96) and ((int(p[row,col,color])) <= 128):
                                q[row,col,color] = 111
                            elif ((int(p[row,col,color])) > 128) and ((int(p[row,col,color])) <= 160):
                                q[row,col,color] = 148
                            elif ((int(p[row,col,color])) > 160) and ((int(p[row,col,color])) <= 192):
                                q[row,col,color] = 185
                            elif ((int(p[row,col,color])) > 192) and ((int(p[row,col,color])) <= 224):
                                q[row,col,color] = 222
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
            elif v == 16:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) >= 0) and ((int(p[row,col,color])) <= 16):
                                q[row,col,color] = 0
                            elif ((int(p[row,col,color])) > 16) and ((int(p[row,col,color])) <= 32):
                                q[row,col,color] = 17
                            elif ((int(p[row,col,color])) > 32) and ((int(p[row,col,color])) <= 48):
                                q[row,col,color] = 34
                            elif ((int(p[row,col,color])) > 48) and ((int(p[row,col,color])) <= 64):
                                q[row,col,color] = 51
                            elif ((int(p[row,col,color])) > 64) and ((int(p[row,col,color])) <= 80):
                                q[row,col,color] = 68
                            elif ((int(p[row,col,color])) > 80) and ((int(p[row,col,color])) <= 96):
                                q[row,col,color] = 85
                            elif ((int(p[row,col,color])) > 96) and ((int(p[row,col,color])) <= 112):
                                q[row,col,color] = 102
                            elif ((int(p[row,col,color])) > 112) and ((int(p[row,col,color])) <= 128):
                                q[row,col,color] = 119
                            elif ((int(p[row,col,color])) > 128) and ((int(p[row,col,color])) <= 144):
                                q[row,col,color] = 136
                            elif ((int(p[row,col,color])) > 144) and ((int(p[row,col,color])) <= 160):
                                q[row,col,color] = 153
                            elif ((int(p[row,col,color])) > 160) and ((int(p[row,col,color])) <= 176):
                                q[row,col,color] = 170
                            elif ((int(p[row,col,color])) > 176) and ((int(p[row,col,color])) <= 192):
                                q[row,col,color] = 187
                            elif ((int(p[row,col,color])) > 192) and ((int(p[row,col,color])) <= 208):
                                q[row,col,color] = 204
                            elif ((int(p[row,col,color])) > 208) and ((int(p[row,col,color])) <= 224):
                                q[row,col,color] = 221
                            elif ((int(p[row,col,color])) > 224) and ((int(p[row,col,color])) <= 240):
                                q[row,col,color] = 238
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
            elif v == 32:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) >= 0) and ((int(p[row,col,color])) <= 8):
                                q[row,col,color] = 0
                            elif ((int(p[row,col,color])) > 8) and ((int(p[row,col,color])) <= 16):
                                q[row,col,color] = 8
                            elif ((int(p[row,col,color])) > 16) and ((int(p[row,col,color])) <= 24):
                                q[row,col,color] = 16
                            elif ((int(p[row,col,color])) > 24) and ((int(p[row,col,color])) <= 32):
                                q[row,col,color] = 24
                            elif ((int(p[row,col,color])) > 32) and ((int(p[row,col,color])) <= 40):
                                q[row,col,color] = 32
                            elif ((int(p[row,col,color])) > 40) and ((int(p[row,col,color])) <= 48):
                                q[row,col,color] = 40
                            elif ((int(p[row,col,color])) > 48) and ((int(p[row,col,color])) <= 56):
                                q[row,col,color] = 48
                            elif ((int(p[row,col,color])) > 56) and ((int(p[row,col,color])) <= 64):
                                q[row,col,color] = 56
                            elif ((int(p[row,col,color])) > 64) and ((int(p[row,col,color])) <= 72):
                                q[row,col,color] = 64
                            elif ((int(p[row,col,color])) > 72) and ((int(p[row,col,color])) <= 80):
                                q[row,col,color] = 72
                            elif ((int(p[row,col,color])) > 80) and ((int(p[row,col,color])) <= 88):
                                q[row,col,color] = 80
                            elif ((int(p[row,col,color])) > 88) and ((int(p[row,col,color])) <= 96):
                                q[row,col,color] = 88
                            elif ((int(p[row,col,color])) > 96) and ((int(p[row,col,color])) <= 104):
                                q[row,col,color] = 96
                            elif ((int(p[row,col,color])) > 104) and ((int(p[row,col,color])) <= 112):
                                q[row,col,color] = 104
                            elif ((int(p[row,col,color])) > 112) and ((int(p[row,col,color])) <= 120):
                                q[row,col,color] = 112
                            elif ((int(p[row,col,color])) > 120) and ((int(p[row,col,color])) <= 128):
                                q[row,col,color] = 120
                            elif ((int(p[row,col,color])) > 128) and ((int(p[row,col,color])) <= 136):
                                q[row,col,color] = 128
                            elif ((int(p[row,col,color])) > 136) and ((int(p[row,col,color])) <= 144):
                                q[row,col,color] = 136
                            elif ((int(p[row,col,color])) > 144) and ((int(p[row,col,color])) <= 152):
                                q[row,col,color] = 144
                            elif ((int(p[row,col,color])) > 152) and ((int(p[row,col,color])) <= 160):
                                q[row,col,color] = 152
                            elif ((int(p[row,col,color])) > 160) and ((int(p[row,col,color])) <= 168):
                                q[row,col,color] = 160
                            elif ((int(p[row,col,color])) > 168) and ((int(p[row,col,color])) <= 176):
                                q[row,col,color] = 168
                            elif ((int(p[row,col,color])) > 176) and ((int(p[row,col,color])) <= 184):
                                q[row,col,color] = 176
                            elif ((int(p[row,col,color])) > 184) and ((int(p[row,col,color])) <= 192):
                                q[row,col,color] = 184
                            elif ((int(p[row,col,color])) > 192) and ((int(p[row,col,color])) <= 200):
                                q[row,col,color] = 192
                            elif ((int(p[row,col,color])) > 200) and ((int(p[row,col,color])) <= 208):
                                q[row,col,color] = 200
                            elif ((int(p[row,col,color])) > 208) and ((int(p[row,col,color])) <= 216):
                                q[row,col,color] = 208
                            elif ((int(p[row,col,color])) > 216) and ((int(p[row,col,color])) <= 224):
                                q[row,col,color] = 216
                            elif ((int(p[row,col,color])) > 224) and ((int(p[row,col,color])) <= 232):
                                q[row,col,color] = 224
                            elif ((int(p[row,col,color])) > 232) and ((int(p[row,col,color])) <= 240):
                                q[row,col,color] = 232
                            elif ((int(p[row,col,color])) > 240) and ((int(p[row,col,color])) <= 248):
                                q[row,col,color] = 240
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
            elif v == 64:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) >= 0) and ((int(p[row,col,color])) <= 4):
                                q[row,col,color] = 0
                            elif ((int(p[row,col,color])) > 4) and ((int(p[row,col,color])) <= 8):
                                q[row,col,color] = 4
                            elif ((int(p[row,col,color])) > 8) and ((int(p[row,col,color])) <= 12):
                                q[row,col,color] = 8
                            elif ((int(p[row,col,color])) > 12) and ((int(p[row,col,color])) <= 16):
                                q[row,col,color] = 12
                            elif ((int(p[row,col,color])) > 16) and ((int(p[row,col,color])) <= 20):
                                q[row,col,color] = 16
                            elif ((int(p[row,col,color])) > 20) and ((int(p[row,col,color])) <= 24):
                                q[row,col,color] = 20
                            elif ((int(p[row,col,color])) > 24) and ((int(p[row,col,color])) <= 28):
                                q[row,col,color] = 24
                            elif ((int(p[row,col,color])) > 28) and ((int(p[row,col,color])) <= 32):
                                q[row,col,color] = 28
                            elif ((int(p[row,col,color])) > 32) and ((int(p[row,col,color])) <= 36):
                                q[row,col,color] = 32
                            elif ((int(p[row,col,color])) > 36) and ((int(p[row,col,color])) <= 40):
                                q[row,col,color] = 36
                            elif ((int(p[row,col,color])) > 40) and ((int(p[row,col,color])) <= 44):
                                q[row,col,color] = 40
                            elif ((int(p[row,col,color])) > 44) and ((int(p[row,col,color])) <= 48):
                                q[row,col,color] = 44
                            elif ((int(p[row,col,color])) > 48) and ((int(p[row,col,color])) <= 52):
                                q[row,col,color] = 48
                            elif ((int(p[row,col,color])) > 52) and ((int(p[row,col,color])) <= 56):
                                q[row,col,color] = 52
                            elif ((int(p[row,col,color])) > 56) and ((int(p[row,col,color])) <= 60):
                                q[row,col,color] = 56
                            elif ((int(p[row,col,color])) > 60) and ((int(p[row,col,color])) <= 64):
                                q[row,col,color] = 60
                            elif ((int(p[row,col,color])) > 64) and ((int(p[row,col,color])) <= 68):
                                q[row,col,color] = 64
                            elif ((int(p[row,col,color])) > 68) and ((int(p[row,col,color])) <= 72):
                                q[row,col,color] = 68
                            elif ((int(p[row,col,color])) > 72) and ((int(p[row,col,color])) <= 76):
                                q[row,col,color] = 72
                            elif ((int(p[row,col,color])) > 76) and ((int(p[row,col,color])) <= 80):
                                q[row,col,color] = 76
                            elif ((int(p[row,col,color])) > 80) and ((int(p[row,col,color])) <= 84):
                                q[row,col,color] = 80
                            elif ((int(p[row,col,color])) > 84) and ((int(p[row,col,color])) <= 88):
                                q[row,col,color] = 84
                            elif ((int(p[row,col,color])) > 88) and ((int(p[row,col,color])) <= 92):
                                q[row,col,color] = 88
                            elif ((int(p[row,col,color])) > 92) and ((int(p[row,col,color])) <= 96):
                                q[row,col,color] = 92
                            elif ((int(p[row,col,color])) > 96) and ((int(p[row,col,color])) <= 100):
                                q[row,col,color] = 96
                            elif ((int(p[row,col,color])) > 100) and ((int(p[row,col,color])) <= 104):
                                q[row,col,color] = 100
                            elif ((int(p[row,col,color])) > 104) and ((int(p[row,col,color])) <= 108):
                                q[row,col,color] = 104
                            elif ((int(p[row,col,color])) > 108) and ((int(p[row,col,color])) <= 112):
                                q[row,col,color] = 108
                            elif ((int(p[row,col,color])) > 112) and ((int(p[row,col,color])) <= 116):
                                q[row,col,color] = 112
                            elif ((int(p[row,col,color])) > 116) and ((int(p[row,col,color])) <= 120):
                                q[row,col,color] = 116
                            elif ((int(p[row,col,color])) > 120) and ((int(p[row,col,color])) <= 124):
                                q[row,col,color] = 120
                            elif ((int(p[row,col,color])) > 124) and ((int(p[row,col,color])) <= 128):
                                q[row,col,color] = 124
                            elif ((int(p[row,col,color])) > 128) and ((int(p[row,col,color])) <= 132):
                                q[row,col,color] = 128
                            elif ((int(p[row,col,color])) > 132) and ((int(p[row,col,color])) <= 136):
                                q[row,col,color] = 132
                            elif ((int(p[row,col,color])) > 136) and ((int(p[row,col,color])) <= 140):
                                q[row,col,color] = 136
                            elif ((int(p[row,col,color])) > 140) and ((int(p[row,col,color])) <= 144):
                                q[row,col,color] = 140
                            elif ((int(p[row,col,color])) > 144) and ((int(p[row,col,color])) <= 148):
                                q[row,col,color] = 144
                            elif ((int(p[row,col,color])) > 148) and ((int(p[row,col,color])) <= 152):
                                q[row,col,color] = 148
                            elif ((int(p[row,col,color])) > 152) and ((int(p[row,col,color])) <= 156):
                                q[row,col,color] = 152
                            elif ((int(p[row,col,color])) > 156) and ((int(p[row,col,color])) <= 160):
                                q[row,col,color] = 156
                            elif ((int(p[row,col,color])) > 160) and ((int(p[row,col,color])) <= 164):
                                q[row,col,color] = 160
                            elif ((int(p[row,col,color])) > 164) and ((int(p[row,col,color])) <= 168):
                                q[row,col,color] = 164
                            elif ((int(p[row,col,color])) > 168) and ((int(p[row,col,color])) <= 172):
                                q[row,col,color] = 168
                            elif ((int(p[row,col,color])) > 172) and ((int(p[row,col,color])) <= 176):
                                q[row,col,color] = 172
                            elif ((int(p[row,col,color])) > 176) and ((int(p[row,col,color])) <= 180):
                                q[row,col,color] = 176
                            elif ((int(p[row,col,color])) > 180) and ((int(p[row,col,color])) <= 184):
                                q[row,col,color] = 180
                            elif ((int(p[row,col,color])) > 184) and ((int(p[row,col,color])) <= 188):
                                q[row,col,color] = 184
                            elif ((int(p[row,col,color])) > 188) and ((int(p[row,col,color])) <= 192):
                                q[row,col,color] = 188
                            elif ((int(p[row,col,color])) > 192) and ((int(p[row,col,color])) <= 196):
                                q[row,col,color] = 192
                            elif ((int(p[row,col,color])) > 196) and ((int(p[row,col,color])) <= 200):
                                q[row,col,color] = 196
                            elif ((int(p[row,col,color])) > 200) and ((int(p[row,col,color])) <= 204):
                                q[row,col,color] = 200
                            elif ((int(p[row,col,color])) > 204) and ((int(p[row,col,color])) <= 208):
                                q[row,col,color] = 204
                            elif ((int(p[row,col,color])) > 208) and ((int(p[row,col,color])) <= 212):
                                q[row,col,color] = 208
                            elif ((int(p[row,col,color])) > 212) and ((int(p[row,col,color])) <= 216):
                                q[row,col,color] = 212
                            elif ((int(p[row,col,color])) > 216) and ((int(p[row,col,color])) <= 220):
                                q[row,col,color] = 216
                            elif ((int(p[row,col,color])) > 220) and ((int(p[row,col,color])) <= 224):
                                q[row,col,color] = 220
                            elif ((int(p[row,col,color])) > 224) and ((int(p[row,col,color])) <= 228):
                                q[row,col,color] = 224
                            elif ((int(p[row,col,color])) > 228) and ((int(p[row,col,color])) <= 232):
                                q[row,col,color] = 228
                            elif ((int(p[row,col,color])) > 232) and ((int(p[row,col,color])) <= 236):
                                q[row,col,color] = 232
                            elif ((int(p[row,col,color])) > 236) and ((int(p[row,col,color])) <= 240):
                                q[row,col,color] = 236
                            elif ((int(p[row,col,color])) > 240) and ((int(p[row,col,color])) <= 244):
                                q[row,col,color] = 240
                            elif ((int(p[row,col,color])) > 244) and ((int(p[row,col,color])) <= 248):
                                q[row,col,color] = 244
                            elif ((int(p[row,col,color])) > 248) and ((int(p[row,col,color])) <= 252):
                                q[row,col,color] = 248
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
            elif v == 128:
                #for color in range(0,2):
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if ((int(p[row,col,color])) >= 0) and ((int(p[row,col,color])) <= 2):
                                q[row,col,color] = 0
                            elif ((int(p[row,col,color])) > 2) and ((int(p[row,col,color])) <= 4):
                                q[row,col,color] = 2
                            elif ((int(p[row,col,color])) > 4) and ((int(p[row,col,color])) <= 6):
                                q[row,col,color] = 3
                            elif ((int(p[row,col,color])) > 6) and ((int(p[row,col,color])) <= 8):
                                q[row,col,color] = 6
                            elif ((int(p[row,col,color])) > 8) and ((int(p[row,col,color])) <= 10):
                                q[row,col,color] = 8
                            elif ((int(p[row,col,color])) > 10) and ((int(p[row,col,color])) <= 12):
                                q[row,col,color] = 10
                            elif ((int(p[row,col,color])) > 12) and ((int(p[row,col,color])) <= 14):
                                q[row,col,color] = 12
                            elif ((int(p[row,col,color])) > 14) and ((int(p[row,col,color])) <= 16):
                                q[row,col,color] = 14
                            elif ((int(p[row,col,color])) > 16) and ((int(p[row,col,color])) <= 18):
                                q[row,col,color] = 16
                            elif ((int(p[row,col,color])) > 18) and ((int(p[row,col,color])) <= 20):
                                q[row,col,color] = 18
                            elif ((int(p[row,col,color])) > 20) and ((int(p[row,col,color])) <= 22):
                                q[row,col,color] = 20
                            elif ((int(p[row,col,color])) > 22) and ((int(p[row,col,color])) <= 24):
                                q[row,col,color] = 22
                            elif ((int(p[row,col,color])) > 24) and ((int(p[row,col,color])) <= 26):
                                q[row,col,color] = 24
                            elif ((int(p[row,col,color])) > 26) and ((int(p[row,col,color])) <= 28):
                                q[row,col] = 26
                            elif ((int(p[row,col,color])) > 28) and ((int(p[row,col,color])) <= 30):
                                q[row,col,color] = 28
                            elif ((int(p[row,col,color])) > 30) and ((int(p[row,col,color])) <= 32):
                                q[row,col,color] = 30
                            elif ((int(p[row,col,color])) > 32) and ((int(p[row,col,color])) <= 34):
                                q[row,col,color] = 32
                            elif ((int(p[row,col,color])) > 34) and ((int(p[row,col,color])) <= 36):
                                q[row,col,color] = 34
                            elif ((int(p[row,col,color])) > 36) and ((int(p[row,col,color])) <= 38):
                                q[row,col,color] = 36
                            elif ((int(p[row,col,color])) > 38) and ((int(p[row,col,color])) <= 40):
                                q[row,col,color] = 38
                            elif ((int(p[row,col,color])) > 40) and ((int(p[row,col,color])) <= 42):
                                q[row,col,color] = 40
                            elif ((int(p[row,col,color])) > 42) and ((int(p[row,col,color])) <= 44):
                                q[row,col,color] = 42
                            elif ((int(p[row,col,color])) > 44) and ((int(p[row,col,color])) <= 46):
                                q[row,col,color] = 44
                            elif ((int(p[row,col,color])) > 46) and ((int(p[row,col,color])) <= 48):
                                q[row,col,color] = 46
                            elif ((int(p[row,col,color])) > 48) and ((int(p[row,col,color])) <= 50):
                                q[row,col,color] = 48
                            elif ((int(p[row,col,color])) > 50) and ((int(p[row,col,color])) <= 52):
                                q[row,col,color] = 50
                            elif ((int(p[row,col,color])) > 52) and ((int(p[row,col,color])) <= 54):
                                q[row,col,color] = 52
                            elif ((int(p[row,col,color])) > 54) and ((int(p[row,col,color])) <= 56):
                                q[row,col,color] = 54
                            elif ((int(p[row,col,color])) > 56) and ((int(p[row,col,color])) <= 58):
                                q[row,col,color] = 56
                            elif ((int(p[row,col,color])) > 58) and ((int(p[row,col,color])) <= 60):
                                q[row,col,color] = 58
                            elif ((int(p[row,col,color])) > 60) and ((int(p[row,col,color])) <= 62):
                                q[row,col,color] = 60
                            elif ((int(p[row,col,color])) > 62) and ((int(p[row,col,color])) <= 64):
                                q[row,col,color] = 62
                            elif ((int(p[row,col,color])) > 64) and ((int(p[row,col,color])) <= 66):
                                q[row,col,color] = 64
                            elif ((int(p[row,col,color])) > 66) and ((int(p[row,col,color])) <= 68):
                                q[row,col,color] = 66
                            elif ((int(p[row,col,color])) > 68) and ((int(p[row,col,color])) <= 70):
                                q[row,col,color] = 68
                            elif ((int(p[row,col,color])) > 70) and ((int(p[row,col,color])) <= 72):
                                q[row,col,color] = 70
                            elif ((int(p[row,col,color])) > 72) and ((int(p[row,col,color])) <= 74):
                                q[row,col,color] = 72
                            elif ((int(p[row,col,color])) > 74) and ((int(p[row,col,color])) <= 76):
                                q[row,col,color] = 74
                            elif ((int(p[row,col,color])) > 76) and ((int(p[row,col,color])) <= 78):
                                q[row,col,color] = 76
                            elif ((int(p[row,col,color])) > 78) and ((int(p[row,col,color])) <= 80):
                                q[row,col,color] = 78
                            elif ((int(p[row,col,color])) > 80) and ((int(p[row,col,color])) <= 82):
                                q[row,col,color] = 80
                            elif ((int(p[row,col,color])) > 82) and ((int(p[row,col,color])) <= 84):
                                q[row,col,color] = 82
                            elif ((int(p[row,col,color])) > 84) and ((int(p[row,col,color])) <= 86):
                                q[row,col,color] = 84
                            elif ((int(p[row,col,color])) > 86) and ((int(p[row,col,color])) <= 88):
                                q[row,col,color] = 86
                            elif ((int(p[row,col,color])) > 88) and ((int(p[row,col,color])) <= 90):
                                q[row,col,color] = 88
                            elif ((int(p[row,col,color])) > 90) and ((int(p[row,col,color])) <= 92):
                                q[row,col,color] = 90
                            elif ((int(p[row,col,color])) > 92) and ((int(p[row,col,color])) <= 94):
                                q[row,col,color] = 92
                            elif ((int(p[row,col,color])) > 94) and ((int(p[row,col,color])) <= 96):
                                q[row,col,color] = 94
                            elif ((int(p[row,col,color])) > 96) and ((int(p[row,col,color])) <= 98):
                                q[row,col,color] = 96
                            elif ((int(p[row,col,color])) > 98) and ((int(p[row,col,color])) <= 100):
                                q[row,col,color] = 98
                            elif ((int(p[row,col,color])) > 100) and ((int(p[row,col,color])) <= 102):
                                q[row,col,color] = 100
                            elif ((int(p[row,col,color])) > 102) and ((int(p[row,col,color])) <= 104):
                                q[row,col,color] = 102
                            elif ((int(p[row,col,color])) > 104) and ((int(p[row,col,color])) <= 106):
                                q[row,col,color] = 104
                            elif ((int(p[row,col,color])) > 106) and ((int(p[row,col,color])) <= 108):
                                q[row,col,color] = 106
                            elif ((int(p[row,col,color])) > 108) and ((int(p[row,col,color])) <= 110):
                                q[row,col,color] = 108
                            elif ((int(p[row,col,color])) > 110) and ((int(p[row,col,color])) <= 112):
                                q[row,col,color] = 110
                            elif ((int(p[row,col,color])) > 112) and ((int(p[row,col,color])) <= 114):
                                q[row,col,color] = 112
                            elif ((int(p[row,col,color])) > 114) and ((int(p[row,col,color])) <= 116):
                                q[row,col,color] = 114
                            elif ((int(p[row,col,color])) > 116) and ((int(p[row,col,color])) <= 118):
                                q[row,col,color] = 116
                            elif ((int(p[row,col,color])) > 118) and ((int(p[row,col,color])) <= 120):
                                q[row,col,color] = 118
                            elif ((int(p[row,col,color])) > 120) and ((int(p[row,col,color])) <= 122):
                                q[row,col,color] = 120
                            elif ((int(p[row,col,color])) > 122) and ((int(p[row,col,color])) <= 124):
                                q[row,col,color] = 122
                            elif ((int(p[row,col,color])) > 124) and ((int(p[row,col,color])) <= 126):
                                q[row,col,color] = 124
                            elif ((int(p[row,col,color])) > 126) and ((int(p[row,col,color])) <= 128):
                                q[row,col,color] = 126
                            elif ((int(p[row,col,color])) > 128) and ((int(p[row,col,color])) <= 130):
                                q[row,col,color] = 128
                            elif ((int(p[row,col,color])) > 130) and ((int(p[row,col,color])) <= 132):
                                q[row,col,color] = 130
                            elif ((int(p[row,col,color])) > 132) and ((int(p[row,col,color])) <= 134):
                                q[row,col,color] = 132
                            elif ((int(p[row,col,color])) > 134) and ((int(p[row,col,color])) <= 136):
                                q[row,col,color] = 134
                            elif ((int(p[row,col,color])) > 136) and ((int(p[row,col,color])) <= 138):
                                q[row,col,color] = 136
                            elif ((int(p[row,col,color])) > 138) and ((int(p[row,col,color])) <= 140):
                                q[row,col,color] = 138
                            elif ((int(p[row,col,color])) > 140) and ((int(p[row,col,color])) <= 142):
                                q[row,col,color] = 140
                            elif ((int(p[row,col,color])) > 142) and ((int(p[row,col,color])) <= 144):
                                q[row,col,color] = 142
                            elif ((int(p[row,col,color])) > 144) and ((int(p[row,col,color])) <= 146):
                                q[row,col,color] = 144
                            elif ((int(p[row,col,color])) > 146) and ((int(p[row,col,color])) <= 148):
                                q[row,col,color] = 146
                            elif ((int(p[row,col,color])) > 148) and ((int(p[row,col,color])) <= 150):
                                q[row,col,color] = 148
                            elif ((int(p[row,col,color])) > 150) and ((int(p[row,col,color])) <= 152):
                                q[row,col,color] = 150
                            elif ((int(p[row,col,color])) > 152) and ((int(p[row,col,color])) <= 154):
                                q[row,col,color] = 152
                            elif ((int(p[row,col,color])) > 154) and ((int(p[row,col,color])) <= 156):
                                q[row,col,color] = 154
                            elif ((int(p[row,col,color])) > 156) and ((int(p[row,col,color])) <= 158):
                                q[row,col,color] = 156
                            elif ((int(p[row,col,color])) > 158) and ((int(p[row,col,color])) <= 160):
                                q[row,col,color] = 158
                            elif ((int(p[row,col,color])) > 160) and ((int(p[row,col,color])) <= 162):
                                q[row,col,color] = 160
                            elif ((int(p[row,col,color])) > 162) and ((int(p[row,col,color])) <= 164):
                                q[row,col,color] = 162
                            elif ((int(p[row,col,color])) > 164) and ((int(p[row,col,color])) <= 166):
                                q[row,col,color] = 164
                            elif ((int(p[row,col,color])) > 166) and ((int(p[row,col,color])) <= 168):
                                q[row,col,color] = 166
                            elif ((int(p[row,col,color])) > 168) and ((int(p[row,col,color])) <= 170):
                                q[row,col,color] = 168
                            elif ((int(p[row,col,color])) > 170) and ((int(p[row,col,color])) <= 172):
                                q[row,col,color] = 170
                            elif ((int(p[row,col,color])) > 172) and ((int(p[row,col,color])) <= 174):
                                q[row,col,color] = 172
                            elif ((int(p[row,col,color])) > 174) and ((int(p[row,col,color])) <= 176):
                                q[row,col,color] = 174
                            elif ((int(p[row,col,color])) > 176) and ((int(p[row,col,color])) <= 178):
                                q[row,col,color] = 176
                            elif ((int(p[row,col,color])) > 178) and ((int(p[row,col,color])) <= 180):
                                q[row,col,color] = 178
                            elif ((int(p[row,col,color])) > 180) and ((int(p[row,col,color])) <= 182):
                                q[row,col,color] = 180
                            elif ((int(p[row,col,color])) > 182) and ((int(p[row,col,color])) <= 184):
                                q[row,col,color] = 182
                            elif ((int(p[row,col,color])) > 184) and ((int(p[row,col,color])) <= 186):
                                q[row,col,color] = 184
                            elif ((int(p[row,col,color])) > 186) and ((int(p[row,col,color])) <= 188):
                                q[row,col,color] = 186
                            elif ((int(p[row,col,color])) > 188) and ((int(p[row,col,color])) <= 190):
                                q[row,col,color] = 188
                            elif ((int(p[row,col,color])) > 190) and ((int(p[row,col,color])) <= 192):
                                q[row,col,color] = 190
                            elif ((int(p[row,col,color])) > 192) and ((int(p[row,col,color])) <= 194):
                                q[row,col,color] = 192
                            elif ((int(p[row,col,color])) > 194) and ((int(p[row,col,color])) <= 196):
                                q[row,col,color] = 194
                            elif ((int(p[row,col,color])) > 196) and ((int(p[row,col,color])) <= 198):
                                q[row,col,color] = 196
                            elif ((int(p[row,col,color])) > 198) and ((int(p[row,col,color])) <= 200):
                                q[row,col,color] = 198
                            elif ((int(p[row,col,color])) > 200) and ((int(p[row,col,color])) <= 202):
                                q[row,col,color] = 200
                            elif ((int(p[row,col,color])) > 202) and ((int(p[row,col,color])) <= 204):
                                q[row,col,color] = 202
                            elif ((int(p[row,col,color])) > 204) and ((int(p[row,col,color])) <= 206):
                                q[row,col,color] = 204
                            elif ((int(p[row,col,color])) > 206) and ((int(p[row,col,color])) <= 208):
                                q[row,col,color] = 206
                            elif ((int(p[row,col,color])) > 208) and ((int(p[row,col,color])) <= 210):
                                q[row,col,color] = 208
                            elif ((int(p[row,col,color])) > 210) and ((int(p[row,col,color])) <= 212):
                                q[row,col,color] = 210
                            elif ((int(p[row,col,color])) > 212) and ((int(p[row,col,color])) <= 214):
                                q[row,col,color] = 212
                            elif ((int(p[row,col,color])) > 214) and ((int(p[row,col,color])) <= 216):
                                q[row,col,color] = 214
                            elif ((int(p[row,col,color])) > 216) and ((int(p[row,col,color])) <= 218):
                                q[row,col,color] = 216
                            elif ((int(p[row,col,color])) > 218) and ((int(p[row,col,color])) <= 220):
                                q[row,col,color] = 218
                            elif ((int(p[row,col,color])) > 220) and ((int(p[row,col,color])) <= 222):
                                q[row,col,color] = 220
                            elif ((int(p[row,col,color])) > 222) and ((int(p[row,col,color])) <= 224):
                                q[row,col,color] = 222
                            elif ((int(p[row,col,color])) > 224) and ((int(p[row,col,color])) <= 226):
                                q[row,col,color] = 224
                            elif ((int(p[row,col,color])) > 226) and ((int(p[row,col,color])) <= 228):
                                q[row,col,color] = 226
                            elif ((int(p[row,col,color])) > 228) and ((int(p[row,col,color])) <= 230):
                                q[row,col,color] = 228
                            elif ((int(p[row,col,color])) > 230) and ((int(p[row,col,color])) <= 232):
                                q[row,col,color] = 230
                            elif ((int(p[row,col,color])) > 232) and ((int(p[row,col,color])) <= 234):
                                q[row,col,color] = 232
                            elif ((int(p[row,col,color])) > 234) and ((int(p[row,col,color])) <= 236):
                                q[row,col,color] = 234
                            elif ((int(p[row,col,color])) > 236) and ((int(p[row,col,color])) <= 238):
                                q[row,col,color] = 236
                            elif ((int(p[row,col,color])) > 238) and ((int(p[row,col,color])) <= 240):
                                q[row,col,color] = 238
                            elif ((int(p[row,col,color])) > 240) and ((int(p[row,col,color])) <= 242):
                                q[row,col,color] = 240
                            elif ((int(p[row,col,color])) > 242) and ((int(p[row,col,color])) <= 244):
                                q[row,col,color] = 242
                            elif ((int(p[row,col,color])) > 244) and ((int(p[row,col,color])) <= 246):
                                q[row,col,color] = 244
                            elif ((int(p[row,col,color])) > 246) and ((int(p[row,col,color])) <= 248):
                                q[row,col,color] = 246
                            elif ((int(p[row,col,color])) > 248) and ((int(p[row,col,color])) <= 250):
                                q[row,col,color] = 248
                            elif ((int(p[row,col,color])) > 250) and ((int(p[row,col,color])) <= 252):
                                q[row,col,color] = 250
                            elif ((int(p[row,col,color])) > 252) and ((int(p[row,col,color])) <= 254):
                                q[row,col,color] = 252
                            else:
                                q[row,col,color] = 255
                img = q
                b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
                img = cv2.merge((r,g, b))
        cv2.imwrite("edit.jpg", q)

        txtnomum8 = Entry(rise17, width=25) # Crea un campo de entrada de datos
        txtnomum8.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomum8.insert(END, "edit.jpg")

        canvasum8 = Canvas(rise17, width=320, height=180)
        canvasum8.grid(column=1, row=2)

        im8 = Image.open("edit.jpg")
        im8 = im8.resize((320, 180), Image.ANTIALIAS)
        canvasum8.image = ImageTk.PhotoImage(im8)
        canvasum8.create_image(0, 0, image=canvasum8.image, anchor='nw')

        def descargainv8(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            rise17.destroy()
            rise17.update()

        btn_descargaum8 = Button(rise17, text="Descargar", command=lambda: descargainv8(str(txtnomum8.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaum8.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150
    #u = 2

    #lista = []
    #lista.append(txtt3)
    #lista.append(txtt32)

    btn_aceptar8 = Button(rise16, text="Ok", command=lambda: funcionumbral8(int(combo.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptar8.grid(column="1", row="5") # Posiciona el botón

def logic():
    print("logic")

    def cargar_logic_color_1():
        global check1
        global check2
        print("Cargar a color para el canvas 1")
        print("Cargar")
        file = filedialog.askopenfilename()
        im = Image.open(file)
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas1.image = ImageTk.PhotoImage(im)
        canvas1.create_image(0, 0, image=canvas1.image, anchor='nw')
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_COLOR)
        cv2.imwrite('current1.jpg', image)
        check1 = False
    
    def cargar_logic_color_2():
        global check1
        global check2
        print("Cargar a color para el canvas 2")
        print("Cargar")
        file = filedialog.askopenfilename()
        im = Image.open(file)
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas2.image = ImageTk.PhotoImage(im)
        canvas2.create_image(0, 0, image=canvas2.image, anchor='nw')
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_COLOR)
        cv2.imwrite('current2.jpg', image)
        check2 = False

    def cargar_logic_gris_1():
        global check1
        global check2
        print("Cargar a gris para el canvas 1")
        print("Cargar")
        file = filedialog.askopenfilename()
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite('current1.jpg', image)
        im = Image.open("current1.jpg")
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas1.image = ImageTk.PhotoImage(im)
        canvas1.create_image(0, 0, image=canvas1.image, anchor='nw')
        check1 = True

    def cargar_logic_gris_2():
        global check1
        global check2
        print("Cargar a gris para el canvas 1")
        file = filedialog.askopenfilename()
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite('current2.jpg', image)
        im = Image.open("current2.jpg")
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas2.image = ImageTk.PhotoImage(im)
        canvas2.create_image(0, 0, image=canvas2.image, anchor='nw')
        check2 = True

    def logicand():
        global check1
        global check2
        print("AND")

        risepregunta = Toplevel()
        risepregunta.title("AND")
        risepregunta.geometry("230x150")

        lblespacioand = Label(risepregunta, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblespacioand.grid(column=0, row=0) # Posiciona la etiqueta

        lbland = Label(risepregunta, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lbland.grid(column=1, row=1) # Posiciona la etiqueta

        txtand = Entry(risepregunta, width=25) # Crea un campo de entrada de datos
        txtand.grid(column=1, row=2) # Posiciona la entrada de texto

        def funcionumbraland(t):

            risepregunta.destroy()
            risepregunta.update()

            riseand = Toplevel()
            riseand.title("AND")
            riseand.geometry("320x250")

            int(t)

            p = cv2.imread('current1.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit1.jpg", q)

            p = cv2.imread('current2.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit2.jpg", q)

            txtnomumand = Entry(riseand, width=25) # Crea un campo de entrada de datos
            txtnomumand.grid(column=1, row=0) # Posiciona la entrada de texto
            txtnomumand.insert(END, "edit.jpg")

            canvasum = Canvas(riseand, width=320, height=180)
            canvasum.grid(column=1, row=2)

            #Aquí va la conversión del and, se debe descargar en edit.jpg
        
            #p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
            #r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
            p = io.imread("edit1.jpg")
            r = io.imread("edit2.jpg")
            p = cv2.resize(p  , (320 , 180))
            r = cv2.resize(r  , (320 , 180))
            q = p

            if (check1 == True and check2 == True):
            #for color in range(0,2):
                p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
                r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
                p = cv2.resize(p  , (320 , 180))
                r = cv2.resize(r  , (320 , 180))
                q = p
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) == (int(r[row,col]))):
                            q[row,col] = 255
                        else:
                            q[row,col] = 0
            else:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if (int(p[row,col,color]) == int(r[row,col,color])):
                                q[row,col,color] = 255
                            else:
                                q[row,col,color] = 0

            cv2.imwrite("edit.jpg", q)

            im = Image.open("edit.jpg")
            im = im.resize((320, 180), Image.ANTIALIAS)
            canvasum.image = ImageTk.PhotoImage(im)
            canvasum.create_image(0, 0, image=canvasum.image, anchor='nw')

            def descargainv(txtnom):
                image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
                cv2.imwrite(txtnom, image)
                print("descargada")
                riseand.destroy()
                riseand.update()

            btn_descargaand = Button(riseand, text="Descargar", command=lambda: descargainv(str(txtnomumand.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
            btn_descargaand.grid(column=1, row=30) # Posiciona el botón

        print("Umbral")
        t = 150

        btn_aceptarand = Button(risepregunta, text="Ok", command=lambda: funcionumbraland(int(txtand.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        #btn_aceptar = Button(rise2, text="Ok", command=cargar)
        btn_aceptarand.grid(column="1", row="3") # Posiciona el botón

    def logicor():
        print("OR")
        global check1
        global check2

        risepreguntaor = Toplevel()
        risepreguntaor.title("OR")
        risepreguntaor.geometry("230x150")

        lblespacioor = Label(risepreguntaor, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblespacioor.grid(column=0, row=0) # Posiciona la etiqueta

        lblor = Label(risepreguntaor, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblor.grid(column=1, row=1) # Posiciona la etiqueta

        txtor = Entry(risepreguntaor, width=25) # Crea un campo de entrada de datos
        txtor.grid(column=1, row=2) # Posiciona la entrada de texto

        def funcionumbralor(t):

            risepreguntaor.destroy()
            risepreguntaor.update()

            riseor = Toplevel()
            riseor.title("OR")
            riseor.geometry("320x250")

            int(t)

            p = cv2.imread('current1.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit1.jpg", q)

            p = cv2.imread('current2.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit2.jpg", q)

            txtnomumor = Entry(riseor, width=25) # Crea un campo de entrada de datos
            txtnomumor.grid(column=1, row=0) # Posiciona la entrada de texto
            txtnomumor.insert(END, "edit.jpg")

            canvasum = Canvas(riseor, width=320, height=180)
            canvasum.grid(column=1, row=2)

            #Aquí va la conversión del and, se debe descargar en edit.jpg
        
            #p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
            #r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
            p = io.imread("edit1.jpg")
            r = io.imread("edit2.jpg")
            p = cv2.resize(p  , (320 , 180))
            r = cv2.resize(r  , (320 , 180))
            q = p

            if (check1 == True and check2 == True):
            #for color in range(0,2):
                p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
                r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
                p = cv2.resize(p  , (320 , 180))
                r = cv2.resize(r  , (320 , 180))
                q = p
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if (((int(p[row,col])) == 255) or ((int(r[row,col])) == 255)):
                            q[row,col] = 255
                        else:
                            q[row,col] = 0
            else:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if (((int(p[row,col,color])) == 255) or ((int(r[row,col,color])) == 255)):
                                q[row,col,color] = 255
                            else:
                                q[row,col,color] = 0

            cv2.imwrite("edit.jpg", q)

            im = Image.open("edit.jpg")
            im = im.resize((320, 180), Image.ANTIALIAS)
            canvasum.image = ImageTk.PhotoImage(im)
            canvasum.create_image(0, 0, image=canvasum.image, anchor='nw')

            def descargainvor(txtnom):
                image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
                cv2.imwrite(txtnom, image)
                print("descargada")
                riseor.destroy()
                riseor.update()

            btn_descargaor = Button(riseor, text="Descargar", command=lambda: descargainvor(str(txtnomumor.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
            btn_descargaor.grid(column=1, row=30) # Posiciona el botón

        print("Umbral")
        t = 150

        btn_aceptaror = Button(risepreguntaor, text="Ok", command=lambda: funcionumbralor(int(txtor.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        #btn_aceptar = Button(rise2, text="Ok", command=cargar)
        btn_aceptaror.grid(column="1", row="3") # Posiciona el botón

    def logicnot():
        print("NOT")
        global check1
        global check2

        risepreguntanot = Toplevel()
        risepreguntanot.title("NOT")
        risepreguntanot.geometry("230x150")

        lblespacionot = Label(risepreguntanot, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblespacionot.grid(column=0, row=0) # Posiciona la etiqueta

        lblnot = Label(risepreguntanot, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblnot.grid(column=1, row=1) # Posiciona la etiqueta

        txtnot = Entry(risepreguntanot, width=25) # Crea un campo de entrada de datos
        txtnot.grid(column=1, row=2) # Posiciona la entrada de texto

        def funcionumbralnot(t):

            risepreguntanot.destroy()
            risepreguntanot.update()

            risenot = Toplevel()
            risenot.title("NOT")
            risenot.geometry("320x250")

            int(t)

            p = cv2.imread('current1.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit1.jpg", q)

            p = cv2.imread('current2.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit2.jpg", q)

            txtnomumnot = Entry(risenot, width=25) # Crea un campo de entrada de datos
            txtnomumnot.grid(column=1, row=0) # Posiciona la entrada de texto
            txtnomumnot.insert(END, "edit.jpg")

            canvasum = Canvas(risenot, width=320, height=180)
            canvasum.grid(column=1, row=2)

            #Aquí va la conversión del and, se debe descargar en edit.jpg
        
            #p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
            #r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
            p = io.imread("edit1.jpg")
            r = io.imread("edit2.jpg")
            p = cv2.resize(p  , (320 , 180))
            r = cv2.resize(r  , (320 , 180))
            q = p

            if check1 == True:
            #for color in range(0,2):
                p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
                r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
                p = cv2.resize(p  , (320 , 180))
                r = cv2.resize(r  , (320 , 180))
                q = p
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if ((int(p[row,col])) == 255):
                            q[row,col] = 0
                        else:
                            q[row,col] = 255
            else:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if (int(p[row,col,color]) == 255):
                                q[row,col,color] = 0
                            else:
                                q[row,col,color] = 255

            cv2.imwrite("edit.jpg", q)

            im = Image.open("edit.jpg")
            im = im.resize((320, 180), Image.ANTIALIAS)
            canvasum.image = ImageTk.PhotoImage(im)
            canvasum.create_image(0, 0, image=canvasum.image, anchor='nw')

            def descargainvnot(txtnom):
                image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
                cv2.imwrite(txtnom, image)
                print("descargada")
                risenot.destroy()
                risenot.update()

            btn_descarganot = Button(risenot, text="Descargar", command=lambda: descargainvnot(str(txtnomumnot.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
            btn_descarganot.grid(column=1, row=30) # Posiciona el botón

        print("Umbral")
        t = 150

        btn_aceptarnot = Button(risepreguntanot, text="Ok", command=lambda: funcionumbralnot(int(txtnot.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        #btn_aceptar = Button(rise2, text="Ok", command=cargar)
        btn_aceptarnot.grid(column="1", row="3") # Posiciona el botón

    def logicxor():
        print("XOR")
        global check1
        global check2

        risepreguntaxor = Toplevel()
        risepreguntaxor.title("XOR")
        risepreguntaxor.geometry("230x150")

        lblespacioxor = Label(risepreguntaxor, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblespacioxor.grid(column=0, row=0) # Posiciona la etiqueta

        lblxor = Label(risepreguntaxor, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
        lblxor.grid(column=1, row=1) # Posiciona la etiqueta

        txtxor = Entry(risepreguntaxor, width=25) # Crea un campo de entrada de datos
        txtxor.grid(column=1, row=2) # Posiciona la entrada de texto

        def funcionumbralxor(t):

            risepreguntaxor.destroy()
            risepreguntaxor.update()

            risexor = Toplevel()
            risexor.title("XOR")
            risexor.geometry("320x250")

            int(t)

            p = cv2.imread('current1.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit1.jpg", q)

            p = cv2.imread('current2.jpg', cv2.IMREAD_COLOR)

            q = p
            idx = p <= t 
            q[idx] = 0
            idx = p > t
            q[idx] = 255

            cv2.imwrite("edit2.jpg", q)

            txtnomumxor = Entry(risexor, width=25) # Crea un campo de entrada de datos
            txtnomumxor.grid(column=1, row=0) # Posiciona la entrada de texto
            txtnomumxor.insert(END, "edit.jpg")

            canvasum = Canvas(risexor, width=320, height=180)
            canvasum.grid(column=1, row=2)

            #Aquí va la conversión del and, se debe descargar en edit.jpg
        
            #p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
            #r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
            p = io.imread("edit1.jpg")
            r = io.imread("edit2.jpg")
            p = cv2.resize(p  , (320 , 180))
            r = cv2.resize(r  , (320 , 180))
            q = p

            if (check1 == True and check2 == True):
            #for color in range(0,2):
                p = cv2.imread('edit1.jpg', cv2.IMREAD_GRAYSCALE)
                r = cv2.imread('edit2.jpg', cv2.IMREAD_GRAYSCALE)
                p = cv2.resize(p  , (320 , 180))
                r = cv2.resize(r  , (320 , 180))
                q = p
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        if (((int(p[row,col])) == 255) and ((int(r[row,col])) == 255)):
                            q[row, col] = 0
                        elif (((int(p[row,col])) == 255) or ((int(r[row,col])) == 255)):
                            q[row,col] = 255
                        else:
                            q[row,col] = 0
            else:
                for row in range(p.shape[0]):
                    for col in range(p.shape[1]):
                        for color in range(3):
                            if (((int(p[row,col,color])) == 255) and ((int(r[row,col,color])) == 255)):
                                q[row, col,color] = 0
                            elif (((int(p[row,col,color])) == 255) or ((int(r[row,col,color])) == 255)):
                                q[row,col,color] = 255
                            else:
                                q[row,col,color] = 0

            cv2.imwrite("edit.jpg", q)

            im = Image.open("edit.jpg")
            im = im.resize((320, 180), Image.ANTIALIAS)
            canvasum.image = ImageTk.PhotoImage(im)
            canvasum.create_image(0, 0, image=canvasum.image, anchor='nw')

            def descargainvxor(txtnom):
                image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
                cv2.imwrite(txtnom, image)
                print("descargada")
                risexor.destroy()
                risexor.update()

            btn_descargaxor = Button(risexor, text="Descargar", command=lambda: descargainvxor(str(txtnomumxor.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
            btn_descargaxor.grid(column=1, row=30) # Posiciona el botón

        print("Umbral")
        t = 150

        btn_aceptarxor = Button(risepreguntaxor, text="Ok", command=lambda: funcionumbralxor(int(txtxor.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        #btn_aceptar = Button(rise2, text="Ok", command=cargar)
        btn_aceptarxor.grid(column="1", row="3") # Posiciona el botón

    logico = Toplevel()
    logico.title("Operaciones Lógicas")
    logico.geometry("812x350")

    lbltit = Label(logico, text="Operaciones Lógicas", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbltit.grid(column=2, row=1) # Posiciona la etiqueta

    canvas1 = Canvas(logico, width=320, height=180)
    canvas1.grid(column=1, row=2)

    btn_can1 = Button(logico, text="Cargar a color", command=cargar_logic_color_1) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can1.grid(column=1, row=3) # Posiciona el botón

    btn_can1g = Button(logico, text="Cargar a gris", command=cargar_logic_gris_1) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can1g.grid(column=1, row=4) # Posiciona el botón

    canvas2 = Canvas(logico, width=320, height=180)
    canvas2.grid(column=3, row=2)

    btn_can2 = Button(logico, text="Cargar a color", command=cargar_logic_color_2) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can2.grid(column=3, row=3) # Posiciona el botón

    btn_can2g = Button(logico, text="Cargar a gris", command=cargar_logic_gris_2) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can2g.grid(column=3, row=4) # Posiciona el botón

    logic_and = Button(logico, text="AND", command=logicand) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    logic_and.grid(column=2, row=3) # Posiciona el botón

    logic_or = Button(logico, text="OR", command=logicor) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    logic_or.grid(column=2, row=4) # Posiciona el botón

    logic_not = Button(logico, text="NOT", command=logicnot) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    logic_not.grid(column=2, row=5) # Posiciona el botón

    logic_xor = Button(logico, text="XOR", command=logicxor) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    logic_xor.grid(column=2, row=6) # Posiciona el botón

def suma():
    print("suma")
    global gris

    risesuma = Toplevel()
    risesuma.title("Suma")
    risesuma.geometry("230x150")

    lblespaciosuma = Label(risesuma, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespaciosuma.grid(column=0, row=0) # Posiciona la etiqueta

    lblsuma = Label(risesuma, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblsuma.grid(column=1, row=1) # Posiciona la etiqueta

    txtsuma = Entry(risesuma, width=25) # Crea un campo de entrada de datos
    txtsuma.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbralsuma(t):

        risesuma.destroy()
        risesuma.update()

        risesumares = Toplevel()
        risesumares.title("Suma")
        risesumares.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((p[row,col] + t) > 255):
                        q[row,col] = 255
                    else:
                        q[row,col] = (int(p[row, col]) + t) 
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((p[row,col,color] + t) > 255):
                            q[row,col,color] = 255
                        else:
                            q[row,col,color] = (int(p[row, col,color]) + t) 
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomsuma = Entry(risesumares, width=25) # Crea un campo de entrada de datos
        txtnomsuma.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomsuma.insert(END, "edit.jpg")

        canvasuma = Canvas(risesumares, width=320, height=180)
        canvasuma.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvasuma.image = ImageTk.PhotoImage(im2)
        canvasuma.create_image(0, 0, image=canvasuma.image, anchor='nw')

        def descargainvsuma(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risesumares.destroy()
            risesumares.update()

        btn_descargaumsuma = Button(risesumares, text="Descargar", command=lambda: descargainvsuma(str(txtnomsuma.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumsuma.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptarsuma = Button(risesuma, text="Ok", command=lambda: funcionumbralsuma(int(txtsuma.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptarsuma.grid(column="1", row="3") # Posiciona el botón

def resta():
    print("Resta")
    global gris

    riseresta = Toplevel()
    riseresta.title("Resta")
    riseresta.geometry("230x150")

    lblespacioresta = Label(riseresta, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespacioresta.grid(column=0, row=0) # Posiciona la etiqueta

    lblresta = Label(riseresta, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblresta.grid(column=1, row=1) # Posiciona la etiqueta

    txtresta = Entry(riseresta, width=25) # Crea un campo de entrada de datos
    txtresta.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbralresta(t):

        riseresta.destroy()
        riseresta.update()

        riserestares = Toplevel()
        riserestares.title("Resta")
        riserestares.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(p[row,col]) - t) < 0):
                        q[row,col] = 0
                    else:
                        q[row,col] = int(p[row, col]) - t
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(p[row,col,color]) - t) < 0):
                            q[row,col,color] = 0
                        else:
                            q[row,col,color] = int(p[row, col,color]) - t
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomresta = Entry(riserestares, width=25) # Crea un campo de entrada de datos
        txtnomresta.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomresta.insert(END, "edit.jpg")

        canvaresta = Canvas(riserestares, width=320, height=180)
        canvaresta.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvaresta.image = ImageTk.PhotoImage(im2)
        canvaresta.create_image(0, 0, image=canvaresta.image, anchor='nw')

        def descargainvresta(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            riserestares.destroy()
            riserestares.update()

        btn_descargaumresta = Button(riserestares, text="Descargar", command=lambda: descargainvresta(str(txtnomresta.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumresta.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptarresta = Button(riseresta, text="Ok", command=lambda: funcionumbralresta(int(txtresta.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptarresta.grid(column="1", row="3") # Posiciona el botón

def multiplicacion():
    print("Multiplicación")
    global gris

    risemult = Toplevel()
    risemult.title("Multiplicación")
    risemult.geometry("230x150")

    lblespaciomult = Label(risemult, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespaciomult.grid(column=0, row=0) # Posiciona la etiqueta

    lblmult = Label(risemult, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblmult.grid(column=1, row=1) # Posiciona la etiqueta

    txtmult = Entry(risemult, width=25) # Crea un campo de entrada de datos
    txtmult.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbralmult(t):

        risemult.destroy()
        risemult.update()

        risemultres = Toplevel()
        risemultres.title("Multiplicación")
        risemultres.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    q[row,col] = (int(p[row, col]) * t) / 2
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        q[row,col,color] = (int(p[row,col,color]) * t) / 2
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnommult = Entry(risemultres, width=25) # Crea un campo de entrada de datos
        txtnommult.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnommult.insert(END, "edit.jpg")

        canvamult = Canvas(risemultres, width=320, height=180)
        canvamult.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvamult.image = ImageTk.PhotoImage(im2)
        canvamult.create_image(0, 0, image=canvamult.image, anchor='nw')

        def descargainvresta(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risemultres.destroy()
            risemultres.update()

        btn_descargaummult = Button(risemultres, text="Descargar", command=lambda: descargainvmult(str(txtnommult.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaummult.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptarmult = Button(risemult, text="Ok", command=lambda: funcionumbralmult(int(txtmult.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptarmult.grid(column="1", row="3") # Posiciona el botón

def division():
    print("División")
    global gris

    risediv = Toplevel()
    risediv.title("División")
    risediv.geometry("230x150")

    lblespaciodiv = Label(risediv, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespaciodiv.grid(column=0, row=0) # Posiciona la etiqueta

    lbldiv = Label(risediv, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbldiv.grid(column=1, row=1) # Posiciona la etiqueta

    txtdiv = Entry(risediv, width=25) # Crea un campo de entrada de datos
    txtdiv.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbraldiv(t):

        risediv.destroy()
        risediv.update()

        risedivres = Toplevel()
        risedivres.title("División")
        risedivres.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (t == 0):
                        q[row,col] = 0
                    else:
                        q[row,col] = p[row,col] / t
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (t == 0):
                            q[row,col,color] = 0
                        else:
                            q[row,col,color] = p[row,col,color] / t

            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomdiv = Entry(risedivres, width=25) # Crea un campo de entrada de datos
        txtnomdiv.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomdiv.insert(END, "edit.jpg")

        canvadiv = Canvas(risedivres, width=320, height=180)
        canvadiv.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvadiv.image = ImageTk.PhotoImage(im2)
        canvadiv.create_image(0, 0, image=canvadiv.image, anchor='nw')

        def descargainvresta(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risedivres.destroy()
            risedivres.update()

        btn_descargaumdiv = Button(risedivres, text="Descargar", command=lambda: descargainvdiv(str(txtnomdiv.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumdiv.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptardiv = Button(risediv, text="Ok", command=lambda: funcionumbraldiv(int(txtdiv.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptardiv.grid(column="1", row="3") # Posiciona el botón

def potencia():
    print("Potencia")
    global gris

    risepot = Toplevel()
    risepot.title("Potencia")
    risepot.geometry("230x150")

    lblespaciopot = Label(risepot, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespaciopot.grid(column=0, row=0) # Posiciona la etiqueta

    lblpot = Label(risepot, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblpot.grid(column=1, row=1) # Posiciona la etiqueta

    txtpot = Entry(risepot, width=25) # Crea un campo de entrada de datos
    txtpot.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbralpot(t):

        risepot.destroy()
        risepot.update()

        risepotres = Toplevel()
        risepotres.title("Potencia")
        risepotres.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if (pow(int(p[row,col]),t) > 255):
                        q[row,col] = 255
                    else:
                        q[row,col] = pow(int(p[row,col]),t)

            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if (pow(int(p[row,col,color]),t) > 255):
                            q[row,col,color] = 255
                        else:
                            q[row,col,color] = pow(int(p[row,col,color]),t)
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnompot = Entry(risepotres, width=25) # Crea un campo de entrada de datos
        txtnompot.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnompot.insert(END, "edit.jpg")

        canvapot = Canvas(risepotres, width=320, height=180)
        canvapot.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvapot.image = ImageTk.PhotoImage(im2)
        canvapot.create_image(0, 0, image=canvapot.image, anchor='nw')

        def descargainvpot(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risepotres.destroy()
            risepotres.update()

        btn_descargaumpot = Button(risepotres, text="Descargar", command=lambda: descargainvpot(str(txtnompot.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumpot.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptarpot = Button(risepot, text="Ok", command=lambda: funcionumbralpot(int(txtpot.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptarpot.grid(column="1", row="3") # Posiciona el botón

def logaritmo():
    print("logaritmo")
    global gris

    riselog = Toplevel()
    riselog.title("Logaritmo")
    riselog.geometry("230x150")

    lblespaciolog = Label(riselog, text="  ", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lblespaciolog.grid(column=0, row=0) # Posiciona la etiqueta

    lbllog = Label(riselog, text="Dame un valor del 1 al 254", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbllog.grid(column=1, row=1) # Posiciona la etiqueta

    txtlog = Entry(riselog, width=25) # Crea un campo de entrada de datos
    txtlog.grid(column=1, row=2) # Posiciona la entrada de texto

    def funcionumbrallog(t):

        riselog.destroy()
        riselog.update()

        riselogres = Toplevel()
        riselogres.title("Logaritmo")
        riselogres.geometry("320x250")

        int(t)
        print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current.jpg")

        if gris == True:
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    p[row,col] += 1
                    if (int(p[row,col]) == 0):
                        q[row,col] = 0
                    else:
                        q[row,col] = round(np.log(int(p[row,col]))) * t

            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        p[row,col,color] += 1
                        if (int(p[row,col,color]) == 0):
                            q[row,col,color] = 0
                        else:
                            q[row,col,color] = round(np.log(int(p[row,col,color]))) * t
                        #print(q[row,col, color])
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomlog = Entry(riselogres, width=25) # Crea un campo de entrada de datos
        txtnomlog.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomlog.insert(END, "edit.jpg")

        canvalog = Canvas(riselogres, width=320, height=180)
        canvalog.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvalog.image = ImageTk.PhotoImage(im2)
        canvalog.create_image(0, 0, image=canvalog.image, anchor='nw')

        def descargainvlog(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            riselogres.destroy()
            riselogres.update()

        btn_descargaumlog = Button(riselogres, text="Descargar", command=lambda: descargainvlog(str(txtnomlog.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumlog.grid(column=1, row=30) # Posiciona el botón

    print("Umbral")
    t = 150

    btn_aceptarlog = Button(riselog, text="Ok", command=lambda: funcionumbrallog(int(txtlog.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    #btn_aceptar = Button(rise2, text="Ok", command=cargar)
    btn_aceptarlog.grid(column="1", row="3") # Posiciona el botón

def imag2():
    print("Imag 2")
    def cargar_logic_color_1():
        global check1
        global check2
        print("Cargar a color para el canvas 1")
        print("Cargar")
        file = filedialog.askopenfilename()
        im = Image.open(file)
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas1.image = ImageTk.PhotoImage(im)
        canvas1.create_image(0, 0, image=canvas1.image, anchor='nw')
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_COLOR)
        cv2.imwrite('current1.jpg', image)
        check1 = False
    
    def cargar_logic_color_2():
        global check1
        global check2
        print("Cargar a color para el canvas 2")
        print("Cargar")
        file = filedialog.askopenfilename()
        im = Image.open(file)
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas2.image = ImageTk.PhotoImage(im)
        canvas2.create_image(0, 0, image=canvas2.image, anchor='nw')
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_COLOR)
        cv2.imwrite('current2.jpg', image)
        check2 = False

    def cargar_logic_gris_1():
        global check1
        global check2
        print("Cargar a gris para el canvas 1")
        print("Cargar")
        file = filedialog.askopenfilename()
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite('current1.jpg', image)
        im = Image.open("current1.jpg")
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas1.image = ImageTk.PhotoImage(im)
        canvas1.create_image(0, 0, image=canvas1.image, anchor='nw')
        check1 = True

    def cargar_logic_gris_2():
        global check1
        global check2
        print("Cargar a gris para el canvas 1")
        file = filedialog.askopenfilename()
        image = cv2.imread(os.path.abspath(file), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite('current2.jpg', image)
        im = Image.open("current2.jpg")
        im = im.resize((320, 180), Image.ANTIALIAS)
        canvas2.image = ImageTk.PhotoImage(im)
        canvas2.create_image(0, 0, image=canvas2.image, anchor='nw')
        check2 = True

    def suma2():
        global check1
        global check2
        print("suma")
        risesumares2 = Toplevel()
        risesumares2.title("Suma")
        risesumares2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    q[row,col] = (int(p[row, col]) + int(r[row,col])) / 2
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        q[row,col,color] = (int(p[row,col,color]) + int(r[row,col,color])) / 2
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomsuma2 = Entry(risesumares2, width=25) # Crea un campo de entrada de datos
        txtnomsuma2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomsuma2.insert(END, "edit.jpg")

        canvasuma2 = Canvas(risesumares2, width=320, height=180)
        canvasuma2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvasuma2.image = ImageTk.PhotoImage(im2)
        canvasuma2.create_image(0, 0, image=canvasuma2.image, anchor='nw')

        def descargainvsuma2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risesumares2.destroy()
            risesumares2.update()

        btn_descargaumsuma2 = Button(risesumares2, text="Descargar", command=lambda: descargainvsuma2(str(txtnomsuma2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumsuma2.grid(column=1, row=30) # Posiciona el botón

    def resta2():
        print("resta")
        global check1
        global check2

        riserestares2 = Toplevel()
        riserestares2.title("Resta")
        riserestares2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(p[row,col]) - int(r[row,col])) <= 0):
                        q[row,col] = 0
                    else:
                        q[row,col] = (int(p[row, col]) - int(r[row,col])) 
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(p[row,col,color]) - int(r[row,col,color])) <= 0):
                            q[row,col,color] = 0
                        else:
                            q[row,col,color] = (int(p[row,col,color]) - int(r[row,col,color]))
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomresta2 = Entry(riserestares2, width=25) # Crea un campo de entrada de datos
        txtnomresta2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomresta2.insert(END, "edit.jpg")

        canvaresta2 = Canvas(riserestares2, width=320, height=180)
        canvaresta2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvaresta2.image = ImageTk.PhotoImage(im2)
        canvaresta2.create_image(0, 0, image=canvaresta2.image, anchor='nw')

        def descargainvresta2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            riserestares2.destroy()
            riserestares2.update()

        btn_descargaumresta2 = Button(riserestares2, text="Descargar", command=lambda: descargainvresta2(str(txtnomresta2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumresta2.grid(column=1, row=30) # Posiciona el botón

    def mult():
        print("Multiplicación")
        global check1
        global check2

        risemultires2 = Toplevel()
        risemultires2.title("Multiplicación")
        risemultires2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(p[row,col]) * int(r[row,col])) > 255):
                        q[row,col] = 255
                    else:
                        q[row,col] = (int(p[row, col]) * int(r[row,col])) 
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(p[row,col,color]) * int(r[row,col,color])) > 255):
                            q[row,col,color] = 255
                        else:
                            q[row,col,color] = (int(p[row,col,color]) * int(r[row,col,color]))
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnommulti2 = Entry(risemultires2, width=25) # Crea un campo de entrada de datos
        txtnommulti2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnommulti2.insert(END, "edit.jpg")

        canvamulti2 = Canvas(risemultires2, width=320, height=180)
        canvamulti2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvamulti2.image = ImageTk.PhotoImage(im2)
        canvamulti2.create_image(0, 0, image=canvamulti2.image, anchor='nw')

        def descargainvmulti2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risemultires2.destroy()
            risemultires2.update()

        btn_descargaummulti2 = Button(risemultires2, text="Descargar", command=lambda: descargainvmulti2(str(txtnommulti2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaummulti2.grid(column=1, row=30) # Posiciona el botón

    def div():
        print("División")
        global check1
        global check2

        risedivres2 = Toplevel()
        risedivres2.title("División")
        risedivres2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(r[row,col])) == 0):
                        q[row,col] = 0
                    else:
                        q[row,col] = (int(p[row, col]) / int(r[row,col])) 
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(r[row,col,color])) == 0):
                            q[row,col,color] = 0
                        else:
                            q[row,col,color] = (int(p[row,col,color]) / int(r[row,col,color]))
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomdiv2 = Entry(risedivres2, width=25) # Crea un campo de entrada de datos
        txtnomdiv2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomdiv2.insert(END, "edit.jpg")

        canvadiv2 = Canvas(risedivres2, width=320, height=180)
        canvadiv2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvadiv2.image = ImageTk.PhotoImage(im2)
        canvadiv2.create_image(0, 0, image=canvadiv2.image, anchor='nw')

        def descargainvdiv2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risedivres2.destroy()
            risedivres2.update()

        btn_descargaumdiv2 = Button(risedivres2, text="Descargar", command=lambda: descargainvdiv2(str(txtnomdiv2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumdiv2.grid(column=1, row=30) # Posiciona el botón

    def abso():
        print("Valor absoluto")
        global check1
        global check2

        riseabsores2 = Toplevel()
        riseabsores2.title("Absoluto")
        riseabsores2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    q[row,col] = abs((int(q[row,col]))-(int(r[row,col])))
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        q[row,col,color] = abs((int(q[row,col,color]))-(int(r[row,col,color])))
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnomabso2 = Entry(riseabsores2, width=25) # Crea un campo de entrada de datos
        txtnomabso2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnomabso2.insert(END, "edit.jpg")

        canvaabso2 = Canvas(riseabsores2, width=320, height=180)
        canvaabso2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvaabso2.image = ImageTk.PhotoImage(im2)
        canvaabso2.create_image(0, 0, image=canvaabso2.image, anchor='nw')

        def descargainvabso2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            riseabsores2.destroy()
            riseabsores2.update()

        btn_descargaumabso2 = Button(riseabsores2, text="Descargar", command=lambda: descargainvabso2(str(txtnomabso2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaumabso2.grid(column=1, row=30) # Posiciona el botón

    def maxi():
        print("Máximo")
        global check1
        global check2

        risemaxres2 = Toplevel()
        risemaxres2.title("Máximo")
        risemaxres2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(p[row,col])) >= int(r[row,col])):
                        q[row,col] = p[row,col]
                    else:
                        q[row,col] = r[row,col]
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(p[row,col,color])) >= int(r[row,col,color])):
                            q[row,col,color] = p[row,col,color]
                        else:
                            q[row,col,color] = r[row,col,color]
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnommax2 = Entry(risemaxres2, width=25) # Crea un campo de entrada de datos
        txtnommax2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnommax2.insert(END, "edit.jpg")

        canvamax2 = Canvas(risemaxres2, width=320, height=180)
        canvamax2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvamax2.image = ImageTk.PhotoImage(im2)
        canvamax2.create_image(0, 0, image=canvamax2.image, anchor='nw')

        def descargainvmax2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            risemaxres2.destroy()
            risemaxres2.update()

        btn_descargaummax2 = Button(risemaxres2, text="Descargar", command=lambda: descargainvmax2(str(txtnommax2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaummax2.grid(column=1, row=30) # Posiciona el botón
    
    def mini():
        print("Mínimo")
        global check1
        global check2

        riseminres2 = Toplevel()
        riseminres2.title("Mínimo")
        riseminres2.geometry("320x250")

        #int(t)
        #print(t)

        #p = cv2.imread('current.jpg', cv2.IMREAD_COLOR)
        p = io.imread("current1.jpg")
        r = io.imread("current2.jpg")
        p = cv2.resize(p  , (320 , 180))
        r = cv2.resize(r  , (320 , 180))
        q = p

        if ((check1 == True) and (check2 == True)):
            q = p
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    if ((int(p[row,col])) <= int(r[row,col])):
                        q[row,col] = p[row,col]
                    else:
                        q[row,col] = r[row,col]
            img = q

        else:
            q = p
            #for color in range(0, 2):
            for row in range(p.shape[0]):
                for col in range(p.shape[1]):
                    for color in range(3):
                        if ((int(p[row,col,color])) <= int(r[row,col,color])):
                            q[row,col,color] = p[row,col,color]
                        else:
                            q[row,col,color] = r[row,col,color]
            img = q
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            img = cv2.merge((r,g, b))

        cv2.imwrite("edit.jpg", img)

        txtnommin2 = Entry(riseminres2, width=25) # Crea un campo de entrada de datos
        txtnommin2.grid(column=1, row=0) # Posiciona la entrada de texto
        txtnommin2.insert(END, "edit.jpg")

        canvamin2 = Canvas(riseminres2, width=320, height=180)
        canvamin2.grid(column=1, row=2)

        im2 = Image.open("edit.jpg")
        im2 = im2.resize((320, 180), Image.ANTIALIAS)
        canvamin2.image = ImageTk.PhotoImage(im2)
        canvamin2.create_image(0, 0, image=canvamin2.image, anchor='nw')

        def descargainvmin2(txtnom):
            image = cv2.imread("edit.jpg", cv2.IMREAD_COLOR)
            cv2.imwrite(txtnom, image)
            print("descargada")
            riseminres2.destroy()
            riseminres2.update()

        btn_descargaummin2 = Button(riseminres2, text="Descargar", command=lambda: descargainvmin2(str(txtnommin2.get()))) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
        btn_descargaummin2.grid(column=1, row=30) # Posiciona el botón

    imag2 = Toplevel()
    imag2.title("Aritmética")
    imag2.geometry("732x450")

    lbltit = Label(imag2, text="Aritmética", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
    lbltit.grid(column=2, row=1) # Posiciona la etiqueta

    canvas1 = Canvas(imag2, width=320, height=180)
    canvas1.grid(column=1, row=2)

    btn_can1 = Button(imag2, text="Cargar a color", command=cargar_logic_color_1) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can1.grid(column=1, row=3) # Posiciona el botón

    btn_can1g = Button(imag2, text="Cargar a gris", command=cargar_logic_gris_1) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can1g.grid(column=1, row=4) # Posiciona el botón

    canvas2 = Canvas(imag2, width=320, height=180)
    canvas2.grid(column=3, row=2)

    btn_can2 = Button(imag2, text="Cargar a color", command=cargar_logic_color_2) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can2.grid(column=3, row=3) # Posiciona el botón

    btn_can2g = Button(imag2, text="Cargar a gris", command=cargar_logic_gris_2) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    btn_can2g.grid(column=3, row=4) # Posiciona el botón

    imag2_suma = Button(imag2, text="Suma", command=suma2) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=5) # Posiciona el botón

    imag2_suma = Button(imag2, text="Resta", command=resta2) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=6) # Posiciona el botón

    imag2_suma = Button(imag2, text="Multiplicación", command=mult) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=7) # Posiciona el botón

    imag2_suma = Button(imag2, text="División", command=div) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=8) # Posiciona el botón

    imag2_suma = Button(imag2, text="Absoluto", command=abso) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=9) # Posiciona el botón

    imag2_suma = Button(imag2, text="Máximo", command=maxi) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=10) # Posiciona el botón

    imag2_suma = Button(imag2, text="Mínimo", command=mini) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
    imag2_suma.grid(column=2, row=11) # Posiciona el botón

gris = False
check1 = False
check2 = False
    
window = Tk()
window.title("Retrica 2021") # Define el título de la ventana
window.geometry('322x750')

#window.call('wm', 'iconphoto', window._w, PhotoImage(file='jocheem.jpg'))
# window.iconbitmap("jocheem.ico")

lbl = Label(window, text="Efectos", font=("Arial Bold", 12)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
lbl.grid(column=1, row=0) # Posiciona la etiqueta

btn_carga = Button(window, text="Cargar a color", command=cargar, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_carga.grid(column=1, row=1) # Posiciona el botón

btn_cargagris = Button(window, text="Cargar en grises", command=cargargris, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_cargagris.grid(column=1, row=2) # Posiciona el botón

#Create a canvas
canvas = Canvas(window, width=320, height=180)
canvas.grid(column=1, row=3)

lbl = Label(window, text="Individual", font=("Arial Bold", 10)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
lbl.grid(column=1, row=4) # Posiciona la etiqueta

btn_invertir = Button(window, text="Invertir", command=invertir, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_invertir.grid(column=1, row=5) # Posiciona el botón

btn_umbral = Button(window, text="Umbral", command=umbral, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_umbral.grid(column=1, row=6) # Posiciona el botón

btn_umbralinv = Button(window, text="Umbral Invertido", command=umbralinv, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_umbralinv.grid(column=1, row=7) # Posiciona el botón

btn_umbralbin = Button(window, text="Umbral binario", command=umbralbin, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_umbralbin.grid(column=1, row=8) # Posiciona el botón

btn_umbralbininv = Button(window, text="Umbral binario Invertido", command=umbralbininv, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_umbralbininv.grid(column=1, row=9) # Posiciona el botón

btn_umbralgray = Button(window, text="Umbral grises", command=umbralgray, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_umbralgray.grid(column=1, row=10) # Posiciona el botón

btn_umbralgrayinv = Button(window, text="Umbral grises inv", command=umbralgrayinv, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_umbralgrayinv.grid(column=1, row=11) # Posiciona el botón

btn_extension = Button(window, text="Extensión", command=extension, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_extension.grid(column=1, row=12) # Posiciona el botón

btn_niveles = Button(window, text="Reducción de nivel", command=niveles, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_niveles.grid(column=1, row=13) # Posiciona el botón

btn_suma = Button(window, text="Suma", command=suma, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_suma.grid(column=1, row=14) # Posiciona el botón

btn_resta = Button(window, text="Resta", command=resta, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_resta.grid(column=1, row=15) # Posiciona el botón

btn_multiplicacion = Button(window, text="Multiplicación", command=multiplicacion, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_multiplicacion.grid(column=1, row=16) # Posiciona el botón

btn_division = Button(window, text="División", command=division, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_division.grid(column=1, row=17) # Posiciona el botón

btn_potencia = Button(window, text="Potencia", command=potencia, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_potencia.grid(column=1, row=18) # Posiciona el botón

btn_logaritmo = Button(window, text="Logaritmo", command=logaritmo, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_logaritmo.grid(column=1, row=19) # Posiciona el botón

lbl = Label(window, text="Combo", font=("Arial Bold", 10)) # Crea y define lo que dice la etiqueta, agrega una fuente y tamaño
lbl.grid(column=1, row=20) # Posiciona la etiqueta

btn_imag2 = Button(window, text="Aritmética 2", command=imag2, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_imag2.grid(column=1, row=21) # Posiciona el botón

btn_logic = Button(window, text="Operaciones Lógicas", command=logic, width=20) # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
btn_logic.grid(column=1, row=22) # Posiciona el botón

#selected = IntVar()
#rad1 = Radiobutton(window, text="ci", value = 0, variable=selected) # Crea un radio buttón
#rad2 = Radiobutton(window, text="non", value = 1, variable=selected)
#rad1.grid(column=3, row=2) # Posiciona un radio button
#rad2.grid(column=3, row=3)

#btn = Button(window, text="ok jusgame") # Crea un botón, le pone texto. También seleccionamos lo que hará al ser seleccionado
#btn.grid(column=1, row=5) # Posiciona el botón

#p1 = PhotoImage(file="jocheem.jpg")
# Icon set for program window
#window.iconphoto(False, p1)
window.mainloop()