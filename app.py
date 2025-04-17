import streamlit as st
import pandas as pd

# Título
st.title("📊 Análise de Reprovações de Alunos")

# Lê o CSV
df = pd.read_csv("trypa5.csv", sep=",")

# Filtro: apenas reprovados
reprovados = df[df['Situacao'] == 'Reprovacao']

# Mostrar dataframe completo se quiser
if st.checkbox("Mostrar todos os reprovados"):
    st.dataframe(reprovados)

# Contagem por disciplina
st.subheader("📌 Disciplinas com mais reprovações")
contagem = reprovados['Unidade Curricular Pendente'].value_counts()
st.bar_chart(contagem)

# Agrupamento por disciplina e estudante
st.subheader("📚 Detalhamento por disciplina e estudante")
agrupado1 = reprovados.groupby(['Unidade Curricular Pendente', 'Estudante', 'Situacao']).size().reset_index(name='Total')
st.dataframe(agrupado1)

# Agrupamento por estudante
st.subheader("👨‍🎓 Disciplinas pendentes por aluno e semestre")
agrupado2 = reprovados.groupby(['Estudante','Semestre','Unidade Curricular Pendente', 'Situacao']).size().reset_index(name='Total')
st.dataframe(agrupado2)

# Download das tabelas processadas
st.subheader("📥 Baixar relatórios")

csv1 = agrupado1.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Baixar Disciplina vs Aluno (2024)",
    data=csv1,
    file_name='202401byDisc.csv',
    mime='text/csv'
)

csv2 = agrupado2.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Baixar Aluno vs Disciplina (2024)",
    data=csv2,
    file_name='AlunoToDisc2024.csv',
    mime='text/csv'
)
