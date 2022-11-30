from get_distribution import return_distribution
import numpy as np

#domains = ["EM", "MW", "NW", "SW", "NE"]
domains = ["EM", "SW", "NE"]

total_num = []

for domain in domains:
    num_imgs, width_turbines, height_turbines = return_distribution(domain)
    total_num.extend(num_imgs)


sorted_imgs = sorted(total_num)

upper_quantile = sorted_imgs[9 * len(sorted_imgs) // 10]

#print(f"DOMAIN: {domain}")
print(upper_quantile)