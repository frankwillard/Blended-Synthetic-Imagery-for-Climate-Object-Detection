import cv2
import random
import glob
import os
import re
from pathlib import Path

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

output_dir = "/home/fcw/shadow_boxes/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
    x_ctrs = [round(i*608,1) for i in label_lst[1::5]]
    y_ctrs = [round(i*608,1) for i in label_lst[2::5]]
    widths = [round(i*304) for i in label_lst[3::5]]
    heights = [round(i*304)  for i in label_lst[4::5]]

    if not os.path.exists(shadow_label):
        continue

    with open(shadow_label, "r") as f:
        #print(f.read().split())
        shadow_lst = [float(x) for x in f.read().split()]

    #Shadow + turbine for image
    num_turbines = [i for i in shadow_lst[::5]]
    shadow_x_ctrs = [round(i*608,1) for i in shadow_lst[1::5]]
    shadow_y_ctrs = [round(i*608,1) for i in shadow_lst[2::5]]
    shadow_widths = [round(i*304) for i in shadow_lst[3::5]]
    shadow_heights = [round(i*304) for i in shadow_lst[4::5]]

    print(img_name)
    print(label)

    my_img = cv2.imread(img_name)

    #Could add "bbox_"
    new_fname = output_dir  + img_name[img_name.rfind("/")+1:]
    #new_fname = multiple_replace(reg_dict, my_png_file)
    print(new_fname)

    x_ctrs.extend(shadow_x_ctrs)
    y_ctrs.extend(shadow_y_ctrs)
    widths.extend(shadow_widths)
    heights.extend(shadow_heights)


    plot_one_box(x_ctrs=x_ctrs, y_ctrs=y_ctrs, widths=widths, heights=heights,img=my_img,fname=new_fname)


