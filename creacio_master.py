#!/usr/bin/env python3
#coding=utf-8
#Created on 11 dec. 2020 - by Daniel González Martínez
#creacio_master.py

#http://web.archive.org/web/20130115175340/http://nadiana.com/pil-tutorial-basic-advanced-drawing
#https://pythonexamples.org/python-pillow-flip-image-vertical-horizontal/
#https://automatetheboringstuff.com/chapter17/#calibre_link-135

#Formula per extreure l'angle en base a 3 coordenades d'un objecte 2D.
#https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd

#Importació de llibreries
import os
import PIL
import math
import subprocess
import pathlib
from PIL import Image, ImageDraw

path_script = str(pathlib.Path(__file__).parent.absolute()) + "/folder_creation.sh"
home_img = expanduser("~") + "/Image_creation_tool"

#funcio per crear la carpeta on anira el fitxer master 
def create_folder(path):
    subprocess.call(path)

create_folder(path_script)

#Header del fitxer master & Lineas on anira escrit el master.
header_master = "fitxermaster_x_y_ang_ample_alt_color"
lineas = ""

#Color per la imatge que s'introduira a la plantilla (c=color, bn=blanc/negre, s=sepia)
COLOR_IMATGE = "bn"

#Plantilla sobre la que executar la creacio del fitxer master.
plantilla = Image.open(home_img+"img_name.png")
#plantilla = Image.open("/path/to/the/image/you/want/to/analyze")
print(plantilla.size[0], plantilla.size[1])

plantilla = plantilla.convert("RGB")

#Funcio per trobar l'angle.
def find_angle(pixel_esquerra, pixel_dreta, minmax_y):

    #Definicio de les cantonades i del pixel mes infeorior i superior en base a la Y.
    pixel_amunt = minmax_y[0]
    pixel_avall = minmax_y[1]
    cantonada_esquerra = pixel_esquerra[0], pixel_amunt[1]
    cantonada_dreta = pixel_dreta[0], pixel_avall[1]

    #Punts que formen el triangle.
    a = pixel_esquerra
    b = pixel_amunt
    c = cantonada_esquerra

    #Formula per extreure l'angle de 3 punts concrets utilitzant coordenades.
    angle = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))

    return angle

#Funció per trobar les cantonades d'una imatge rotada.
def find_rotated_coords(pixel_esquerra, pixel_dreta, minmax_y):
    
    #Definicio del pixel mes inferior i superior en base a la Y.
    pixel_amunt = minmax_y[0]
    pixel_avall = minmax_y[1]

    #Definicio de les dues cantonades (esquerra superior i dreta inferior).
    cantonada_esquerra = pixel_esquerra[0], pixel_amunt[1]
    cantonada_dreta = pixel_dreta[0], pixel_avall[1]

    return cantonada_esquerra, cantonada_dreta

#Funció per detectar la rotacio.
def detecta_rotacio(minmax_y):

    #Per calcular la rotacio comparo si las X del minim i el maxim son la mateixa, en cas de ser-ho la imatge no esta rotada, per tant retorna false.
    if minmax_y[0][0] == minmax_y[1][0]:
        value = False
    else:
        #En cas d'estar rotada retorna True.
        value = True

    return value

#Funció per poder detectar les coordenades minimes i maximes d'y (alçada) per poder calcular la rotacio mes endavant.
def detecta_y_coords(pixels):
    
    biggest_y = 0
    smallest_y = 10000

    #Comparació per treure les coordenades Y mes grans i mes petites.
    for coord in pixels:
        if coord[1] < smallest_y:
            smallest_y = coord[1]
            smallest_y_coord = coord
        if coord[1] > biggest_y:
            biggest_y = coord[1]
            biggest_y_coord = coord

    return smallest_y_coord, biggest_y_coord

#Funció per poder pintar de negre els rectangles ja detectats
def pintarequadre(img, cantonada1, cantonada2):
    
    #Converteixo la imatge en un ImageDraw per poder pinta sobre la imatge
    # --- La imatge esta sent modificada en temps real, el drawing es pinta sobre la img.
    draw = ImageDraw.Draw(img)
    draw.polygon((cantonada1, (cantonada2[0], cantonada1[1]), cantonada2, (cantonada1[0], cantonada2[1])), fill=(0, 0, 0))

#Generador de les lineas sobre el master.dpl
def generalinea(lineas,amp,llarg,x,y, ang):

    global COLOR_IMATGE

    lineas = lineas + str(x) + "," + str(y) + "," + str(ang) + "," + str(amp) + "," + str(llarg) + "," + COLOR_IMATGE + "\n"

    return lineas

#Escriptura sobre el fitxer master
def writefitxermaster(lineas):
    
    global home_img
    global header_master
    fitxer = open(home_img + "/master.dpl","w")
    fitxer.write(header_master + "\n" + lineas)
    fitxer.close

#Deteccio de pixels d'un color concret.
def detectarequadre(img):

    global lineas
    pixels=[]

    #Coords declarades per poder fer comparacions directament.
    coordenadesX_min = 10000
    coordenadesY_min = 10000
    coordenadesX_max = 0
    coordenadesY_max = 0

    #Bypass per poder agafar nomes els rectangles vermells.
    full_white_line = False
    red_found_x = False

    #Començo a recorrer d'esquerra a dreta desde x=0.
    for x in range(img.width):

        #Si la white line es true (es a dir no hi ha pixels vermells), pero ja he trobat pixels vermells abans significa que ja tinc un requadre.
        if full_white_line == True and red_found_x == True:
            white_found_x = False
            break

        red_found_y = False
        full_white_line = True

        #Per cada pixel d'x recorro tota la columna desde y=0.
        for y in range(img.height):
            
            #Coordenades actuals que estem recorrent (x, y)
            coords = x, y
            
            #Agafo la combinacio RGB del pixel actual en el que estic pasantli les coordenades actuals.
            pixel = img.getpixel(coords)
            
            #Pixel de color vermell:
            if (pixel[0] == 255 or pixel[0] == 254) and (pixel[1] == 0 or pixel[1] == 1) and (pixel[2] == 0 or pixel[2] == 1):

                #En el moment en el que es troba un pixel vermell declarem que red_found_y es True.
                red_found_y = True

                #Guardo les coordenades del pixel vermell trobat.
                pixels.append(coords)

                #Coords temporals de la X i la Y del pixel de color vermell actual.
                tmpcoordsx = coords[0]
                tmpcoordsy = coords[1]

                #Calcul de les coordenades mes grans i petites de cada una. (XMAX, XMIN, YMAX, YMIN)
                if tmpcoordsx < coordenadesX_min:
                    coordenadesX_min = tmpcoordsx

                if tmpcoordsy < coordenadesY_min:
                    coordenadesY_min = tmpcoordsy

                if tmpcoordsx > coordenadesX_max:
                    coordenadesX_max = tmpcoordsx

                if tmpcoordsy > coordenadesY_max:
                    coordenadesY_max = tmpcoordsy

            else:

                #Detecto si l'ultim pixel que he trobat es de color vermell torno la x vermella i la white line es false.
                if red_found_y == True:
                    red_found_x = True
                    full_white_line = False
                    break
    
    #Metode per detectar les coordenades minimes i maximes d'y + la x que acompanya.
    minmax_y = detecta_y_coords(pixels)

    #detecta_rotacio retorna True si la imatge esta rotada i False si no ho esta.
    if detecta_rotacio(minmax_y):
        #print("Hi ha rotació en la imatge.")
        cantonades = find_rotated_coords(pixels[0], pixels[-1], minmax_y)
        coordenadesX_max = cantonades[1][0]
        coordenadesX_min = cantonades[0][0]
        coordenadesY_max = cantonades[1][1]
        coordenadesY_min = cantonades[0][1]
        #print(coordenadesX_max, coordenadesX_min, coordenadesY_max, coordenadesY_min)
        angle = round(find_angle(pixels[0], pixels[-1], minmax_y), 2)
        print("Angle de la imatge trobat: ",angle)

    else:
        print("No hi ha rotació en la imatge.")
        angle = 0

    #Calcul de l'amplada i l'allargada de la zona de color vermell.
    amplada = coordenadesX_max-coordenadesX_min
    llargada = coordenadesY_max-coordenadesY_min

    #Arreglo de coordenades per agafar el pixel que dona cantonada amb el color
    coordenadesX_max = coordenadesX_max + 3
    coordenadesY_max = coordenadesY_max + 2

    #Append de les lineas dins del fitxer amb les dades corresponents a cada rectangle.
    lineas = generalinea(lineas,amplada,llargada,coordenadesX_min,coordenadesY_min, angle)
    writefitxermaster(lineas)

    c1 = coordenadesX_min, coordenadesY_min
    c2 = coordenadesX_max, coordenadesY_max

    #Es pinta de color negre el rectangle que ja s'ha detectat i escrit.
    pintarequadre(plantilla, c1, c2)
    return pixels[0], pixels[-1]


requadre = detectarequadre(plantilla)
print("Coordenades de les dues cantonades que formen el rectangle: ", requadre)


'''
#----- TMP - Canviar per un que es recorri automaticament sense especificar els requadres que hi ha. -----
#Bucle de repetició en funcio de la quantitat de imatges a sustituir.
while img_number > 0:
    requadre = detectarequadre(plantilla)
    print(requadre)
    img_number -= 1
    '''