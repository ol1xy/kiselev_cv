import numpy as np
import matplotlib.pyplot as plt 
from skimage import color
from skimage.measure import regionprops, label


def calculate_mean(hsv_image):
    saturated = hsv_image[:, :, 0]
    av_saturated = np.unique(saturated)
    eps = np.diff(av_saturated).mean()

    return [np.mean(i) * 360 for i in np.array_split(av_saturated, 
            np.where(np.diff(av_saturated)) > eps)[0] + 1]


def calculate_mid(figure):
    
    return [(p1 + p2) / 2 for p1, p2 in zip(figure,
            figure[1:] + [figure[0] + 360])]


def figure_color(region):
    color_value = hsv_image[int(region.centroid[0]),
                  int(region.centroid[1]), 0] * 360
    
    return next((label for label, border_color in zip(['красный', 
            'желтый', 'зеленый', 'светло-зеленый', 'синий', 'фиолетовый'], 
            border_values) if color_value < border_color), 'red')
    

image = plt.imread("balls_and_rects.png")
hsv_image = color.rgb2hsv(image)

binary_mask = (np.sum(image, 2) > 0).astype(int)
labeled_regions = label(binary_mask)

regions = regionprops(labeled_regions)
color_means = calculate_mean(hsv_image)[1:]
border_values = calculate_mid(color_means)

figures_circle = {}
figures_rect = {}

for region in regions:
    color_figure = figure_color(region)
    figures_dict = figures_circle if np.all(region.image) else figures_rect
    figures_dict[color_figure] = figures_dict.get(color_figure, 0) + 1

print(f"Общее число {labeled_regions.max()}")
print(f"Элипсоиды {figures_circle}")
print(f"Прямоугольники {figures_rect}")


# plt.imshow(image)
# plt.show()