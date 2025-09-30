from rembg import remove
from PIL import Image
import os
import numpy as np
from pathlib import Path

# =================================================================
# DESPILLING FUNCTION
# =================================================================

def despill_alpha_halo(img: Image, despill_strength: float = 0.1) -> Image:
    """
    Removes residual color fringe (like gray/white) along transparent edges.
    This technique reduces color where the Alpha channel isn't completely opaque.

    Args:
        img: PIL Image in RGBA format.
        despill_strength: How aggressively to remove the contamination (0.0 to 1.0).
                          0.1 is a good starting point.
    Returns:
        PIL Image with the color fringe removed.
    """
    # Convert to NumPy array for pixel-level processing
    data = np.array(img.convert("RGBA"))
    
    # Separate RGB and Alpha channels
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Identify partially transparent pixels (the soft edges)
    # We work on pixels where Alpha is > 0 and < 255
    mask = (a > 0) & (a < 255)
    
    if np.any(mask):
        # Calculate the despill factor: the more transparent the pixel (low alpha), 
        # the more the RGB color is reduced.
        # This reduces the residual color from the original background.
        despill_factor = 1.0 - ((255.0 - a[mask]) / 255.0) * despill_strength

        # Apply the despill factor to the RGB channels only in the edge area
        r[mask] = (r[mask] * despill_factor).astype(np.uint8)
        g[mask] = (g[mask] * despill_factor).astype(np.uint8)
        b[mask] = (b[mask] * despill_factor).astype(np.uint8)

    # Recombine the channels into a single array
    data[:,:,:4] = np.stack([r, g, b, a], axis=2)
    
    # Return the PIL image
    return Image.fromarray(data, 'RGBA')

# =================================================================

def new_name(path):
    p = Path(path)
    # Assumes file has a 4-character extension (e.g., .jpg)
    base_name = p.name[:-4] 
    return f"output/{base_name}.png"

# --- MODIFIED: Single element list ---
IMGS = [ 
    "input.jpg"
]
# ------------------------------------

def remove_background_and_despill(input_path, output_path, despill_val=0.1):
    """
    Removes the background and applies despilling to eliminate the gray fringe.
    """
    try:
        if not os.path.exists(input_path):
            print(f"ERROR: File not found at: {input_path}")
            return

        print(f"\n--- Processing: {input_path} ---")
        
        # 1. Background Removal
        input_image = Image.open(input_path).convert("RGBA")
        print("Removing background...")
        output_image = remove(input_image) 
        
        # 2. Cleanup (Despilling)
        print("Applying despilling...")
        final_image = despill_alpha_halo(output_image, despill_strength=despill_val) 
        
        # 3. Saving
        # Ensure the output directory exists
        Path("output").mkdir(exist_ok=True)
        final_image.save(output_path)
        
        print(f"Complete! Saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred during execution: {e}")

# --- Execution Loop ---
if __name__ == "__main__":
    for INPUT_FILE in IMGS:
        # The 'new_name' function will now create 'output/input.png'
        OUTPUT_FILE = new_name(INPUT_FILE) 
        # You can adjust 0.1 here if the fringe is too much or too little removed
        remove_background_and_despill(INPUT_FILE, OUTPUT_FILE, despill_val=0.1)
