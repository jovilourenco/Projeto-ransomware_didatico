import os
import webbrowser

def mostrar_imagem():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(base_dir, "assets", "alert_image.png")

    if os.path.exists(caminho_imagem):
        webbrowser.open(f"file://{caminho_imagem}")
    else:
        print("Imagem não encontrada:", caminho_imagem)