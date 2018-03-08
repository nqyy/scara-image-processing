# styletransfer

test.jpg is the testing file <br />

``quantize.py`` contains the method of quantization of image <br />
command: ``python3 quantize.py image.jpg color1 color2 color3 (factor)`` <br />
example: ``python3 quantize.py image.jpg black yellow red 0.5`` <br />
white is used as the default 4th color <br />
supported colors: red, orange, yellow, green, blue, purple, black, white. <br />
last argument is the optional image resolution factor <br />
this function will ``output out_quantize.bmp`` which will be taken as input of filling, etc. <br />

``filling.py`` contains the method of filling of the image

