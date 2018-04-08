import random, math, progressbar
from PIL import Image, ImageDraw
from push_to_git import git_add, git_commit, git_push

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

def main(THRESHOLD, t_incremental, angle, angle_incremental):
    fname = 'front/'+str(t_incremental)+'-'+str(angle_incremental)+'.jpg'

    im = Image.open('pic.jpg')
    im2 = Image.new("RGB", (im.width, im.height), "white")
    draw = ImageDraw.Draw(im2)
    pixels_to_fill = []
    for j in range(im.height)[::-1]:
        for i in range(im.width):
            pixels_to_fill.append((i,j))
    pixels_to_fill.sort(key=lambda p: p[1]*math.cos(angle) + p[0]*math.sin(angle))
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

        avg = im.getpixel(initial_pixel)
        draw.point(group, fill=avg)
        im2.save(fname)
    git_add('.', '.')
    git_commit('add file', '.')
    git_push('.')

if __name__ == '__main__':
    dx = math.log(442/13)/16
    for angle_incremental in range(16):
        for t_incremental in range(17):
            t = 13 * math.exp(dx * t_incremental)
            angle = math.pi * 2 / 16 * angle_incremental
            main(t, t_incremental+1, angle - math.pi/2, angle_incremental)



