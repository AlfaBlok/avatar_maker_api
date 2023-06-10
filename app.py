from flask import Flask, send_file
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image, ImageDraw
import random
import tempfile

app = Flask(__name__)

# Define the Gaussian function
def gaussian(x, y, a1, a2, b1, b2,c1,c2,c3,c):
    return np.exp(-(a1*(x+a2)**2 + b1*(y+b2)**2)) + c*np.exp(-((x+c1)**2 + c2*(y+c3)**2))

def generate_avatar(file_name):
    # Generate coordinates
    x = np.linspace(-2, 2, 10)
    y = np.linspace(-2, 2, 10)
    X, Y = np.meshgrid(x, y)

    # Randomize parameters
    a1 = random.uniform(-0.5, 0.5)
    a2 = random.uniform(-0.5, 0.5)
    b1 = random.uniform(-0.5, 0.5)
    b2 = random.uniform(-0.5, 0.5)
    b1 = random.uniform(-0.5, 0.5)
    c = random.uniform(-0.5, 0.5)
    c1 = random.uniform(-0.5, 0.5)
    c2 = random.uniform(-0.5, 0.5)
    c3 = random.uniform(-0.5, 0.5)

    # Calculate Z values
    Z = gaussian(X, Y, a1, a2, b1, b2,c1,c2,c3,c)
    # Randomize colormap
    hex_colors = ["#0E0B13", "#616161", "#A160F1", "#72E249", "#1BDCDF", "#F460FF", "#F06087", "#FCD842", "#C3B48E", "#FF9F20","#3929FA"]
    colors = random.sample(hex_colors, k=4)
    cmap = mcolors.LinearSegmentedColormap.from_list("", colors)

    # Plot
    fig, ax = plt.subplots(figsize=(5, 5), dpi=80)
    img = ax.imshow(Z, cmap=cmap, interpolation='nearest')

    # Remove frame
    ax.axis('off')
    plt.tight_layout(pad=0)

    # Save figure
    plt.savefig("temp.png", bbox_inches='tight', pad_inches=0, transparent=True)

    # Open the saved image and apply circular crop
    im = Image.open("temp.png")

    # Create a white circle of the same size as the image
    mask = Image.new('L', im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + im.size, fill=255)

    # Add the mask to the image as an alpha channel
    im.putalpha(mask)
    im.save(file_name)

@app.route('/avatar')
def avatar():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        generate_avatar(temp.name)
        return send_file(temp.name, mimetype='image/png')
    
    
if __name__ == '__main__':
    app.run() #port=8000