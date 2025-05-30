import requests
from bs4 import BeautifulSoup
import re

def separar_texto_concatenado(texto):
    # Separa palavras concatenadas com letras maiúsculas no meio
    return re.split(r'(?<=[a-z])(?=[A-Z])', texto)

def limpar_linha(dados_linha):
    """Remove entradas irrelevantes e separa textos agrupados"""
    ignorar = {"TOPO", "DOWNLOAD", ""}
    resultado = []
    for campo in dados_linha:
        if campo.upper() in ignorar:
            continue
        # Verifica se o campo parece ter nomes ou palavras concatenadas
        if len(campo) > 40 and not " " in campo:
            resultado.extend(separar_texto_concatenado(campo))
        else:
            resultado.append(campo.strip())
    return resultado

def scrape_tabelas(ano: int, subopcao: str, opcao: str = None):
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    url = f"{base_url}?ano={ano}&subopcao={subopcao}&opcao={opcao}"

    if subopcao:
        url = f"{base_url}?ano={ano}&subopcao={subopcao}&opcao={opcao}"
    else:
        url = f"{base_url}?ano={ano}&opcao={opcao}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tabela_principal = soup.find("table", class_="tb_base tb_dados")

    if not tabela_principal:
        return []

    dados_tabela = []
    for linha in tabela_principal.find_all("tr"):
        colunas = linha.find_all(["td", "th"])
        dados_linha = [coluna.get_text(strip=True) for coluna in colunas]

        if dados_linha and any(campo.strip() for campo in dados_linha):
            dados_limpos = limpar_linha(dados_linha)
            if dados_limpos:
                dados_tabela.append(dados_limpos)

    return dados_tabela