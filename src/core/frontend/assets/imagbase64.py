# Script para converter imagem JPEG para base64
import base64
from pathlib import Path

def jpeg_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Converter sua imagem JPEG
image_path = r"C:\Users\F147176\Documents\GitLab_Elisa\projetos-inteligencia\miamiga\src\core\frontend\assets\imagem1.jpeg"
base64_string = jpeg_to_base64(image_path)
print(f"data:image/jpeg;base64,{base64_string}")