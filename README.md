# Color-detector-by-coords

## Requirements
- Python3.x or more.
- Pillow library.

## How it works
This code works around finding the coordinates of the upper left corner of a red rectangle, straight or inclined.
I iterates over x (which is the width) and on every x it iterates over the columns y (height). The moment the code finds
a completely red pixel it will save that red pixel on a list and everytime he finds an x when going to the next y value,
it will just break and go the next x value. The moment there are no red pixels when iterating over a column by y, it will
calculate the coordinates, angle and both width and height of that specific rectangle, save it on a variable and paint
that rectangle color black. After all the rectangle have been found, it will write all the information of each rectangle on
a master.dpl file.
After that you can just read the file and user creacio_imtages.py to try and paste an image on all the rectangles found.

## Example
![tmp-0](https://user-images.githubusercontent.com/48527821/102594852-0e020a00-4117-11eb-94f1-ccabb93b4457.png)  
The black dots represent the coordinates I would get in this case, I also would get the inclination angle of the image
and the width and height of the inclination. In case of pasting an image to that template you will need to first inclinate
the image and then resize the image using the new width and height values from the master.dpl file.
