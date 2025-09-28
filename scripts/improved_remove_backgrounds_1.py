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

def remove_background(input_path: str, output_path: str,TARGET_SCALE_FACTOR: int) -> None:
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
        W,H = input_image.size
        input_image.thumbnail(
            (int(W/TARGET_SCALE_FACTOR),int(H/TARGET_SCALE_FACTOR))
            )

        # 2. Remove the background
        # The AI model will download automatically the first time it is used.
        print("Removing background...")
        output_image = remove(input_image,
                              alpha_matting=True,
                              alpha_matting_foreground_threshold=240,
                              alpha_matting_background_threshold=10,
                              alpha_matting_erode_size=10)

        # 3. Save the image with a transparent background (PNG format)
        output_image.save(output_path)

        print("\nOperation completed successfully!")
        print(f"Image saved as: {output_path}")

    except Exception as e:
        print(f"An error occurred during processing: {e}")

# Process each image in the list
for input_file in IMAGES:
    output_file = new_name(input_file)
    remove_background(input_file, output_file,SCALE_FACTOR)
