import json
import random
import subprocess
import os
import time

CAMINHO_CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PASTA_DESEJADA = "o cordeiro ajoelha-se para mamar"
CAMINHO_BOOKMARKS = r"C:\Users\artpe\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"

def obter_favoritos():
    if not os.path.exists(CAMINHO_BOOKMARKS):
        print(f"Arquivo não encontrado: {CAMINHO_BOOKMARKS}")
        return []

    with open(CAMINHO_BOOKMARKS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    links = []

    def extrair_links(pasta):
        if "children" in pasta:
            for item in pasta["children"]:
                if item["type"] == "folder" and item["name"] == PASTA_DESEJADA:
                    for link in item["children"]:
                        if link["type"] == "url":
                            links.append(link["url"])
                elif item["type"] == "folder":
                    extrair_links(item)

    for pasta in dados["roots"].values():
        extrair_links(pasta)

    return links

todos_links = obter_favoritos()
links_escolhidos = random.sample(todos_links, 8) if len(todos_links) >= 8 else todos_links

if links_escolhidos:
    subprocess.Popen([CAMINHO_CHROME, "--new-window", links_escolhidos[0]])
    time.sleep(1)
    
    for link in links_escolhidos[1:]:
        subprocess.Popen([CAMINHO_CHROME, link])

    print(f"Sucesso! {len(links_escolhidos)} links abertos.")
else:
    print("Nenhum link encontrado.")