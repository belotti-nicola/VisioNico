from rembg import remove
from PIL import Image
from pathlib import Path
import os

def new_name(path: str) -> str:
    """
    Generate a new output filename by appending '_no_background.png'
    to the original name (without its extension).
    """
    p = Path(path)
    return p.stem + "_no_background.png"

# Function to clean edges (remove gray halo pixels)
def clean_edges(image: Image.Image, threshold: int = 180) -> Image.Image:
    """
    Force low-opacity pixels to become fully transparent,
    removing gray/halo artifacts around the object.

    Args:
        image (PIL.Image.Image): Input RGBA image.
        threshold (int): Alpha threshold (0–255). Pixels with alpha below this
                         value will be set to fully transparent.

    Returns:
        PIL.Image.Image: Cleaned image.
    """
    image = image.convert("RGBA")
    data = image.getdata()

    new_data = []
    for r, g, b, a in data:
        if a < threshold:
            # Force transparency if pixel is too weak (gray halo)
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))

    image.putdata(new_data)
    return image

def remove_background_and_merge(input_path: str, output_path: str, bg_color=(255, 255, 255, 255)) -> None:
    """
    Remove the background from an image, clean gray halos,
    and merge the result onto a solid background color.

    Args:
        input_path (str): Path to the input image (e.g., "photo.jpg").
        output_path (str): Path to save the final image (e.g., "photo_clean.png").
        bg_color (tuple): RGBA tuple for background color. Default is white.
    """
    try:
        if not os.path.exists(input_path):
            print(f"ERROR: File not found: {input_path}")
            return

        print(f"Loading image from: {input_path}")

        input_image = Image.open(input_path)

        print("Removing background...")
        no_bg = remove(input_image)

        print("Cleaning edge artifacts...")
        no_bg = clean_edges(no_bg, threshold=100)

        background = Image.new("RGBA", no_bg.size, bg_color)
        background.paste(no_bg, mask=no_bg.split()[3])  # use alpha channel

        background.save(output_path)
        print("\nOperation completed successfully!")
        print(f"Image saved as: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
IMAGES = ["input.jpg"]

for input_file in IMAGES:
    output_file = new_name(input_file)
    remove_background_and_merge(input_file, output_file, bg_color=(255, 255, 255, 255))
