import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2 as cv
import os
from random import randint
import shutil


import img_augmentation as aug
import utils
from utils import ImageProcessing


def readImage(path,pic,resolution):
   # read image
   n_img = cv.imread(path + pic)
   # resize images with size inferior of resolution
   if ((n_img.shape[0] <= resolution[0]) or (n_img.shape[1] <= resolution[1])):

       img=cv.resize(n_img,(resolution[1],resolution[0]))

   else:

       # crop image
       # size of cropped image equal to resolution
       i = randint(0, n_img.shape[0] - resolution[0])

       j = randint(0, n_img.shape[1] - resolution[1])

       img = n_img[i:i + resolution[0], j:j + resolution[1]]

   return img

class DataGenerator:

  train_path = "train_path"
  mask_path ="mask_path"
  other_path = "train_path1"

  #resolution = (194, 259)
  def __init__(self, root_dir , resolution ):
      """
      Args:
           root_dir(string): directory with all train images
           resolution:(x,y): resolution of train images
      """

      self.root_dir = root_dir
      self.resolution = resolution
      self.images = []
      self.positions = []
      self.transparents = []
      # create a directory to hold training images
      utils.create_dir(self.other_path)
      # create a directory to hold label images
      utils.create_dir(self.mask_path)


  def generate(self):
      print("reading ..........")
      # load images
      for pic in os.listdir(self.root_dir):

           img = readImage(self.root_dir,pic,self.resolution)
           #probability of transparent text
           sometimes = randint(1, 10)

           img_process = ImageProcessing(img)

           # Create a white image
           img_white = utils.white_img(img)

           # get text caracteristics
           font, fontScale, fontColor, lineType = utils.text_caracteristics(img)

           # number of lines
           nb_lines = randint(1, 4)

           # name of image without the extension
           img_name = os.path.splitext(pic)[0]

           #write text
           img, bt, left1, bottom, end_left, transparent = img_process.draw_text(pic,img,img_white,nb_lines,font,fontScale,fontColor,lineType,sometimes,self.other_path,self.mask_path)

           self.images.append([img_name,img])
           self.transparents.append([sometimes,transparent])

           #text region
           self.positions.append([bt, left1, bottom, end_left])

      #create a directory to hold training images
      utils.create_dir(self.train_path)
      #delete directory
      shutil.rmtree(self.other_path)

     #instance of Augmentor
      augmentor = aug.Augmentor()
      print("image processing ............")
      #apply blending to get transparent text
      #for 10%  of images
      augmentor.blending(self.images,self.transparents,self.positions)

       #get augmented images
      augmented_images=  augmentor.img_aug(self.images,self.positions)

      #save the images on the train path
      for each_img in augmented_images:
            img_label=each_img[0]
            picture=each_img[1]
            # save image
            cv.imwrite(self.train_path+"/" + img_label + ".jpg", picture)
      print("saved")

if __name__ == "__main__":
    resol = (int(sys.argv[2]) , int(sys.argv[3]))
    trainset = DataGenerator(sys.argv[1],resol)
    trainset.generate()
