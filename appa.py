import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Relatório de Reprovações", layout="wide")

st.title("📊 Relatório Interativo de Reprovações")

# Lê o CSV
df = pd.read_csv("trypa5.csv", sep=",")
reprovados = df[df['Situacao'] == 'Reprovacao']

st.markdown("Selecione um aluno ou uma disciplina para visualizar as reprovações.")

col1, col2 = st.columns(2)

# 🔍 Por aluno
with col1:
    st.subheader("👨‍🎓 Buscar por aluno")
    lista_alunos = sorted(reprovados['Estudante'].unique())
    aluno_escolhido = st.selectbox("Escolha um aluno", lista_alunos)

    if aluno_escolhido:
        dados_aluno = reprovados[reprovados['Estudante'] == aluno_escolhido][['Semestre', 'Unidade Curricular Pendente', 'Situacao']]
        st.write(f"Reprovações de **{aluno_escolhido}**:")
        st.dataframe(dados_aluno)

# 🔍 Por disciplina
with col2:
    st.subheader("📚 Buscar por disciplina")
    lista_disciplinas = sorted(reprovados['Unidade Curricular Pendente'].unique())
    disciplina_escolhida = st.selectbox("Escolha uma disciplina", lista_disciplinas)

    if disciplina_escolhida:
        dados_disciplina = reprovados[reprovados['Unidade Curricular Pendente'] == disciplina_escolhida][['Estudante', 'Semestre', 'Situacao']]
        st.write(f"Alunos reprovados em **{disciplina_escolhida}**:")
        st.dataframe(dados_disciplina)
        
# 📊 Análises adicionais: Disciplinas e Alunos que mais demandam atenção
st.markdown("---")
st.subheader("🔎 Análises de atenção imediata")

col5, col6 = st.columns(2)

# 🚨 Disciplinas com mais reprovações
with col5:
    st.markdown("### 📌 Disciplinas com mais reprovações")
    reprovacoes_por_disciplina = reprovados['Unidade Curricular Pendente'].value_counts().reset_index()
    reprovacoes_por_disciplina.columns = ['Disciplina', 'Número de Reprovações']
    st.dataframe(reprovacoes_por_disciplina)

# 🚨 Alunos com mais reprovações
with col6:
    st.markdown("### 🚨 Alunos com mais reprovações")
    reprovacoes_por_aluno = reprovados['Estudante'].value_counts().reset_index()
    reprovacoes_por_aluno.columns = ['Aluno', 'Número de Reprovações']
    st.dataframe(reprovacoes_por_aluno)


st.markdown("---")
st.subheader("📈 Visualizações gráficas")

col7, col8 = st.columns(2)

# 📊 Gráfico de barras: Disciplinas com mais reprovações
with col7:
    st.markdown("#### 📌 Gráfico: Disciplinas com mais reprovações")
    chart_disc = alt.Chart(reprovacoes_por_disciplina.head(10)).mark_bar(color='crimson').encode(
        x=alt.X('Número de Reprovações:Q', title='Nº de Reprovações'),
        y=alt.Y('Disciplina:N', sort='-x', title='Disciplina')
    ).properties(height=400)
    st.altair_chart(chart_disc, use_container_width=True)

# 📊 Gráfico de barras: Alunos com mais reprovações
with col8:
    st.markdown("#### 🚨 Gráfico: Alunos com mais reprovações")
    chart_aluno = alt.Chart(reprovacoes_por_aluno.head(10)).mark_bar(color='darkblue').encode(
        x=alt.X('Número de Reprovações:Q', title='Nº de Reprovações'),
        y=alt.Y('Aluno:N', sort='-x', title='Aluno')
    ).properties(height=400)
    st.altair_chart(chart_aluno, use_container_width=True)

# 📥 Exportar dados filtrados
st.markdown("---")
st.subheader("📥 Exportar dados completos")

col3, col4 = st.columns(2)

with col3:
    csv_alunos = reprovados[['Estudante','Unidade Curricular Pendente','Situacao','Semestre']].sort_values(by='Estudante')
    csv_bytes_alunos = csv_alunos.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Baixar relatório por aluno",
        data=csv_bytes_alunos,
        file_name="reprovacoes_por_aluno.csv",
        mime="text/csv"
    )

with col4:
    csv_disciplinas = reprovados[['Unidade Curricular Pendente','Estudante','Situacao','Semestre']].sort_values(by='Unidade Curricular Pendente')
    csv_bytes_disciplinas = csv_disciplinas.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Baixar relatório por disciplina",
        data=csv_bytes_disciplinas,
        file_name="reprovacoes_por_disciplina.csv",
        mime="text/csv"
    )
