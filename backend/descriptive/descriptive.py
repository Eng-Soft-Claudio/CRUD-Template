# descriptive/descriptive.py
"""
Este script varre recursivamente uma estrutura de diretórios a partir de um caminho raiz,
identifica todos os arquivos `.py`, e gera um arquivo de saída com estilo de **livro**.

O arquivo de saída possui:
- Uma capa e um sumário (índice) com todos os arquivos rastreados.
- Cada arquivo é tratado como um capítulo, com separadores e numeração.
- Arquivos vazios são ignorados.
- Em caso de erro de leitura, uma mensagem é registrada no local do capítulo correspondente.

Diretórios comuns de desenvolvimento (como venv, __pycache__, etc.) são ignorados.
"""

import os
import sys

# =========================
# --- Configurações ---
# =========================

# Caminho absoluto para o diretório raiz do projeto.
PASTA_RAIZ_PROJETO = '/media/claudioh4x5w6l7/Desenvolvimento/FastAPI-CRUD-Template/'

# Nome do arquivo de saída
NOME_BASE_ARQUIVO_SAIDA = 'Codigo_Fonte.txt'

# Diretórios a serem ignorados durante a varredura
PASTAS_IGNORADAS = (
    '__pycache__', 'descriptive', '.pytest_cache',
    '.git', '.idea', 'node_modules', '.env', 'venv'
)

# Extensões e arquivos a serem monitorados
EXTENSOES_INCLUIDAS = ('.py',)
ARQUIVOS_EXTRAS = ('Dockerfile', 'docker-compose.yml', '.env.exemple', '.env.test')

# Caminho do diretório onde o script está localizado
if getattr(sys, 'frozen', False):
    DIRETORIO_DO_SCRIPT = os.path.dirname(sys.executable)
else:
    DIRETORIO_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

ARQUIVO_SAIDA_CONSOLIDADO = os.path.join(DIRETORIO_DO_SCRIPT, NOME_BASE_ARQUIVO_SAIDA)

# ===============================
# --- Função Principal ---
# ===============================

def gerar_livro_codigo(pasta_raiz: str, arquivo_saida: str, pastas_ignoradas: tuple):
    """
    Varre o diretório raiz do projeto e gera um arquivo no formato de livro contendo
    os códigos Python organizados em capítulos.

    Args:
        pasta_raiz (str): Caminho absoluto para a raiz do projeto.
        arquivo_saida (str): Caminho completo do arquivo de saída a ser gerado.
        pastas_ignoradas (tuple): Diretórios que devem ser ignorados na varredura.

    O arquivo de saída terá:
        - Uma capa com título
        - Um sumário (índice) com os nomes dos arquivos
        - Um capítulo para cada arquivo, com o código formatado
    """
    caminhos_arquivos = []
    capitulos = []

    # Coleta os caminhos de todos os arquivos .py
    for raiz, pastas, arquivos in os.walk(pasta_raiz):
        pastas[:] = [p for p in pastas if p not in pastas_ignoradas]
        for arquivo in arquivos:
            if arquivo.endswith(EXTENSOES_INCLUIDAS) or arquivo in ARQUIVOS_EXTRAS:
                    caminho_abs = os.path.join(raiz, arquivo)
                    caminhos_arquivos.append(caminho_abs)

    caminhos_arquivos.sort()

    # Processa os arquivos e prepara os capítulos
    for caminho_abs in caminhos_arquivos:
        caminho_rel = os.path.relpath(caminho_abs, pasta_raiz)
        try:
            with open(caminho_abs, 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            if not any(l.strip() for l in linhas):
                continue

            capitulos.append({
                'titulo': caminho_rel,
                'linhas': linhas
            })
        except Exception as e:
            capitulos.append({
                'titulo': caminho_rel,
                'linhas': [f"# ERRO AO LER ARQUIVO: {e}\n"]
            })


    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
            escrever_capa_com_logo(f_out)
            escrever_sumario(f_out, capitulos)
            escrever_capitulos(f_out, capitulos)
    except Exception as e:
        print(f"ERRO ao escrever o arquivo final: {e}")

def escrever_capa_com_logo(arquivo):
    """
    Escreve a capa no arquivo de saída.

    Args:
        arquivo (file object): Objeto de arquivo já aberto para escrita.
    """
    largura = 80
    margem = 2
    interior = largura - 2 * margem

    logo_python = [
        "     ____        _   _                  ",
        "    |  _ \\ _   _| |_| |__   ___  _ __   ",
        "    | |_| | | | | __| '_ \\ / _ \\| '_ \\  ",
        "    |  __/| |_| | |_| | | | (_) | | | | ",
        "    |_|    \\__, |\\__|_| |_|\\___/|_| |_| ",
        "           |___/                        "
    ]
    altura_logo = len(logo_python)
    altura_total = altura_logo + 6

    # Topo
    arquivo.write("#" * largura + "\n")
    for _ in range(margem - 1):
        arquivo.write("#" + " " * (largura - 2) + "#\n")

    espaco_superior = (interior - len(logo_python[0])) // 2
    for linha in logo_python:
        arquivo.write("#" + " " * margem + " " * espaco_superior + linha.ljust(len(logo_python[0])) +
                      " " * (interior - len(linha) - espaco_superior) + " " * margem + "#\n")

    for _ in range(margem):
        arquivo.write("#" + " " * (largura - 2) + "#\n")
    arquivo.write("#" * largura + "\n\n")



def escrever_sumario(arquivo, capitulos: list):
    """
    Escreve o sumário no arquivo de saída.

    Args:
        arquivo (file object): Objeto de arquivo já aberto para escrita.
        capitulos (list): Lista de dicionários com os capítulos a serem escritos.
    """
    arquivo.write("=" * 80 + "\n")
    arquivo.write("CÓDIGO-FONTE DO PROJETO\n")
    arquivo.write("=" * 80 + "\n\n")

    arquivo.write("SUMÁRIO\n")
    arquivo.write("-" * 80 + "\n")
    for i, cap in enumerate(capitulos, 1):
        arquivo.write(f"Capítulo {i}: {cap['titulo']}\n")
    arquivo.write("\n\n")


def escrever_capitulos(arquivo, capitulos: list):
    """
    Escreve os capítulos (conteúdo dos arquivos) no arquivo de saída.

    Args:
        arquivo (file object): Objeto de arquivo já aberto para escrita.
        capitulos (list): Lista de dicionários com os capítulos e seu conteúdo.
    """
    for i, cap in enumerate(capitulos, 1):
        arquivo.write("=" * 80 + "\n")
        arquivo.write(f"Capítulo {i}: {cap['titulo']}\n")
        arquivo.write("=" * 80 + "\n\n")
        arquivo.writelines(cap['linhas'])
        arquivo.write("\n\n")


# ========================
# --- Execução ---
# ========================
if __name__ == "__main__":
    if not os.path.isdir(PASTA_RAIZ_PROJETO):
        print(f"ERRO: Caminho inválido: {PASTA_RAIZ_PROJETO}")
    else:
        gerar_livro_codigo(PASTA_RAIZ_PROJETO, ARQUIVO_SAIDA_CONSOLIDADO, PASTAS_IGNORADAS)
