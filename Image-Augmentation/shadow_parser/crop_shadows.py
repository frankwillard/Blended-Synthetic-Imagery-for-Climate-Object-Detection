import glob
import os
from pathlib import Path
from PIL import Image
from collections import Counter
import re
import json

def multiple_replace(dict, text):
  """
  Applies multiple replaces in string based on dictionary

  Args:
      dict ([type]): Dictionary with keys as phrase to be replaced, vals as phrase to replace key
      text ([type]): Text to apply string replaces to

  Returns:
      [type]: [description]
  """


  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

reg_dict = {
    "images": "labels",
    ".jpg": ".txt"
}

domain_file = "/scratch/public/jitter/wt/domain_overview.json"

flexibility = 10

domains = ["EM", "SW", "NW"]

for domain in domains:

    shadow_lbl_dir = f"/scratch/public/jitter/wt/labels/{domain}/Real_Shadow/"

    lbl_dir = f"/scratch/public/jitter/wt/labels/{domain}/Real/"

    #img_directory = "/scratch/public/images_for_shadow/EM/"

    with open(domain_file, "r") as f:
        data = json.load(f)
        all_fnames = data[domain]['Real'][:100]
    
    all_images = [f"/scratch/public/jitter/wt/images/{domain}/Real/{fname}.jpg" for fname in all_fnames]
    #all_images = glob.glob(img_directory + "*.jpg")

    new_cropped_directory = f"/scratch/public/new_cropped_turbines/images/{domain}/"

    if not os.path.exists(new_cropped_directory):
        os.makedirs(new_cropped_directory)
        os.makedirs(new_cropped_directory.replace("images", "labels"))


    turb_total = 0
    shadow_total = 0
    total_matches = 0

    #all_images = ["/scratch/public/images_for_shadow/EM/EM_16877.jpg"]

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
        num_turbines = [i for i in label_lst[::5]]
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
        num_shadows = [i for i in shadow_lst[::5]]
        shadow_x_ctrs = [round(i*608,1) for i in shadow_lst[1::5]]
        shadow_y_ctrs = [round(i*608,1) for i in shadow_lst[2::5]]
        shadow_widths = [round(i*608) for i in shadow_lst[3::5]]
        shadow_heights = [round(i*608) for i in shadow_lst[4::5]]

        turbine_matches = {}
        count = []
        shadow_total+=len(num_shadows)
        
        for i in range(len(num_shadows)):

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

                #Debugging

                #print(f"Pair: ({i}, {j})")
                #print("Shadow:")
                #print(left, right, top, bottom)
                #print("Turbine:")
                #print(relative_left, relative_right, relative_top, relative_bottom)

                #print(0 < left - flexibility < relative_left, 608 > right + flexibility > relative_right,  0 < top - flexibility < relative_top,  608 > bottom + flexibility > relative_bottom)

                if 0 < left - flexibility < relative_left and 608 > right + flexibility > relative_right and 0 < top - flexibility < relative_top and 608 > bottom + flexibility > relative_bottom:
                #if 0 < left < relative_left and 608 > right > relative_right and 0 < top < relative_top and 608 > bottom > relative_bottom:

                    turbine_matches[i].append(j)
                    count.append(j)
        
        counter = Counter(count)
        
        for i in range(len(num_shadows)):

            left = shadow_x_ctrs[i] - (shadow_widths[i] / 2) - flexibility
            right = shadow_x_ctrs[i] + (shadow_widths[i] / 2) + flexibility

            top = shadow_y_ctrs[i] - (shadow_heights[i] / 2) - flexibility
            bottom = shadow_y_ctrs[i] + (shadow_heights[i] / 2) + flexibility
            
            #One turbine in each shadow label
            #Each turbine only its shadow label
            
            #for j in range(len(num_turbines)):
            #print("Turbine" + str(i))

            #print(len(turbine_matches[i]))

            #if len(turbine_matches[i]) >= 1:
            #    print(counter[turbine_matches[i][0]])

            if len(turbine_matches[i]) == 1 and counter[turbine_matches[i][0]] == 1:

                image = Image.open(img_name)
                image_cropped = image.crop((left, top, right, bottom))

                image_filename = new_cropped_directory + Path(img_name).stem + "_" + str(i) + ".jpg"

                cropped_label = multiple_replace(reg_dict, image_filename)

                print(image_filename)
                total_matches +=1

                image_cropped.save(image_filename)

                my_class = 0

                new_width = right - left
                new_height = bottom - top

                j = turbine_matches[i][0]
                
                relative_left = turbine_x_ctrs[j] - (turbine_widths[j] / 2)
                relative_right = turbine_x_ctrs[j] + (turbine_widths[j] / 2)
                relative_top = turbine_y_ctrs[j] - (turbine_heights[j] / 2)
                relative_bottom = turbine_y_ctrs[j] + (turbine_heights[j] / 2)

                relative_width = (relative_right - relative_left)
                relative_height = (relative_bottom - relative_top)
                
                my_class = 0
                my_x_ctr = ((relative_left - left) + (relative_width / 2)) / new_width
                my_y_ctr = ((relative_top - top) + (relative_height / 2)) / new_height
                my_width = relative_width / new_width
                my_height = relative_height / new_height

                with open(cropped_label, "w") as f:
                    f.write(f"{my_class} {my_x_ctr} {my_y_ctr} {my_width} {my_height}\n")

    print("Matches, total: ")
    print(total_matches, shadow_total)





        






    


