import os
import platform
import ctypes
import subprocess

def mostrar_imagem():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(base_dir, "assets", "alert_image.png")

    if not os.path.exists(caminho_imagem):
        print("Imagem não encontrada:", caminho_imagem)
        return

    sistema = platform.system()

    try:
        if sistema == "Windows":
            # Windows
            ctypes.windll.user32.SystemParametersInfoW(20, 0, caminho_imagem, 3)

        elif sistema == "Darwin":
            # macOS
            script = f'''
            osascript -e 'tell application "Finder" to set desktop picture to POSIX file "{caminho_imagem}"'
            '''
            subprocess.run(script, shell=True)

        elif sistema == "Linux":
            # GNOME (Ubuntu, etc.)
            subprocess.run([
                "gsettings", "set",
                "org.gnome.desktop.background",
                "picture-uri",
                f"file://{caminho_imagem}"
            ])

        else:
            print("Sistema não suportado")

    except Exception as e:
        print("Erro ao definir papel de parede:", e)