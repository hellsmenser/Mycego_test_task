import numpy as np
import cv2

from os import walk
from math import sqrt, ceil


def flat_list_to_rectangle_nested(lst):
    """
        transform list of images to rectangle form
    :param lst: list to transform
    :return: neasted list with rectangle form
    """
    nested_list = []
    size = ceil(sqrt(len(lst)))
    row = []

    for i, element in enumerate(lst):
        row.append(element)
        if len(row) % size == 0:
            nested_list.append(row)
            row = []
    if len(row) > 0:
        row += ["placeholder" for i in range(size - len(row))]
        nested_list.append(row)

    return nested_list

def get_images(path):
    """
        read all images from path directory
    :param path: directory with images
    :return: list of images
    """

    images = []
    for root, dirs, filenames in walk("data/" + path.strip()):
        images += [root + "/" + f for f in filenames]
    return images

def add_border(img):
    border_width = 25
    border_color = (255, 255, 255)

    new_img = cv2.copyMakeBorder(img,
                             top=border_width,
                             bottom=border_width,
                             left=border_width,
                             right=border_width,
                             borderType=cv2.BORDER_CONSTANT,
                             value=border_color)
    return new_img

def get_image_row(namesList):
    """
        concatinate list of images into single image
    :param namesList: list of images in NumPy or openCV format
    :return: single image in NumPy/OpenCV
    """

    row = []

    for i in namesList:
        if i != "placeholder":
            img = cv2.imread(i)
        else:
            img = np.zeros((800, 800, 3), np.uint8)
            img[:] = (255, 255, 255)

        row.append(add_border(img))
    return cv2.hconcat(row)

def main():
    dicts = input("Введите список папок с изображениями из data через запятую: ").split(",")

    images = []
    for path in dicts:
        images += get_images(path)
    squareImg = flat_list_to_rectangle_nested(images)

    rows = list(map(get_image_row, squareImg))
    result = cv2.vconcat(rows)
    cv2.imwrite("result.tiff", result)

if __name__ == '__main__':
    main()
