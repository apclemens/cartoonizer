import random, math, progressbar
from PIL import Image, ImageDraw

def random_pixel(image, visited):
    rand = (random.randint(0, image.width-1), random.randint(0, image.height-1))
    while rand in visited:
        rand = (random.randint(0, image.width-1), random.randint(0, image.height-1))
    return rand

def difference(pixel1, pixel2):
    diff = 0
    for i in range(3):
        diff += (pixel1[i] - pixel2[i])**2
    return math.sqrt(diff)

def pixel_neighbors(pixel, image):
    neighbors = []
    if pixel[0] > 0:
        neighbors.append((pixel[0]-1, pixel[1]))
    if pixel[1] > 0:
        neighbors.append((pixel[0], pixel[1]-1))
    if pixel[0] < image.width-1:
        neighbors.append((pixel[0]+1, pixel[1]))
    if pixel[1] < image.height-1:
        neighbors.append((pixel[0], pixel[1]+1))
    return neighbors

def average_color(image, pixel_group):
    r, g, b = (0, 0, 0)
    for p in pixel_group:
        r += image.getpixel(p)[0]
        g += image.getpixel(p)[1]
        b += image.getpixel(p)[2]
    r /= len(pixel_group)
    g /= len(pixel_group)
    b /= len(pixel_group)
    return (int(r), int(g), int(b))

def main(THRESHOLD):
    fname = 'left-to-right/'+("%06d" % (THRESHOLD,))+'.jpg'

    im = Image.open('pic.jpg')
    im2 = Image.new("RGB", (im.width, im.height), "white")
    draw = ImageDraw.Draw(im2)
    pixels_to_fill = []
    for i in range(im.width):
        for j in range(im.height):
            pixels_to_fill.append((i,j))
    pixel_groups = []
    bar = progressbar.ProgressBar(max_value=len(pixels_to_fill))
    i = 0

    while len(pixels_to_fill) > 0:
        pixel_queue = [pixels_to_fill[0]]
        initial_pixel = pixel_queue[0]
        pixels_to_fill.remove(initial_pixel)
        i += 1
        bar.update(i)
        group = []
        while len(pixel_queue) > 0:
            curr_pixel = pixel_queue.pop(0)
            group.append(curr_pixel)
            for n in pixel_neighbors(curr_pixel, im):
                if n not in pixels_to_fill:
                    continue
                if difference(im.getpixel(initial_pixel), im.getpixel(n)) > THRESHOLD:
                    continue
                pixel_queue.append(n)
                pixels_to_fill.remove(n)
                i += 1
                bar.update(i)

        avg = average_color(im, group)
        draw.point(group, fill=avg)
        im2.save(fname)

if __name__ == '__main__':
    t = 442
    for i in range(6):
        main(t)
        t = int(t / 2)
