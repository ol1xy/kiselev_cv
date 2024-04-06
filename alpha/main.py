import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from collections import defaultdict
from pathlib import Path


def has_line(region, horizontal=True):
    return 1. in np.mean(region.image, int(horizontal))

def holes_count(region):
    inv = np.logical_not(region.image)
    labeled = label(inv)
    holes = np.max(labeled)
    return holes

def extractor(region):
    area = region.area/ region.image.size
    euler = (region.euler_number + 1) / 2
    eccentricity = region.eccentricity
    perimeter = region.perimeter / region.image.size
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]

    line_v = has_line(region, False)
    holes = holes_count(region)
    if eccentricity == 0:
        holes = 0
    return np.array([area, euler, eccentricity, perimeter, cy, cx, line_v, holes])


def distance(p1, p2):
    return ((p1 - p2)**2).sum() ** 0.5

def classificator(prop, classes):
    klass = None
    min_d = 10**16
    for cls in classes:
        d = distance(prop, classes[cls])
        if d<min_d:
            klass = cls
            min_d = d
    return klass

image = plt.imread("alphabet_small.png")
image = np.mean(image, 2)

image[image == 1] = 0
image[image > 0] = 1

labeled = label(image)
regions = regionprops(labeled)

classes = {"A": extractor(regions[2]),
           "B": extractor(regions[3]),
           "8": extractor(regions[0]),
           "0": extractor(regions[1]),
           "1": extractor(regions[4]),
           "W": extractor(regions[5]),  
           "X": extractor(regions[6]),  
           "*": extractor(regions[7]),  
           "-": extractor(regions[9]), 
           "/": extractor(regions[8]), 

            } 

alphabet = plt.imread('alphabet.png').mean(2)
alphabet[alphabet>0] = 1
labeled = label(alphabet)
regions = regionprops(labeled)

result = defaultdict(lambda: 0)
path = Path('.') / 'result'
path.mkdir(exist_ok=True)
plt.figure()
for i, region in enumerate(regionprops(labeled)):
    symbol = classificator(extractor(region), classes)
    result[symbol] += 1
    plt.clf()
    plt.title(f'{symbol=}')
    plt.imshow(region.image)
    plt.tight_layout()
    plt.savefig(path/f'{i}.png')

print(result)