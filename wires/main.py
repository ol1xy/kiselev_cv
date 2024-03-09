from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np
import os


for img_path in os.listdir("images"):
    
    labeled = label(image)
    print("Следующая картинка: ")
    image = np.load("images/" + img_path)

    for i in range(1, labeled.max()+1):
        tmp = labeled == i
        result = label(binary_erosion(tmp))

        max_parts = result.max()

        if max_parts == 0:
            print("Нету провода")

        elif max_parts == 1:
            print("Целый провод")

        else:
            print(f"Провод порван на {max_parts} части")
