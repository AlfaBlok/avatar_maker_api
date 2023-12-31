import io
from flask import Flask, send_file, Response
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image, ImageDraw
import random

app = Flask(__name__)

# Define the Gaussian function
def gaussian(x, y, a1, a2, b1, b2, c1, c2, c3, c):
    return np.exp(-(a1*(x+a2)**2 + b1*(y+b2)**2)) + c*np.exp(-((x+c1)**2 + c2*(y+c3)**2))

def generate_avatar():
    # Generate coordinates
    x = np.linspace(-2, 2, 24)
    y = np.linspace(-2, 2, 24)
    X, Y = np.meshgrid(x, y)

    # Randomize parameters
    a1 = random.uniform(0.1, 2)
    a2 = random.uniform(-0.5, 0.5)
    b1 = random.uniform(-0.5, 0.5)
    b2 = random.uniform(-0.5, 0.5)
    b1 = random.uniform(0.1, 2)
    c = random.uniform(-0.5, 0.5)
    c1 = random.uniform(-0.5, 0.5)
    c2 = random.uniform(-0.5, 0.5)
    c3 = random.uniform(-0.5, 0.5)

    # Calculate Z values
    Z = gaussian(X, Y, a1, a2, b1, b2, c1, c2, c3, c)

    # Randomize colormap
    hex_colors = [  "#A160F1", "#72E249", "#1BDCDF", "#F460FF", "#F06087", "#FCD842", "#FF9F20","#3929FA"]  #"#0E0B13", "#616161", "#C3B48E"
#    hex_colors = ["#0E0B13", "#616161", "#A160F1", "#72E249", "#1BDCDF", "#F460FF", "#F06087", "#FCD842", "#C3B48E", "#FF9F20","#3929FA"]
    constant_color = "#EA3EFF"
    #we add the constant color to the colormap
    colors = random.sample(hex_colors, k=3)
    colors.append(constant_color)

    cmap = mcolors.LinearSegmentedColormap.from_list("", colors)

    # Plot
    fig, ax = plt.subplots(figsize=(5, 5), dpi=80)
    img = ax.imshow(Z, cmap=cmap, interpolation='nearest')

    # Remove frame
    ax.axis('off')
    plt.tight_layout(pad=0)

    # Save figure to BytesIO object
    img_io = io.StringIO()
    plt.savefig(img_io, format='svg', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

    # Get the SVG content
    svg = img_io.getvalue()

    # Add SVG mask for circular crop
    svg_masked = svg.replace('<svg ', '<svg clip-path="url(#myCircle)" ', 1)
    svg_masked = svg_masked.replace('</svg>', '<defs><clipPath id="myCircle"><circle cx="50%" cy="50%" r="40%" /></clipPath></defs></svg>', 1)

    return svg_masked


def generate_avatar_old():
    # Generate coordinates
    x = np.linspace(-2, 2, 24)
    y = np.linspace(-2, 2, 24)
    X, Y = np.meshgrid(x, y)

    # Randomize parameters
    a1 = random.uniform(0.1, 2)
    a2 = random.uniform(-0.5, 0.5)
    b1 = random.uniform(-0.5, 0.5)
    b2 = random.uniform(-0.5, 0.5)
    b1 = random.uniform(0.1, 2)
    c = random.uniform(-0.5, 0.5)
    c1 = random.uniform(-0.5, 0.5)
    c2 = random.uniform(-0.5, 0.5)
    c3 = random.uniform(-0.5, 0.5)

    # Calculate Z values
    Z = gaussian(X, Y, a1, a2, b1, b2, c1, c2, c3, c)

    # Randomize colormap
    hex_colors = [  "#A160F1", "#72E249", "#1BDCDF", "#F460FF", "#F06087", "#FCD842", "#FF9F20","#3929FA"]  #"#0E0B13", "#616161", "#C3B48E"
    constant_color = "#EA3EFF"
    #we add the constant color to the colormap
    colors = random.sample(hex_colors, k=3)
    colors.append(constant_color)

    cmap = mcolors.LinearSegmentedColormap.from_list("", colors)

    

    # Plot
    fig, ax = plt.subplots(figsize=(5, 5), dpi=80)
    img = ax.imshow(Z, cmap=cmap, interpolation='nearest')

    # Remove frame
    ax.axis('off')
    plt.tight_layout(pad=0)

    # Save figure to BytesIO object
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

    # Open the saved image and apply circular crop
    img_io.seek(0)
    im = Image.open(img_io)

    # Create a white circle of the same size as the image
    mask = Image.new('L', im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + im.size, fill=255)

    # Add the mask to the image as an alpha channel
    im.putalpha(mask)
    
    # Save final image to BytesIO object
    final_img_io = io.BytesIO()
    im.save(final_img_io, format='png')
    final_img_io.seek(0)

    return final_img_io

@app.route('/avatar')
def avatar():
    svg = generate_avatar()
    return Response(svg, mimetype='image/svg+xml')


@app.route('/hello')
def hello():
    return("Hello World!")    


if __name__ == '__main__':
    app.run() #port=8000