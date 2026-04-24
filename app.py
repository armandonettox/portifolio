import streamlit as st
import requests

# Configuracao da pagina
st.set_page_config(page_title="Portifolio Armando Netto", layout="wide")

# Funcao para buscar dados do Github
def buscar_github(usuario):
    url = f"https://api.github.com/users/{usuario}/repos"
    response = requests.get(url)
    return response.json()

#  HEADER 
st.title("Armando Netto")
st.subheader("Cientista de Dados | Data Science")
st.write("Extraio conhecimento e padrões de grandes volumes de dados utilizando Estatística Avançada e IA para resolver problemas complexos de negócio..")

st.write("---")

#  SECAO DE PROJETOS 
st.header("Projetos")
meu_usuario = "armandonettox" 

if st.button('Carregar Projetos'):
    repos = buscar_github(meu_usuario)
    
    # Criando 2 colunas para os cards
    col1, col2 = st.columns(2)
    
    for i, repo in enumerate(repos[:4]): # Pega os 4 primeiros repositorios
        # Alterna entre coluna 1 e coluna 2
        alvo = col1 if i % 2 == 0 else col2
        with alvo:
            st.info(f"**{repo['name']}**")
            st.write(repo['description'] if repo['description'] else "Sem descricao")
            st.write(f"Link: {repo['html_url']}")
            st.write("---")