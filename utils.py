import numpy as np
import cv2 as cv
import os
from random import randint, uniform, choice, gauss

#get a random color centred around (r,g,b)
def random_color(r,g,b):
    u = gauss(0, 1)
    v = gauss(0, 1)
    z = gauss(0, 1)

    R = abs(int(r * u))
    G = abs(int(g * v))
    B = abs(int(b * z))

    return (R, G, B)

#create a white image
def white_img(img):
        # Create a white image
        img_white = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        img_white[:] = (255, 255, 255)
        return img_white

#generate a line of text
def lineOfText():
    # choose a text
    words = open('/etc/dictionaries-common/words').read().splitlines()

    line = ""
    while line == "":
        for k in range(1, randint(1, 4)):
            word = choice(words)
            line += word + " "

    return line

#create a non existant directory
def create_dir(name_dir):
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

#get random text caracterisitics
#font, color, fontscale, thickness
def text_caracteristics(img):
 # list of fonts
        list = [cv.FONT_HERSHEY_SIMPLEX, cv.FONT_HERSHEY_PLAIN, cv.FONT_HERSHEY_SIMPLEX, cv.FONT_HERSHEY_DUPLEX,
                cv.FONT_HERSHEY_COMPLEX, cv.FONT_HERSHEY_SIMPLEX, cv.FONT_HERSHEY_TRIPLEX,
                cv.FONT_HERSHEY_COMPLEX_SMALL, cv.FONT_HERSHEY_SCRIPT_SIMPLEX, cv.FONT_HERSHEY_SCRIPT_COMPLEX]

        # text caracteristics
        font = choice(list)
        fontScale = uniform(0.3, 6.5)
        lineType = randint(1, 5)

        # random color
        fontColor = random_color(30, 20, 30)


        # in case of little image apply an average fontscale
        if img.shape[0] < 200:
            fontScale = uniform(0.3, 2)
        if img.shape[0] < 100:
            fontScale = uniform(0.3, 1)

        # for visibility of text
        if (fontScale < 1):
           lineType = 1

        return font, fontScale, fontColor, lineType



class ImageProcessing:

    def __init__(self,img):
        self.img=img

    #draw text
    def draw_text(self, pic, img, img_white, nb_lines, font, fontScale, fontColor, lineType, nb, o_path, mask_path):
        global text_bottom
        end_lines = 0
        height, weight = img.shape[:2]
        # Create a white image for transparency
        transparent_img = white_img(img)
        # foreach line
        for j in range(1, nb_lines+1):

            # load_text
            line = lineOfText()
            # get size of text
            textSize = cv.getTextSize(line, font, fontScale, lineType)
            w_text, h_text = textSize[0]


            if (j == 1):
              # Localization of text
              if(h_text<height):
                  if(h_text<(height-h_text)):
                     bottom = randint(h_text , height - h_text )
                  else:
                     bottom = randint(h_text,height)
              else:
                  bottom = randint(0,height)

              while (w_text>weight):
                line = line[0:int(len(line)/2)]
                w_text = int(w_text/2)
              left = randint(0, weight - w_text)
              if(bottom<h_text):
                text_bottom = min(0,(bottom-h_text))
              else:
                  text_bottom = (bottom-h_text)

            end_lines = max(left+w_text,end_lines)

            #text position
            bottomLeftCornerOfText = (left, bottom)

            #the case of non text_transparency
            if(nb != 1):
              # write the text
              cv.putText(img, line,
                       bottomLeftCornerOfText,
                       font,
                       fontScale,
                       fontColor,
                       lineType)


            cv.putText(img_white, line,
                       bottomLeftCornerOfText,
                       font,
                       fontScale,
                       fontColor,
                       lineType)

            cv.putText(transparent_img, line,
                       bottomLeftCornerOfText,
                       font,
                       fontScale,
                       fontColor,
                       lineType)

            # save image
            cv.imwrite(o_path+"/" + pic, img)

            cv.imwrite(mask_path+"/" + pic, img_white)

            # for next line
            if (nb_lines > 1):
             # load image to write next line
             img = cv.imread(o_path+"/" + pic)

             img_white = cv.imread(mask_path+"/" + pic)

             # make space between lines
             bottom = bottom + h_text

             #bottomLeftCornerOfText[0] = bottom

        if(end_lines>weight):
            end_lines = weight

        return (img, text_bottom, left, bottom, end_lines,transparent_img)
