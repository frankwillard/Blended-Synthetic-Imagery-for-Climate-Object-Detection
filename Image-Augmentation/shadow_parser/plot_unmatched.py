import glob
import os
from pathlib import Path
from PIL import Image
from collections import Counter
import cv2
import random
import re

def plot_one_box(x_ctrs, y_ctrs, widths, heights, img, fname, color=None, label=None, line_thickness=None):
  """
  Plots boxes in one image

  Args:
      x_ctrs ([type]): Holds x centerpoints of YOLO bounding boxes in image
      y_ctrs ([type]): Holds y centerpoints of YOLO bounding boxes in image
      widths ([type]): Holds widths of YOLO bounding boxes in image
      heights ([type]): Holds heights of YOLO bounding boxes in image
      img ([type]): Holds image to add bounding boxes to
      fname ([type]): File name for output image
      color ([type], optional): [description]. Defaults to None.
      label ([type], optional): [description]. Defaults to None.
      line_thickness ([type], optional): [description]. Defaults to None.
  """
  for i in range(len(x_ctrs)):
    x = [x_ctrs[i]-widths[i],y_ctrs[i]-heights[i],x_ctrs[i]+widths[i],y_ctrs[i]+heights[i]]
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
  #Save file
  cv2.imwrite(fname, img)

shadow_lbl_dir = "/scratch/public/jitter/wt/labels/EM/Real_Shadow/"

lbl_dir = "/scratch/public/jitter/wt/labels/EM/Real/"

img_directory = "/scratch/public/images_for_shadow/EM/"

all_images = glob.glob(img_directory + "*.jpg")

output_dir = "/home/fcw/unmatched/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

turb_total = 0
shadow_total = 0
total_matches = 0

for img_name in all_images:
    #print(img_name)

    #head, tail = os.path.split(img)
    #base_fname = os.path.basename(img)
    base_fname = Path(img_name).stem

    label = lbl_dir + base_fname + ".txt"
    shadow_label = shadow_lbl_dir + base_fname + ".txt"

    with open(label, "r") as f:
        #print(f.read().split())
        label_lst = [float(x) for x in f.read().split()]

    #turb_total += len([i for i in label_lst[::5]])
    turbine_x_ctrs = [round(i*608,1) for i in label_lst[1::5]]
    turbine_y_ctrs = [round(i*608,1) for i in label_lst[2::5]]
    turbine_widths = [round(i*608) for i in label_lst[3::5]]
    turbine_heights = [round(i*608)  for i in label_lst[4::5]]

    if not os.path.exists(shadow_label):
        continue

    with open(shadow_label, "r") as f:
        #print(f.read().split())
        shadow_lst = [float(x) for x in f.read().split()]

    #Shadow + turbine for image
    num_turbines = [i for i in shadow_lst[::5]]
    shadow_x_ctrs = [round(i*608,1) for i in shadow_lst[1::5]]
    shadow_y_ctrs = [round(i*608,1) for i in shadow_lst[2::5]]
    shadow_widths = [round(i*608) for i in shadow_lst[3::5]]
    shadow_heights = [round(i*608) for i in shadow_lst[4::5]]

    turbine_matches = {}
    count = []
    shadow_total+=len(num_turbines)
    
    for i in range(len(num_turbines)):

        left = shadow_x_ctrs[i] - (shadow_widths[i] / 2)
        right = shadow_x_ctrs[i] + (shadow_widths[i] / 2)

        top = shadow_y_ctrs[i] - (shadow_heights[i] / 2)
        bottom = shadow_y_ctrs[i] + (shadow_heights[i] / 2)

        turbine_matches[i] = []
        for j in range(len(num_turbines)):
            relative_left = turbine_x_ctrs[j] - (turbine_widths[j] / 2)
            relative_right = turbine_x_ctrs[j] + (turbine_widths[j] / 2)

            relative_top = turbine_y_ctrs[j] - (turbine_heights[j] / 2)
            relative_bottom = turbine_y_ctrs[j] + (turbine_heights[j] / 2)

            #print(0 < left - 10 < relative_left, 608 > right + 10 > relative_right)
            #print(0 < top - 10 < relative_top, 0 < relative_bottom < bottom + 10)
            
            #print(top, bottom)
            #print(relative_top, relative_bottom)

            flexibility = 10

            if 0 < left - flexibility < relative_left and 608 > right + flexibility > relative_right and 0 < top - flexibility < relative_top and 608 > bottom + flexibility > relative_bottom:
            #if 0 < left < relative_left and 608 > right > relative_right and 0 < top < relative_top and 608 > bottom > relative_bottom:

                turbine_matches[i].append(j)
                count.append(j)
    
    counter = Counter(count)


    my_x_ctrs = turbine_x_ctrs.copy()
    my_y_ctrs = turbine_y_ctrs.copy()
    my_widths = turbine_widths.copy()
    my_heights = turbine_heights.copy()
    
    for i in range(len(num_turbines)):

        left = shadow_x_ctrs[i] - (shadow_widths[i] / 2)
        right = shadow_x_ctrs[i] + (shadow_widths[i] / 2)

        top = shadow_y_ctrs[i] - (shadow_heights[i] / 2)
        bottom = shadow_y_ctrs[i] + (shadow_heights[i] / 2)
        
        #One turbine in each shadow label
        #Each turbine only its shadow label
        
        #for j in range(len(num_turbines)):

        if not (len(turbine_matches[i]) == 1 and counter[turbine_matches[i][0]] == 1):
            my_x_ctrs.append(shadow_x_ctrs[i])
            my_y_ctrs.append(shadow_y_ctrs[i])
            my_widths.append(shadow_widths[i])
            my_heights.append(shadow_heights[i])
            total_matches+=1
    
    my_widths = [x / 2 for x in my_widths]
    my_heights = [x / 2 for x in my_heights]

    my_img = cv2.imread(img_name)
    new_fname = output_dir  + img_name[img_name.rfind("/")+1:]

    if len(my_widths) > len(turbine_widths):
        plot_one_box(x_ctrs=my_x_ctrs, y_ctrs=my_y_ctrs, widths=my_widths, heights=my_heights,img=my_img,fname=new_fname)


            #image = Image.open(img_name)
            #image_cropped = image.crop((left, top, right, bottom))

            #image_filename = new_cropped_directory + Path(img_name).stem + "_" + str(i) + ".jpg"

            #print(image_filename)
            #total_matches +=1
            #image_cropped.save(image_filename)


            #with open(cropped_label, "w") as f:
                #left and relative left and so on
print(shadow_total)
print(total_matches)





        






    


