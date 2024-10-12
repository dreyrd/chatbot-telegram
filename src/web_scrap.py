import requests
from bs4 import BeautifulSoup

def pegar_titulo(url):
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        titulo = soup.find('h1').get_text()
        
        print(titulo)
        
        
        
pegar_titulo('https://noticias.uol.com.br/cotidiano/ultimas-noticias/2024/09/24/idosa-ocorrencia-namoro-elon-musk-pr.htm')