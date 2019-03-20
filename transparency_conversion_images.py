#! /etc/bin/env python3

"""
   transparent_images.py

   Converts a RGB image to a RGBA image with transparency,
   depending on colors in each of the four corners of the image.
"""

from collections import Counter
from glob import glob
from os import chdir, makedirs, path
import sys

from matplotlib.image import imsave
from numpy import array
from PIL import Image
import PySimpleGUI as sg

if len(sys.argv) == 1:
    event, (fname,) = sg.Window('My Script').Layout([[sg.Text('Folder to open')],
                            [sg.In(), sg.FolderBrowse()],
                            [sg.CloseButton('Open'), sg.CloseButton('Cancel')]]).Read()
else:
    fname = sys.argv[1]

if not fname:
    sg.Popup("Cancel", "No filename supplied")
    raise SystemExit("Cancelling: no filename supplied")
# print(event, fname)

if event == "Open":
    chdir(fname)
    png_file_list = glob("*.png")
    # print(len(png_file_list), png_file_list)

    new_file_folder = fname + "/transparent"
    # print(new_file_folder)
    if png_file_list and not path.exists(new_file_folder):
        makedirs(new_file_folder)

    for file_name in png_file_list:
        old_file_path = fname + "/" + file_name
        filename_list = path.splitext(file_name)
        new_file_name = filename_list[0] + "_trans" + filename_list[1]
        # print(file_name, new_file_name)

        img = Image.open(old_file_path).convert('RGBA')
        corner_pix = []
        corner_pix.append((img.getpixel((0, 0))))
        corner_pix.append((img.getpixel((img.width-1, 0))))
        corner_pix.append((img.getpixel((0, img.height-1))))
        corner_pix.append((img.getpixel((img.width-1, img.height-1))))
        color = array(Counter(corner_pix).most_common(1)[0][0])

        # print(f'corner_pix: {corner_pix}')

        corner_pix_set = set(corner_pix)
        corner_pix_count = len(corner_pix_set)
        # print(f'corner color count: {corner_pix_count}, corner color set: {corner_pix_set}')

        if corner_pix_count < 4: # if a color appears more than once in the corners
            alpha_color = array([255, 255, 255, 0])
            # print(corner_pix[0], color, alpha_color)

            pixdata = array(img, dtype='i')
            # old_pix_data = imread(old_file_path)
            # print('Pillow Data: ', pixdata[15], 'MatPlotLib Data: ', old_pix_data)

            width, height = img.size
            # print(width, height)

            # print(color[3], color[3] < alpha_color[3])
            # exit()
            if color[3] > alpha_color[3]:
                for y in range(height):
                    leading_alpha = 0
                    for x in range(width):
                        # print(x, y, pixdata[y, x], color)
                        if (pixdata[y, x] == color).all():
                            leading_alpha = 127
                            # print(x, y, color, alpha_color, pixdata[y,x])
                            pixdata[y, x] = alpha_color
                            # print(color, alpha_color, pixdata[y,x])
                        elif leading_alpha == 127:
                            pixdata[y, x][3] = leading_alpha
                            leading_alpha = 0

            new_file_path = new_file_folder + "/" + new_file_name
            # print(new_file_path)

            # pixdata = pixdata.reshape(pixdata.shape[0]*pixdata.shape[1], pixdata.shape[2])
            # print(pixdata.shape)

            # new_img = Image.fromarray(pixdata, mode='RGBA') # RGBA?
            # new_pix_data = array(new_img, dtype = 'i') # i?
            # print(pixdata[15], new_pix_data[15])

            imsave(new_file_path, pixdata)
            # new_img.show()
            # new_img.save(new_file_path)
            # exit()
