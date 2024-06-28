import streamlit as st


# Function to convert image to base64 format
def image_to_base64(image_path):
    import base64
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Company logo image (assuming it's in the same directory)
logo_path = "logo serratec azul.png"  # Adjust path as per your file structure
iamgem_path = "Logo--png branca.png"
# HTML and CSS for custom header
header_html = f"""
<style>
.st-emotion-cache-1gv3huu{{
    background-color: aliceblue;
    background-image: "logo serratec azul.png";
}}
.st-emotion-cache-12fmjuu{{
    background-color: #a8ccf0;
}}
.st-emotion-cache-1yiq2ps{{
    background-color: aliceblue;
}}
.header {{
    padding: 10px;
    background-color:;
    color: white;
    display: flex;
    align-items: center;
}}
.logo-img {{
    width: 100px;  /* Adjust size as needed */
    margin-right: 20px;
}}
</style>
<div class="header">
    <img src="data:image/png;base64,{image_to_base64(logo_path)}" class="logo-img">
    <h1>Dashboards Informativos Serratec</h1>
</div>
"""

# Render the custom header using st.markdown
st.markdown(header_html, unsafe_allow_html=True)

# Sidebar content
st.sidebar.success("Escolha uma das visualizações na barra ao lado.")

# Main content
presentation_content = """
## Sobre Mim

Olá! Eu sou Henrique Colonese Echternacht, um profissional de 24 anos, natural de Petrópolis, RJ. Desenvolvi esse projeto como parte do processo seletivo de prestação de serviço em Análise de Dados ao Serratec.

O Objetivo principal foi extrair alguns insights do desempenho dos alunos sobre diferentes perspectivas. Na guia de visão geral, temos alguns gráficos, apresentando as média dos alunos, podendo ser filtrados conforme necessário.
Já na guia de distribuição dos alunos, a ideia foi trazer uma visão estatística sobre equilibrio entre gênero, etnia, pessoas portadores de necessidades especiais e escolaridade, também podendo ser filtrados por turma ou formação por exemplo.

### Educação

- **Mestrado** em Ciência da computação, UFMG (dez/2024)

- **Bacharel** em Ciência da computação, UFJF (jan/2023), sendo reconhecido pela Sociedade Brasileira de Computação (SBC) como **Estudante Destaque**.

### Habilidades

- **Linguagens de Programação**: C#, Python, SQL
- **Ferramentas e Tecnologias**: .NET, Angular, Pytorch, Excel, Streamlit
---

"""

st.markdown(presentation_content)