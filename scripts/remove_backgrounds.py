from rembg import remove
from PIL import Image
from pathlib import Path
import os

def new_name(path):
    # Create a Path object
    p = Path(path)

    tmp = p.name[:-4:]+"_no_background.png"
    return tmp

IMGS = [ 
    "input.jpg"
]

def rimuovi_sfondo(input_path, output_path):
    """
    Rimuove lo sfondo da un'immagine usando la libreria rembg e salva il risultato.

    Args:
        input_path (str): Il percorso del file immagine di input (es. 'foto.jpg').
        output_path (str): Il percorso dove salvare il file immagine di output (es. 'foto_senza_sfondo.png').
    """
    try:
        # Assicurati che il file esista
        if not os.path.exists(input_path):
            print(f"ERRORE: File non trovato all'indirizzo: {input_path}")
            return

        print(f"Caricamento immagine da: {input_path}")
        
        # 1. Apri l'immagine
        input_image = Image.open(input_path)
        
        # 2. Rimuovi lo sfondo (la parte principale)
        # Il modello scaricherà il modello AI la prima volta che viene eseguito.
        print("Rimozione sfondo in corso...")
        output_image = remove(input_image)
        
        # 3. Salva l'immagine con sfondo trasparente (formato PNG)
        output_image.save(output_path)
        
        print(f"\nOperazione completata con successo!")
        print(f"Immagine salvata in: {output_path}")

    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione: {e}")

for INPUT_FILE in IMGS:
    # 2. Specifica il nome del file di output (deve essere .png per la trasparenza)
    OUTPUT_FILE = new_name(INPUT_FILE)
    rimuovi_sfondo(INPUT_FILE, OUTPUT_FILE)