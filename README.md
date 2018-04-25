#styletransfer

Overall introduction
===========
``quantize.py`` contains the method of quantization of image including filling holes <br />
``filling.py`` contains the method of filling of the image including optmization. <br />
``animation.py`` contains the forming of animation of our filling method. <br />
``communication.py`` contains the communication function through the serial port to the microcontroller. <br />

``configuration.config`` contains the configuration of the quantize and filling. <br />

supported colors: red, orange, yellow, green, blue, purple, black, white, aqua (more color can be added to quantize.py). <br />

Usage of programs
===========
1. run ``quantize.py`` (or ``test.py``) to generate the quantized image as ``out_quantize.bmp``.
2. run ``filling.py`` to generate the filling vectors of the image.
3. run ``communication.py`` to perform the communication throught serial port.

Explanation of configuration
===========
1. image: the input image to quantize.py.
2. colors: the colors we are trying to quantize to.
3. size: the resolution factor to resize the original image during quantize.
4. fillholes: to fill holes or not during quantize.
5. arm1: the back arm length.
6. arm2: the fore arm length.
7. pixel factor: the length in mm of each pixel.
8. animation: to perform animation or not to output to a directory named ./output
9. optimization: to perform optimization or not during filling.

Packages
===========
All packages required are in requirement.txt. Please run ``pip install -r requirement.txt``

Note
===========
test.jpg is the testing image file <br />