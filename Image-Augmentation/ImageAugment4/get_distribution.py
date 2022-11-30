import glob

def return_distribution(real_label_dir, domain, out_shape):
    real_lbl_dir = f"{real_label_dir}/{domain}/Real/"
    all_lbls = glob.glob(real_lbl_dir + "*.txt")

    out_ht, out_w = out_shape

    num_imgs = []
    width_turbines = []
    height_turbines = []
    
    for lbl in all_lbls:

        with open(lbl, "r") as f:
            lst = [float(x) for x in f.read().split()]
            lines = f.read().split("\n")

            x_ctrs = [round(i*out_w,1) for i in lst[1::5]]
            y_ctrs = [round(i*out_ht,1) for i in lst[2::5]]
            widths = [round(i*out_w) for i in lst[3::5]]
            heights = [round(i*out_ht)  for i in lst[4::5]]

            num_imgs.append(len(x_ctrs))

            width_turbines.extend(widths)
            height_turbines.extend(heights)

    return num_imgs, width_turbines, height_turbines