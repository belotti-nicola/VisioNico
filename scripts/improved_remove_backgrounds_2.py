from rembg import remove
from PIL import Image
from pathlib import Path
import os

def new_name(path: str) -> str:
    """
    Generate a new output filename by appending '_no_background.png'
    to the original name (without its extension).

    Args:
        path (str): Path to the input image file.

    Returns:
        str: Suggested output filename.
    """
    p = Path(path)
    return p.stem + "_no_background.png"


SCALE_FACTOR = 4
# List of input images to process
IMAGES = [
    "input.jpg"
]

def remove_background(input_path: str) -> None:
    """
    Remove the background from an image using the rembg library and
    save the result as a PNG with transparency.

    Args:
        input_path (str): Path to the input image file (e.g., 'photo.jpg').
        output_path (str): Path to save the output image file (e.g., 'photo_no_background.png').
    """
    try:
        # Make sure the file exists
        if not os.path.exists(input_path):
            print(f"ERROR: File not found: {input_path}")
            return

        print(f"Loading image from: {input_path}")

        # 1. Open the image
        input_image = Image.open(input_path)

        # 2. Remove the background
        # The AI model will download automatically the first time it is used.
        print("Removing background...")
        output_image = remove(input_image)

        return output_image

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        


def clean_edges(image, output_path: str, threshold=200):
    """
    Rimuove i pixel grigiastri dai bordi forzando la trasparenza
    se l'opacità è bassa.
    """
    image = image.convert("RGBA")
    data = image.getdata()

    new_data = []
    for item in data:
        r, g, b, a = item
        if a < threshold:  # pixel quasi trasparente → rendilo invisibile
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))

    image.putdata(new_data)

    image.save(output_path)

    print("\nOperation completed successfully!")
    print(f"Image saved as: {output_path}")


# Process each image in the list
for input_file in IMAGES:
    output_file = new_name(input_file)
    filtered = remove_background(input_file)
    clean_edges(filtered,output_file)
