import PIL
from PIL import Image
import random

image = Image.new('RGB', (50, 50))

pixels = image.load()

# # column
# for y in range(50):
#     for x in range(50):
#         if y == 25:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)

# # row
# for y in range(50):
#     for x in range(50):
#         if x == 25:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)


# # upleft to downright
# for y in range(50):
#     for x in range(50):
#         if y == x:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)

# # pound
# for y in range(50):
#     for x in range(50):
#         if y == x or y == 49 - x or x == 0 or x == 49 or y == 0 or y == 49:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)


# # all black
# for y in range(50):
#     for x in range(50):
#         pixels[x, y] = (0, 0, 0)

# circle
for y in range(50):
    for x in range(50):
        number = (x-24)*(x-24) + (y-24)*(y-24)
        if number > 380 and number < 420:
            pixels[x, y] = (0, 0, 0)
        else:
            pixels[x, y] = (252, 252, 252)
            

image.save('out_quantize.bmp')