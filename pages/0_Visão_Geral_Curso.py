import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np

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


def wrap_text(text, width):
    import textwrap
    wrapper = textwrap.TextWrapper(width=width)
    wrapped_text = wrapper.fill(text)
    return wrapped_text

def filter_data(etnia, genero, deficiencia, ensinoMedio, turma, conhecimentoPrevio, ultimaFormacao, disciplina_selecionada):
    filtered_df = df_completo
    filtrado =  'filtrado'
    disciplina_selected = 'Todas'
    experiencia_map = {'Sim': 'Sim, já programo', 'Não': 'Não, nunca programei', 'Parcialmente': 'Tenho alguma ideia de programação, já aprendi alguma coisa, mas nunca programei a sério', 'Ambos': 'Ambos'}
    
    if etnia != 'Todas':
        filtered_df = filtered_df[filtered_df['Cor/Etnia:'] == etnia]
    
    if genero != 'Ambos':
        filtered_df = filtered_df[filtered_df['Gênero'] == genero]
    
    if deficiencia != 'Ambos':
        filtered_df = filtered_df[filtered_df['É portador de alguma deficiência? '] == deficiencia]
    
    if ensinoMedio != 'Ambos':
        filtered_df = filtered_df[filtered_df['Você concluiu o ensino médio em instituição de ensino pública ou privada?'] == ensinoMedio]
        
    if ultimaFormacao != 'Todas':
        filtered_df = filtered_df[filtered_df['Preencha sua ÚLTIMA FORMAÇÃO ou formação em curso. '] == ultimaFormacao]
        
    if turma != 'Todas':
        filtered_df = filtered_df[filtered_df['Turma'] == turma]
        
    if conhecimentoPrevio != 'Ambos':
        filtered_df = filtered_df[filtered_df['Você tem algum conhecimento de programação?'] == experiencia_map[conhecimentoPrevio]]
        
    if disciplina_selecionada != 'Todas':
        filtered_df = filtered_df[filtered_df[disciplina_selecionada].notnull()]
        disciplina_selected = disciplina_selecionada
        
    if etnia == 'Todas' and genero == 'Ambos' and deficiencia == 'Ambos' and ensinoMedio == 'Ambos' and ultimaFormacao == 'Todas' and turma == 'Todas' and conhecimentoPrevio =='Ambos' and disciplina_selecionada == 'Todas': 
        filtrado = 'não filtrado'
    
    return filtered_df, filtrado, disciplina_selected

def bar_chart_prep(df_filtred, disciplinas, disciplina_selected):
    if disciplina_selected != 'Todas':
        df_filtred['Media'] = df_filtred[disciplina_selected].round(2)
    else:
        df_filtred['Media'] = df_filtred[disciplinas].mean(axis=1).round(2)
    df_merged_sorted = df_filtred.sort_values(by='Media', ascending=True, na_position='first')
    return df_merged_sorted

def disciplinas_chart_prep(df_filtred):
    
    df_melted = df_filtred.melt(
    id_vars=['Número', 'Email', 'Turma', 'Status', 'CPF', 'Celular', 'Bairro:', 'Cidade:', 'Data de nascimento', 'Gênero', 'Cor/Etnia:', 'É portador de alguma deficiência? ', 'Você concluiu o ensino médio em instituição de ensino pública ou privada?', 'Preencha sua ÚLTIMA FORMAÇÃO ou formação em curso. ', 'Você tem algum conhecimento de programação?', 'Nome Completo', 'Media'],
    value_vars=['Lógica de Programação', 'Banco de Dados', 'Programação Orientada a objetos', 'Frontend Essencial', 'API Restful', 'Desenvolvimento Web'],
    var_name='Disciplina',
    value_name='Nota')
    
    
    return df_melted

def plot_bar_chart_total(df, filtrado_check, disciplina_selected):

    media_grafico = df['Media'].mean().round(2)
    fig = px.bar(df, x='Nome Completo', y='Media', title=f'Visualização da média dos alunos {filtrado_check}',
            color='Media', color_continuous_scale='RdYlGn', range_color=[0, 100])
    fig.update_layout(xaxis_title='Nome Completo', yaxis_title='Média', xaxis_tickangle=-45, width = 1200, height = 500)
    fig.update_layout(coloraxis_colorbar=dict(tickvals=[0, 60, 100],ticktext=['0', '60', '100']))
    fig.update_xaxes(gridcolor='lightgrey')
    fig.update_yaxes(gridcolor='lightgrey')
    fig.update_layout(title_x=0,plot_bgcolor='white', paper_bgcolor='white')

    fig.add_hline(y=media_grafico, line_dash="dash", line_color="black", annotation_text=f"Média do gráfico: {media_grafico}",
                annotation_position="top left")
    
    if disciplina_selected != 'Todas':
        fig.update_layout(title=f'Visualização da média dos alunos na disciplina {disciplina_selected}', title_x=0)
    return fig

def plot_subject_averages(df, disciplinas, filtrado_check):
    avg_scores = df[disciplinas].mean().round(2).sort_values().dropna()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=avg_scores.index, y=avg_scores.values, 
                        marker_color=px.colors.qualitative.Dark2, 
                        text=avg_scores.round(2), 
                        textposition='auto',
                        name='Média por Disciplina'))

    fig.update_layout(
        title=f'Visualização de média por disciplina',
        xaxis_title='Disciplina',
        yaxis_title='Média',
        width=800,
        height=500,
        title_x=0,
        title_y=0.95,
    )

    return fig

def sort_by_discipline(df, discipline):
    df_filtered = df[df['Disciplina'] == discipline]

    df_sorted = df_filtered.sort_values(by='Nota', ascending=False)
    df_merged = pd.merge(df_sorted[['Nome Completo']], df, on='Nome Completo', how='inner')
    
    return df_merged

def plot_melted_chart(df, filtrado_check, disciplina_embaixo):
    disciplinas = list(df['Disciplina'].unique())
    disciplinas.remove(disciplina_embaixo)
    disciplinas = [disciplina_embaixo] + disciplinas
    
    color_discrete_map = {disciplina: color for disciplina, color in zip(disciplinas, px.colors.qualitative.Dark2)}
    
    df['Disciplina'] = pd.Categorical(df['Disciplina'], categories=disciplinas, ordered=True)
    
    
    fig = px.bar(
    df,
    x='Nome Completo',
    y='Nota',
    color='Disciplina',
    barmode='stack',
    title=f'Visualização de notas parciais {filtrado_check}',
    labels={'Nome Completo': 'Nome Completo', 'Nota': 'Somatório das notas', 'Disciplina': 'Disciplina'},
    color_discrete_sequence=px.colors.qualitative.Dark2,
    category_orders={'Disciplina': disciplinas},
    )

    fig.update_layout(
        width=800,
        height=500,
        title_x=0,
        title_y=0.95,
        annotations=[
            dict(
                x=1.52,
                y=1.05,
                xref='paper',
                yref='paper',
                text='Clique nas  disciplinas para adicionar/remover',
                showarrow=False,
                font=dict(
                    size=12,
                    color="black"
                ),
                align="left"
            )
        ]
    )
    return fig

df_completo, df_datas = merge_and_clean_dfs("Base de dados - exemplo.xlsx")

disciplinas = ['Lógica de Programação', 'Banco de Dados', 'Programação Orientada a objetos',
                    'Frontend Essencial', 'API Restful', 'Desenvolvimento Web',
                    'Desenvolvimento Mobile', 'Projeto Aplicado']


col1, col2 = st.columns(2)
with col1:
    etnia = st.selectbox(
        "Selecione a etnia para visualização:",
        ("Todas", "Amarelo", "Branco", "Pardo", "Preto", "Não informado"),
        index=0 
    )

    genero = st.selectbox(
        "Selecione o gênero para visualização:",
        ("Ambos", "Feminino", "Masculino"),
        index=0
    )

    deficiencia = st.selectbox(
        "Portadores de necessidades especiais:",
        ("Ambos", "Sim", "Não"),
        index=0
    )

    ensinoMedio = st.selectbox(
        "Ensino médio em instituição pública ou privada:",
        ("Ambos", "Pública", "Privada"),
        index=0
    )

with col2:
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
    
    disciplinas_opc = disciplinas.copy()
    disciplinas_opc.insert(0, 'Todas')
    disciplina_selecionada = st.selectbox(
        "Disciplina:",
        disciplinas_opc,
        index=0
    )


filtred_df, filtrado_check, disc_selecionada = filter_data(etnia, genero, deficiencia, ensinoMedio, turma, conhecimentoPrevio, ultimaFormacao, disciplina_selecionada)

bar_chart_df = bar_chart_prep(filtred_df,disciplinas, disc_selecionada)

fig = plot_bar_chart_total(bar_chart_df, filtrado_check, disc_selecionada)
st.plotly_chart(fig)

fig_disciplinas = plot_subject_averages(bar_chart_df, disciplinas, filtrado_check)
st.plotly_chart(fig_disciplinas)

df_melted = disciplinas_chart_prep(filtred_df)
disc_opc = df_melted['Disciplina'].unique()
sort_order = st.selectbox(
        "Selecione por qual disciplina deseja ordenar:",
        disc_opc,
        index=0 
    )

df_melted_sorted = sort_by_discipline(df_melted,sort_order)
fig_melted = plot_melted_chart(df_melted_sorted,filtrado_check, sort_order)
st.plotly_chart(fig_melted)