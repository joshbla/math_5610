# Future Work:
# Squircles (squares with rounded edges) gen
# mxn rather than nxn

from PIL import Image, ImageDraw


def genCircle(n, isfilled):
    # Grids less than 3 x 3 are meaningless
    # x o x
    # o x o
    # x o x

    fileName = f'test{n}.png'

    if isfilled:
        fillcolor = 'white'
    else:
        fillcolor = 'black'

    drawing = Image.new(mode = 'RGB', size = (n, n), color = (0,0,0))
    draw = ImageDraw.Draw(drawing)
    # Outline is ontop of fill not another layer around it
    draw.ellipse((0, 0, n - 1, n - 1), fill = fillcolor, outline ='white')
    drawing.save(fileName)

for n in range(3, 24):
    genCircle(n, True)

im = Image.open('test3.png')

# Save the resulting image
im.save('testt.png')

for n in range(4, 24):
    # Open the first image
    image1 = Image.open('testt.png')

    # Open the second image
    image2 = Image.open(f'test{n}.png')

    # Get the width and height of the first image
    width1, height1 = image1.size

    # Get the width and height of the second image
    width2, height2 = image2.size

    # Create a new image with the combined width and maximum height
    result_image = Image.new('RGB', (width1 + width2, max(height1, height2)))

    # Paste the first image onto the new image
    result_image.paste(image1, (0, 0))

    # Paste the second image onto the new image
    result_image.paste(image2, (width1, 0))

    # Save the resulting image
    result_image.save('testt.png')