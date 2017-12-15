from random import randint, uniform, shuffle

# takes FLATTENED data, width and length as input
def reformat(data, width, length):
    # partition r, g, b
    size = width * length
    r = data[:size]
    g = data[size:2*size]
    b = data[2*size:]
    # create 2d array of r, g, b
    r_formatted = []
    g_formatted = []
    b_formatted = []
    # reformat flattened r, g, b into 2d array
    for i in range(length):
        r_formatted.append(r[i * width: (i + 1) * width])
        g_formatted.append(g[i * width: (i + 1) * width])
        b_formatted.append(b[i * width: (i + 1) * width])
    # return 3d array of r,g,b
    rgb_formatted = []
    rgb_formatted.append(r_formatted)
    rgb_formatted.append(g_formatted)
    rgb_formatted.append(b_formatted)
    return rgb_formatted


# takes FORMATTED data as input and crop the center of the image
def center_crop(data, size):
    # partition r, g, b
    r = data[0]
    g = data[1]
    b = data[2]
    # get start row, column index to crop the center
    w_start = int((len(r) - size) / 2)
    l_start = int((len(r[0]) - size) / 2)
    # construct cropped r,g,b array
    cropped_rgb = []
    cropped_rgb.append(crop(r, l_start, w_start, size))
    cropped_rgb.append(crop(g, l_start, w_start, size))
    cropped_rgb.append(crop(b, l_start, w_start, size))
    return cropped_rgb

# takes FORMATTED data as input and randomly crop the image
def rand_crop(data, size):
    # partition r, g, b
    r = data[0]
    g = data[1]
    b = data[2]
    # get random start row, column index
    w_start = randint(0,len(data[0]) - size)
    l_start = randint(0,len(data[0]) - size)
    # construct cropped r,g,b array
    cropped_rgb = []
    cropped_rgb.append(crop(r, l_start, w_start, size))
    cropped_rgb.append(crop(g, l_start, w_start, size))
    cropped_rgb.append(crop(b, l_start, w_start, size))
    return cropped_rgb

def crop(data, l_start, w_start, size):
    cropped = []
    for i in range(l_start, l_start + size):
        row = []
        for j in range(w_start, w_start + size):
            row.append(data[i][j])
        cropped.append(row)
    return cropped

# takes FORMATTED data as input
def rand_horizontal_flip(data, p):
    if (uniform(0,1) < p):
        rgb_flipped = []
        r = horizontal_flip_single_color(data[0])
        g = horizontal_flip_single_color(data[1])
        b = horizontal_flip_single_color(data[2])
        rgb_flipped.append(r)
        rgb_flipped.append(g)
        rgb_flipped.append(b)
        return rgb_flipped
    else:
        return data

def horizontal_flip_single_color(data):
    # flip image horizontally
    for i in range(int(len(data)/2)):
        temp = data[i]
        data[i] = data[len(data) -1 - i]
        data[len(data) -1 - i] = temp
    return data


def avg(a, b):
    return ((a + b) / 2)

def average_rgb(base_image, pairing_image):
    base_r = base_image[0]
    base_g = base_image[1]
    base_b = base_image[2]
    pair_r = pairing_image[0]
    pair_g = pairing_image[1]
    pair_b = pairing_image[2]
    combined_r = list(map(avg, base_r, pair_r))
    combined_g = list(map(avg, base_g, pair_g))
    combined_b = list(map(avg, base_b, pair_b))
    sample_paired = []
    sample_paired.append(combined_r)
    sample_paired.append(combined_g)
    sample_paired.append(combined_b)
    return np.array(sample_paired)

def sample_pair(ip, tg):
    new = []
    sizeofip = ip.shape[0]
    for counter in range(0,sizeofip):
        randnum = randint(0,sizeofip-1)
        new.append(average_rgb(ip[counter], ip[randnum]))
    return (np.array(new), tg)
