from PIL import Image

image = Image.new('RGB', (50, 50))
width, height = image.size

pixels = image.load()

# # row
# for y in range(height):
#     for x in range(width):
#         if y == height / 2:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)

# # column
# for y in range(height):
#     for x in range(width):
#         if x == width / 2:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)


# # upleft to downright
# for y in range(height):
#     for x in range(width):
#         if y == x:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)

# # upright to downleft
# for y in range(height):
#     for x in range(width):
#         if y == width - x:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)

# # pound
# for y in range(height):
#     for x in range(width):
#         if y == x or y == width - 1 - x or x == 0 or x == height - 1 or y == 0 or y == width - 1:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252 , 252)


# # all black
# for y in range(height):
#     for x in range(width):
#         pixels[x, y] = (0, 0, 0)

# circle
for y in range(height):
    for x in range(width):
        number = (x-24)*(x-24) + (y-24)*(y-24)
        if number > 380 and number < 420:
            pixels[x, y] = (0, 0, 0)
        else:
            pixels[x, y] = (252, 252, 252)

# # boundary
# for y in range(height):
#     for x in range(width):
#         if x == width - 1 or x == 0 or y == height - 1 or y == 0:
#             pixels[x, y] = (0, 0, 0)
#         else:
#             pixels[x, y] = (252, 252, 252)


image.save('out_quantize.bmp')
