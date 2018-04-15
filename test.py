import PIL
from PIL import Image

image = Image.new('RGB', (50, 50))

pixels = image.load()

# #横线
# for y in range(50):
#     for x in range(50):
#         if y == 25:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (255, 255, 255)

# #竖线
# for y in range(50):
#     for x in range(50):
#         if x == 25:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (255, 255, 255)


#斜线
for y in range(50):
    for x in range(50):
        if y == x:
            pixels[x, y] = (0, 0, 0)
        else:
            pixels[x, y] = (255, 255, 255)

# # pound
# for y in range(50):
#     for x in range(50):
#         if y == x or y == 49 - x or x == 0 or x == 49 or y == 0 or y == 49:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (255, 255, 255)


# # all black
# for y in range(50):
#     for x in range(50):
#         pixels[x, y] = (0, 0, 0)

# # circle
# for y in range(50):
#     for x in range(50):
#         number = (x-24)*(x-24) + (y-24)*(y-24)
#         if number > 380 and number < 420:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (255, 255, 255)

image.save('test.bmp')