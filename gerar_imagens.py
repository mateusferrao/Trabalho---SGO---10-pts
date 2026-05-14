"""
Gera PNGs dos diagramas PlantUML usando o servidor público plantuml.com
Uso: python gerar_imagens.py
Requer: pip install requests
"""

import zlib
import os
import requests
import urllib3

def encode6bit(b):
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'
    return '?'

def append3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) +
            encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F))

def encode64(data):
    res = ""
    n = len(data)
    for i in range(0, n - 2, 3):
        res += append3bytes(data[i], data[i+1], data[i+2])
    rem = n % 3
    if rem == 2:
        res += append3bytes(data[n-2], data[n-1], 0)
    elif rem == 1:
        res += append3bytes(data[n-1], 0, 0)
    return res

def encode_plantuml(text):
    compressed = zlib.compress(text.encode('utf-8'))
    return encode64(compressed[2:-4])  # strip zlib header/checksum

DIAGRAMAS = [
    "diagrama-de-caso-de-uso",
    "diagrama-de-classes",
    "diagrama-de-pacotes",
    "diagrama-de-componentes",
    "diagrama-de-componentes-sem-requisições",
    "diagrama-de-implantacao",
]

def main():
    os.makedirs("imagens", exist_ok=True)
    for nome in DIAGRAMAS:
        puml_path = f"codigos/{nome}.puml"
        if not os.path.exists(puml_path):
            print(f"SKIP (não encontrado): {puml_path}")
            continue
        with open(puml_path, "r", encoding="utf-8") as f:
            conteudo = f.read()
        encoded = encode_plantuml(conteudo)
        url = f"https://www.plantuml.com/plantuml/png/{encoded}"
        try:
            try:
                r = requests.get(url, timeout=30)
            except requests.exceptions.SSLError:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                r = requests.get(url, timeout=30, verify=False)
            if r.status_code == 200:
                out_path = f"imagens/{nome}.png"
                with open(out_path, "wb") as out:
                    out.write(r.content)
                print(f"OK  {out_path}")
            else:
                print(f"ERR {r.status_code} → {nome}")
        except Exception as e:
            print(f"ERR {nome}: {e}")

if __name__ == "__main__":
    main()
