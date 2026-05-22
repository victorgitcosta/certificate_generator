from rembg import remove
from PIL import Image
import os

# Input image paths
input_images = [
    "img_footer.jpeg",
    "chapaoverflow.jpg"
]

# Output folder
output_folder = "."
os.makedirs(output_folder, exist_ok=True)

for img_path in input_images:
    # Open image
    with open(img_path, "rb") as f:
        input_data = f.read()

    # Remove background
    output_data = remove(input_data)

    # Save output
    filename = os.path.basename(img_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{name}_no_bg.png")

    with open(output_path, "wb") as out:
        out.write(output_data)

    print(f"Saved: {output_path}")