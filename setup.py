import sys
from cx_Freeze import setup, Executable

# Opções de build do cx_Freeze
build_exe_options = {
    "packages": [],
    "includes": [],
    "excludes": [],
    "include_files": [
        ('./res/icon.ico', 'icon.ico'),  # Inclui o ícone do aplicativo
        ('./res/pedreira_amolar.png', 'res/pedreira_amolar.png'),  # Inclui a imagem
        ('./res/pilha_salgueiro.png', 'res/pilha_salgueiro.png'),  # Inclui a imagem
        ('./res/minerio_ferro.png', 'res/minerio_ferro.png'),  # Inclui a imagem
        ('./res/nucleo_carvao.png', 'res/nucleo_carvao.png'),  # Inclui a imagem
    ]
}

# Configuração do executável
exe = Executable(
    script='main.py',  # Substitua 'main.py' pelo nome do seu script Python
    icon='./res/icon.ico'  # Caminho para o ícone
)

# Configuração do setup
setup(
    name='Auto Coleta',
    version='1.0',
    description='Auto Coleta by hckzn',
    options={"build_exe": build_exe_options},
    executables=[exe]
)
