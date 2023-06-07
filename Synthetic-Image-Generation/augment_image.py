from PIL import Image
import numpy as np
import os
import random

#{src}_{masknum}_{background_fname}

def augment_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, augmented_images_results_dir, out_fname, random_seed, num_objects_to_sample_per_image, offset_ctr, gp_gan_blend_offset,verbose=False):
  """
  Augments the image by pasting turbine images onto a canvas.

  Parameters:
  ----------
    -  objects_to_implant_img_fpaths (list): A list of paths to objects to implant.
    -  out_shape (tuple): The desired shape (width, height) of the output image.
    -  objects_to_implant_lbl_fpaths (list): A list of paths to files containing relative position and size information for the implanting objects.
    -  augmented_images_results_dir (str): The directory where the augmented images will be saved.
    -  out_fname (str): The filename of the output image.
    -  random_seed (int): The random seed for reproducibility.
    -  num_objects_to_sample_per_image (int): The maximum number of turbine images to sample for augmentation.
    -  offset_ctr (int): The offset center used for random positioning of turbine images.
    -  gp_gan_blend_offset (int): The blend offset used for masking.
    -  verbose (bool): Whether to print out information about the augmentation process.

  Returns:
  -------
    -  fpath (str): The file path of the augmented image.
    -  mask_fpath (str): The file path of the corresponding mask image.
    -  list: A list of cropped objects used for augmentation.
  """

  #makes directories
  canvas_dir = os.path.join(augmented_images_results_dir, "canvases/")
  mask_dir = os.path.join(augmented_images_results_dir, "masks/")
  label_dir = os.path.join(augmented_images_results_dir, "labels/")

  if not os.path.exists(augmented_images_results_dir):
    os.makedirs(canvas_dir)
    os.mkdir(mask_dir)
    os.mkdir(label_dir)

  masked_pixels = np.zeros(out_shape,dtype=bool)
  canvas = Image.new(mode='RGB', size=out_shape,color=(255,255,255))

  txt_fname = os.path.join(label_dir, out_fname + ".txt")
  txt_f = open(txt_fname, "w")

  imgs = 0
  c = 0
  random.seed(random_seed)

  ninetieth_percentile = num_objects_to_sample_per_image
  turbines_used = []

  while imgs < ninetieth_percentile and c < 100:
    c+=1

    #for j in range(len(location)):
    #8 sources
    rand_turbine_index = random.randint(0, len(objects_to_implant_img_fpaths)-1)
    windmill = Image.open(objects_to_implant_img_fpaths[rand_turbine_index])

    with open(objects_to_implant_lbl_fpaths[rand_turbine_index], "r") as f:
      rel_lst = [float(x) for x in f.read().split()]

    rel_class = rel_lst[0]
    rel_x_ctr = rel_lst[1]
    rel_y_ctr = rel_lst[2]
    rel_width = rel_lst[3]
    rel_height = rel_lst[4]

    loc_x = random.randint(offset_ctr, out_shape[0]-offset_ctr)
    loc_y = random.randint(offset_ctr, out_shape[1]-offset_ctr)

    #rand_width_index = random.randint(0, len(width_distribution)-1)
    #size_x = width_distribution[rand_width_index]

    #rand_height_index = random.randint(0, len(height_distribution)-1)
    #size_y = height_distribution[rand_height_index]

    curr_rotation = random.randint(0,3)*90

    #imwidth, imheight = windmill.size

    #avg_ratio = ((size_x/imwidth) + (size_y /imheight)) / 2
    #avg_ratio = ((size_x/(rel_width*imwidth)) + (size_y /(rel_height * imheight))) / 2
    #new_size = (int(imwidth * avg_ratio), int(imheight*avg_ratio))

    new_size = windmill.size
    size_x_add = new_size[0]/2
    size_y_add = new_size[1]/2

    #my_corners = [int(loc_x-size_x_add)+5, int(loc_x+size_x_add)-5, int(loc_y-size_y_add)+5, int(loc_y+size_y_add)-5]
    my_corners = [int(loc_x-size_x_add), int(loc_x+size_x_add), int(loc_y-size_y_add), int(loc_y+size_y_add)]

    #my_pixel_vals = masked_pixels[int(loc_y-size_y_add)+5:int(loc_y+size_y_add)-5,int(loc_x-size_x_add)+5:int(loc_x+size_x_add)-5]
    my_pixel_vals = masked_pixels[int(loc_y-size_y_add)-gp_gan_blend_offset:int(loc_y+size_y_add)+gp_gan_blend_offset,int(loc_x-size_x_add)-gp_gan_blend_offset:int(loc_x+size_x_add)+gp_gan_blend_offset]
    
    if curr_rotation == 90 or curr_rotation == 270:
      #my_corners = [int(loc_x-size_y_add)+5, int(loc_x+size_y_add)-5, int(loc_y-size_x_add)+5, int(loc_y+size_x_add)-5]
      my_corners = [int(loc_x-size_y_add), int(loc_x+size_y_add), int(loc_y-size_x_add), int(loc_y+size_x_add)]
      
      #my_pixel_vals = masked_pixels[int(loc_y-size_x_add)+5:int(loc_y+size_x_add)-5,int(loc_x-size_y_add)+5:int(loc_x+size_y_add)-5]
      my_pixel_vals = masked_pixels[int(loc_y-size_x_add)-gp_gan_blend_offset:int(loc_y+size_x_add)+gp_gan_blend_offset,int(loc_x-size_y_add)-gp_gan_blend_offset:int(loc_x+size_y_add)+gp_gan_blend_offset]


    if not all((i <= out_shape[0] and i >= 0) for i in my_corners) or any(my_pixel_vals.flatten()):
      #Try different rotation
      #if curr_rotation % 180 == 0:
      #  my_corners = [int(loc_x-size_y_add)+5, int(loc_x+size_y_add)-5, int(loc_y-size_x_add)+5, int(loc_y+size_x_add)-5]
      #  my_pixel_vals = masked_pixels[int(loc_y-size_x_add)+5:int(loc_y+size_x_add)-5,int(loc_x-size_y_add)+5:int(loc_x+size_y_add)-5]
      #else:
      #  my_corners = [int(loc_x-size_x_add)+5, int(loc_x+size_x_add)-5, int(loc_y-size_y_add)+5, int(loc_y+size_y_add)-5]
      #  my_pixel_vals = masked_pixels[int(loc_y-size_y_add)+5:int(loc_y+size_y_add)-5,int(loc_x-size_x_add)+5:int(loc_x+size_x_add)-5]
      #curr_rotation += 90
      #if not all((i <= 608 and i >= 0) for i in my_corners) or any(my_pixel_vals.flatten()):
      print("OVERLAP")
      continue

    if curr_rotation == 360:
      curr_rotation = 0
    
    turbines_used.append(objects_to_implant_img_fpaths[rand_turbine_index])
    
    new_windmill = windmill.copy()
    #new_windmill = new_windmill.resize(new_size)
    new_windmill = new_windmill.rotate(curr_rotation,expand=True,fillcolor=(255,255,255))

    new_location = (int(loc_x - size_x_add), int(loc_y - size_y_add))

    #my_x_ctr = (new_location[0]+rel_x_ctr * new_size[0]) / out_shape[1]
    #my_y_ctr = (new_location[1]+rel_y_ctr * new_size[1]) / out_shape[0]
    my_width = (rel_width * new_size[0]) / out_shape[1]
    my_height = (rel_height * new_size[1]) / out_shape[0]

    imgs +=1

    ###MAIN EDITS for rotate bounding box
    if curr_rotation == 90 or curr_rotation == 270:
      #rotates for mask as needed
      new_location = (int(loc_x - size_y_add), int(loc_y - size_x_add))
      canvas.paste(im=new_windmill,box=new_location)
      masked_pixels[int(loc_y-size_x_add)+gp_gan_blend_offset:int(loc_y+size_x_add)-gp_gan_blend_offset,int(loc_x-size_y_add)+gp_gan_blend_offset:int(loc_x+size_y_add)-gp_gan_blend_offset] = True
      # Rotate bounding box
      # (x, (rot/180)(height-2y)+y)
      # (h, w)
      my_y_scalar = ((curr_rotation - 90)/ 180) * (1 - 2 * rel_y_ctr) + rel_y_ctr
      my_x_scalar = ((curr_rotation - 270) / -180) * (1 - 2 * rel_x_ctr) + rel_x_ctr
      my_x_ctr = (new_location[0]+my_y_scalar * new_size[1]) / out_shape[0]
      my_y_ctr = (new_location[1]+my_x_scalar * new_size[0]) / out_shape[1]
      txt_f.write("{my_class} {x_ctr} {y_ctr} {width} {height}\n".format(my_class="0", x_ctr=my_x_ctr,y_ctr=my_y_ctr,width=my_height,height=my_width))
    else:
      #0 or 180
      canvas.paste(im=new_windmill,box=new_location)
      masked_pixels[int(loc_y-size_y_add)+gp_gan_blend_offset:int(loc_y+size_y_add)-gp_gan_blend_offset,int(loc_x-size_x_add)+gp_gan_blend_offset:int(loc_x+size_x_add)-gp_gan_blend_offset] = True
      #Rotate bounding box
      # (((rot-90)/180)(width-2y)+y, x)
      # (w, h)
      my_y_scalar = ((curr_rotation)/ 180) * (1 - 2 * rel_y_ctr) + rel_y_ctr
      my_x_scalar = ((curr_rotation)/ 180) * (1 - 2 * rel_x_ctr) + rel_x_ctr
      my_x_ctr = (new_location[0]+my_x_scalar * new_size[0]) / out_shape[1]
      my_y_ctr = (new_location[1]+my_y_scalar * new_size[1]) / out_shape[0]
      txt_f.write("{my_class} {x_ctr} {y_ctr} {width} {height}\n".format(my_class="0", x_ctr=my_x_ctr,y_ctr=my_y_ctr,width=my_width,height=my_height))
  
  masked_pixels = np.stack((masked_pixels, masked_pixels, masked_pixels), axis=2)
  mask = Image.fromarray((masked_pixels*255).astype(np.uint8))
  #mask = mask.rotate(angle=rotation,expand=False)
  #canvas = canvas.rotate(rotation,expand=False,fillcolor=(255,255,255))

  #display(mask)
  #display(canvas)

  txt_f.close()

  fpath = os.path.join(canvas_dir, out_fname + ".jpg")
  canvas.save(fpath)
  mask_fpath = os.path.join(mask_dir, out_fname + ".png")
  mask.save(mask_fpath)

  return fpath, mask_fpath, turbines_used