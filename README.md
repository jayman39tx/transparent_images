# transparent_images
Select a folder full of images to copy them into a "transparency" folder with transparent backgrounds.

   Converts a RGB image to a RGBA image with transparency,
   depending on colors in each of the four corners of the image.

Simply use the folder-selector when the Python script runs to select a folder that holds any images you want to convert.
A subfolder under that folder named "transparent" will be created,
and is where any transparent versions of the images will be found.

Any images that are not saved as transparent to the new folder could not be set as transparent, according to their corner colors.

If the colors and alpha values of all four corner pixels of an image are different, the program won't know which color is the likeliest transparent color, so it won't save a transparent version of the file. This is an intelligent decision to avoid making the wrong color transparent. Some images should not have transparency.

This is great for converting non-transparent PyGame sprites that use specific colors at the corners to represent transparency,
but are not actually transparent images.
