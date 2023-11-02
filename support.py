import csv
import os

import pygame


def import_csv_layout(path):
    map = []
    with open(path) as fin:
        layout = csv.reader(fin)
        for row in layout:
            map.append(list(row))

    return map


def import_folder(path):
    images = []
    for image in sorted(os.listdir(path)):
        image_surf = pygame.image.load(os.path.join(path, image))
        images.append(image_surf)

    return images


if __name__ == "__main__":
    print(import_folder("./assets/graphics/Grass"))
