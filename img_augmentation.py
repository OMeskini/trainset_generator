import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from random import uniform


import imgaug as ia
from imgaug import augmenters as iaa

#blend for transparency
def blend_transparence(background, beta, foreground):

    h, w, c = background.shape

    for i in range(0, h):
       for j in range(0, w):
              for k in range(0, c):
                  #skip the white pixels
                  #just blend the pixels of text
                  if (foreground[i, j, k] != 255):
                            x=background[i, j, k]
                            y=foreground[i, j, k]
                            background[i, j, k] = x * (1-beta) + y * beta



    return background


class Augmentor:


 def __init__(self):
  self.list_crop = []
 #blend text with the background
 #to get text transparency
 def blending(self,list_images,list_transparent,list_positions):

     # text transparence value
     alpha = uniform(0.4, 0.9)

     for idx, eachImg in enumerate(list_images):
         img = eachImg[1]
         txt_pos = list_positions[idx]
         #get text region
         crop = img[txt_pos[0]:txt_pos[2], txt_pos[1]:txt_pos[3]]

         #probability of having transparent text
         nb = (list_transparent[idx])[0]

         #case of transparent text
         if (nb == 1):
             #get text image
             transparent = (list_transparent[idx])[1]
             #text region
             text = transparent[txt_pos[0]:txt_pos[2],
                    txt_pos[1]:txt_pos[3]]

             #apply the blend
             crop = blend_transparence(crop, alpha, text)


         self.list_crop.append(crop)


     return self.list_crop

 #augmentation of text
 def img_aug(self,list_images,list_positions):

  ia.seed(1)


  seq = iaa.Sequential([

  # Execute 0 to 5 of the following(less important) augmenters per
  # image. Don't execute all of them, as that would often be way too
  # strong.
  #
  iaa.SomeOf((0, 5),

                 # Convert some images into their superpixel representation,
                 # sample between 20 and 200 superpixels per image, but do
                 # not replace all superpixels with their average, only
                 # some of them (p_replace).
                 iaa.Sometimes(0.3,
                     iaa.Superpixels(
                         p_replace=(0, 0.4),
                         n_segments=(20, 200)
                 )
                               ),
                 iaa.OneOf((0, 2),
                        # Small gaussian blur with random sigma between 0 and 0.5.
                        # But we only blur about 50% of all images.
                        iaa.GaussianBlur(sigma=(0, 0.5)),
                        iaa.AverageBlur(k=(2, 7)),

              ),
             # Add gaussian noise.
             # For 50% of all images, we sample the noise once per pixel.
             # For the other 50% of all images, we sample the noise per pixel AND
             # channel. This can change the color (not only brightness) of the
             # pixels.
             iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
             iaa.PiecewiseAffine(scale=(0.01, 0.05)),


             ),
# Strengthen or weaken the contrast in each image.
  iaa.ContrastNormalization((0.75, 1.5)),

# Make some images brighter and some darker.
# In 20% of all cases, we sample the multiplier once per channel,
# which can end up changing the color of the images.
  iaa.Multiply((0.8, 1.2), per_channel=0.2),

  # Either drop randomly 1 to 10% of all pixels (i.e. set
  #  them to black) or drop them on an image with 2-5% percent
  # of the original size, leading to large dropped
  # rectangles.
   iaa.Sometimes(0.6,
   iaa.OneOf([
          iaa.Dropout((0.01, 0.1), per_channel=0.5),
          iaa.CoarseDropout(
              (0.03, 0.15), size_percent=(0.02, 0.05),
              per_channel=0.2
          ),
   ])),
  # Apply affine transformations to each image.
  # Scale/zoom them, translate/move them, rotate them and shear them.
  iaa.Affine(
  rotate=(-3, 3),
  shear=(-8, 8)
  )
  ], random_order=
  True
  )
# apply augmenters in random order
  images_aug = seq.augment_images(self.list_crop)

  aug_images=[]

  #paste the text region into the real picture
  for ind, each_image in enumerate(list_images):
      img_name = each_image[0]
      img = each_image[1]
      txt_pos = list_positions[ind]
      img[txt_pos[0]:txt_pos[2], txt_pos[1]:txt_pos[3]] = images_aug[ind]
      aug_images.append([img_name, img])

  return aug_images
