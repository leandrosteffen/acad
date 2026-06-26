from faker import Faker
import pandas as pd

fake = Faker('pt_BR')

df = pd.read_excel("dados.xlsx")

nomes_unicos = df["Nome"].drop_duplicates()

mapa = {
    nome: fake.name()
    for nome in nomes_unicos
}

df["Nome"] = df["Nome"].map(mapa)

df.to_excel("dados_anonimizados.xlsx", index=False)