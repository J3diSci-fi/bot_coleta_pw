import win32gui, win32ui, win32con
import numpy as np
import cv2
import time
import pyautogui
from colorama import init, Fore, Style

# Inicializa o colorama para permitir cores no terminal
init()

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   █████╗ ██╗   ██╗████████╗ ██████╗     ██████╗ ██████╗ ███████╗ ║
    ║  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗██╔════╝ ║
    ║  ███████║██║   ██║   ██║   ██║   ██║    ██████╔╝██████╔╝███████╗ ║
    ║  ██╔══██║██║   ██║   ██║   ██║   ██║    ██╔═══╝ ██╔═══╝ ╚════██║ ║
    ║  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ██║     ██║     ███████║ ║
    ║  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚═╝     ╚═╝     ╚══════╝ ║
    ║                                                                  ║
    ║                           by: hckzn                              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

def find_images(screenshot, image_to_find):
    try:
        img_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)  # Convertendo para RGB
        template = cv2.imread(image_to_find, cv2.IMREAD_COLOR)  # Lendo a imagem do template

            
        if template is None:
            return [], screenshot, -1, -1  # Retorna valores padrão se a imagem não for encontrada
    

        h, w = template.shape[:-1]  # Obtendo as dimensões do template (altura, largura)

        # Realizando a comparação de templates
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)

        found_coords = []

        # Desenhando retângulos na imagem
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
            found_coords.append(pt)

        return found_coords, img_rgb, w, h
    except Exception as e:
        print("Imagem não encontrada:", e)
        return [], screenshot, -1, -1

def click_at_positions(coords, wRect, hRect):
    for x, y in coords:
        pyautogui.moveTo(x + (wRect // 2), y + 20)
        pyautogui.click()
        time.sleep(1)  # Adiciona um pequeno delay entre cliques
    if not coords:
        print('Nenhuma imagem encontrada.')

class DesktopWindow:
    def __init__(self, width, height):
        # Captura a janela principal do desktop
        self.hwnd = win32gui.GetDesktopWindow()

        self.width = width
        self.height = height

    def get_screenshot(self):
        # Captura o contexto do dispositivo (DC)
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        
        # Cria um contexto de dispositivo compatível (CDC)
        cDC = dcObj.CreateCompatibleDC()
        
        # Cria um bitmap compatível com o contexto do dispositivo
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        
        # Seleciona o bitmap no contexto do dispositivo
        cDC.SelectObject(dataBitMap)
        
        # Copia a tela para o bitmap
        cDC.BitBlt((0, 0), (self.width, self.height), dcObj, (0, 0), win32con.SRCCOPY)
        
        # Converte o bitmap em uma matriz numpy
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        # Libera os recursos
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img

def main():
    desktop_width = 1920
    desktop_height = 1080
    desktop = DesktopWindow(desktop_width, desktop_height)

    materiais = {
        "Pó de Esmeril": {"path": "./res/pedreira_amolar.png", "count": 0},
        "Tábua Polida": {"path": "./res/pilha_salgueiro.png", "count": 0},
        "Aço Temperado": {"path": "./res/minerio_ferro.png", "count": 0},
        "Carvão de Pedra": {"path": "./res/nucleo_carvao.png", "count": 0}
    }

    print_banner()

    while True:
        for material, info in materiais.items():
            # Captura a imagem do desktop
            img = desktop.get_screenshot()

            coords, img_with_rectangle, wRect, hRect = find_images(img, info["path"])

            if coords:
                click_at_positions(coords, wRect, hRect)
                info["count"] += len(coords)
                
                # Exibe o log do material encontrado com destaque verde
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {Fore.GREEN}Encontrou - {material}.{Style.RESET_ALL}")
            else:
                pass

        time.sleep(1)  # Aguarda antes de repetir o ciclo

if __name__ == "__main__":
    main()
