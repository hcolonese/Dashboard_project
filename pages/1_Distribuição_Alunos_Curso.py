import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

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
"""

st.markdown(header_html, unsafe_allow_html=True)

@st.cache_data
def merge_and_clean_dfs(file_path):
    df_dados = pd.read_excel(file_path, sheet_name='Dados pessoais')
    df_notas = pd.read_excel(file_path, sheet_name='Notas')
    df_datas = pd.read_excel(file_path, sheet_name='Dados pessoais')
    
    merged_df = pd.merge(df_dados, df_notas, on=['Número', 'Nome', 'Sobrenome','Email','Turma'], how='left')
    merged_df['Nome Completo'] = merged_df['Nome'] + ' ' + merged_df['Sobrenome']
    merged_df = merged_df.drop(columns=['Status_y','Nome','Sobrenome'])
    merged_df = merged_df.rename(columns={'Status_x': 'Status'})
    
    duplicate_mask = merged_df.duplicated(subset='Nome Completo', keep=False)
    merged_df.loc[duplicate_mask, 'Nome Completo'] = merged_df['Nome Completo'] + ' №' + merged_df['Número'].astype(str)
    
    return merged_df, df_datas


def second_view_df(df):
    df_melted = df.melt(
    id_vars=['Número', 'Email', 'Turma', 'Status', 'CPF', 'Celular', 'Bairro:', 'Cidade:', 'Data de nascimento', 'Gênero', 'Cor/Etnia:', 'É portador de alguma deficiência? ', 'Você concluiu o ensino médio em instituição de ensino pública ou privada?', 'Preencha sua ÚLTIMA FORMAÇÃO ou formação em curso. ', 'Você tem algum conhecimento de programação?', 'Nome Completo', 'Media'],
    value_vars=['Lógica de Programação', 'Banco de Dados', 'Programação Orientada a objetos', 'Frontend Essencial', 'API Restful', 'Desenvolvimento Web', 'Desenvolvimento Mobile', 'Projeto Aplicado'],
    var_name='disciplina',
    value_name='Nota')
    return df_melted


def filter_data(turma, conhecimentoPrevio, ultimaFormacao):
    filtered_df = df_completo
    filtrado =  'filtrado'
    experiencia_map = {'Sim': 'Sim, já programo', 'Não': 'Não, nunca programei', 'Parcialmente': 'Tenho alguma ideia de programação, já aprendi alguma coisa, mas nunca programei a sério', 'Ambos': 'Ambos'}
        
    if ultimaFormacao != 'Todas':
        filtered_df = filtered_df[filtered_df['Preencha sua ÚLTIMA FORMAÇÃO ou formação em curso. '] == ultimaFormacao]
        
    if turma != 'Todas':
        filtered_df = filtered_df[filtered_df['Turma'] == turma]
        
    if conhecimentoPrevio != 'Ambos':
        filtered_df = filtered_df[filtered_df['Você tem algum conhecimento de programação?'] == experiencia_map[conhecimentoPrevio]]
        
    if ultimaFormacao == 'Todas' and turma == 'Todas' and conhecimentoPrevio =='Ambos': 
        filtrado = 'não filtrado'
    
    return filtered_df, filtrado

def disciplinas_chart_prep(df_filtred):
    
    df_melted = df_filtred.melt(
    id_vars=['Número', 'Email', 'Turma', 'Status', 'CPF', 'Celular', 'Bairro:', 'Cidade:', 'Data de nascimento', 'Gênero', 'Cor/Etnia:', 'É portador de alguma deficiência? ', 'Você concluiu o ensino médio em instituição de ensino pública ou privada?', 'Preencha sua ÚLTIMA FORMAÇÃO ou formação em curso. ', 'Você tem algum conhecimento de programação?', 'Nome Completo'],
    value_vars=['Lógica de Programação', 'Banco de Dados', 'Programação Orientada a objetos', 'Frontend Essencial', 'API Restful', 'Desenvolvimento Web'],
    var_name='Disciplina',
    value_name='Nota')
    
    return df_melted

def statistic_charts(df):
    columns_to_plot = [
    'Gênero', 
    'Cor/Etnia:', 
    'É portador de alguma deficiência? ', 
    'Você concluiu o ensino médio em instituição de ensino pública ou privada?'
    ]

    col_names = [
        'Gênero', 
        'Etnia', 
        'PCD', 
        'Instituição de ensino médio pública ou privada?'
    ]


    fig = make_subplots(rows=2, cols=2, subplot_titles=col_names)

    for i, col in enumerate(columns_to_plot, start=1):
        row = (i - 1) // 2 + 1
        col_pos = (i - 1) % 2 + 1
        
        hist = df[col].value_counts().reset_index()
        hist.columns = ['x', 'y']
        
        fig.add_trace(
            go.Bar(
                x=hist['x'],
                y=hist['y'],
                name=col,
                marker_color=px.colors.qualitative.Dark2,
                hoverinfo='x+y',
            ),
            row=row, col=col_pos
        )

    fig.update_yaxes(title_text="Alunos", row=1, col=1)
    fig.update_yaxes(title_text="Alunos", row=2, col=1)

    fig.update_layout(
        height=800, 
        width=800,
        title_x=0.5,
        title_text="Distribuição dos alunos",
        showlegend=False
    )
    return fig


df_completo, df_datas = merge_and_clean_dfs("Base de dados - exemplo.xlsx")

disciplinas = ['Lógica de Programação', 'Banco de Dados', 'Programação Orientada a objetos',
                    'Frontend Essencial', 'API Restful', 'Desenvolvimento Web',
                    'Desenvolvimento Mobile', 'Projeto Aplicado']


turma_opc = df_completo['Turma'].unique().tolist()
turma_opc.insert(0, 'Todas')
turma = st.selectbox(
    "Turma específica:",
    turma_opc,
    index=0
)

conhecimentoPrevio = st.selectbox(
    "Possui algum conhecimento de programação:",
    ("Ambos", "Sim", "Não", "Parcialmente"),
    index=0
)

ultimaFormacao_opc = df_completo['Preencha sua ÚLTIMA FORMAÇÃO ou formação em curso. '].unique().tolist()
ultimaFormacao_opc.insert(0, 'Todas')
ultimaFormacao = st.selectbox(
    "Última formação ou curso:",
    ultimaFormacao_opc,
    index=0
)


filtred_df, filtrado_check = filter_data(turma, conhecimentoPrevio, ultimaFormacao)
df_melted = disciplinas_chart_prep(filtred_df)


fig = statistic_charts(filtred_df)
st.plotly_chart(fig)
