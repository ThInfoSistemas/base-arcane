from langchain.docstore.document import Document
from typing import List
from langchain_community.document_loaders import PyPDFLoader
import requests
from bs4 import BeautifulSoup

def html_para_texto_rag(html_str: str) -> str:
    #from django.utils.html import strip_tags
    #texto_limpo = strip_tags(html)
    soup = BeautifulSoup(html_str, "html.parser")
    texto_final = []

    for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
        texto = tag.get_text(strip=True)

        if not texto:
            continue

        if tag.name in ["h1", "h2", "h3"]:
            texto_formatado = f"\n\n### {texto.upper()}"
        elif tag.name == "li":
            texto_formatado = f" - {texto}"
        else:
            texto_formatado = texto

        texto_final.append(texto_formatado)
        
    return "\n".join(texto_final).strip()


def gerar_documentos(instance) -> List[Document]:
    documentos = []
    if instance.documento:
        extensao = instance.documento.name.split('.')[-1].lower()
        if extensao == 'pdf':
            loader = PyPDFLoader(instance.documento.path)
            pdf_doc = loader.load()
            documentos += pdf_doc
            
    if instance.conteudo:
        documentos.append(Document(page_content=instance.conteudo))
    if instance.site:
        site_url = instance.site if instance.site.startswith('https://') else f'https://{instance.site}'
        content = requests.get(site_url, timeout=10).text
        content = html_para_texto_rag(content)
        documentos.append(Document(page_content=instance.conteudo))

    return documentos