from getpass import getpass
from mysql.connector import connect, Error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def usar_conexao(acao):
    try:
        with connect(
            host="localhost",
            user=input("Usuário: "),
            password=getpass("Senha: ")
        ) as connection:
            return acao(connection)
    except Error as e:
        print("Ocorreu um erro ao conectar com o BD:", e)

def carregar_dados(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dbsia.pa_ijui")
        return pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)

tabela = usar_conexao(carregar_dados)

sns.set_theme(style="darkgrid")
plt.rcParams["figure.figsize"] = (12, 6)

# 1. TRATAMENTO DOS DADOS
tabela["MunicipioPaciente"] = (
    tabela["MunicipioPaciente"]
    .fillna("Não informado")
    .astype(str)
    .str.strip()
)

tabela["pa_qtdpro"] = pd.to_numeric(tabela["pa_qtdpro"], errors="coerce").fillna(0)

municipio_ijui = (
    tabela["MunicipioEstabelecimento"]
    .dropna()
    .astype(str)
    .mode()
    .iloc[0]
)

municipio_local = municipio_ijui.strip().casefold()

tabela["Origem"] = tabela["MunicipioPaciente"].apply(
    lambda x: (
        "Ijuí" if x.casefold() == municipio_local
        else "Outros municípios" if x != "Não informado"
        else "Não informado"
    )
)

# 2. RANKING DOS MUNICÍPIOS DE ORIGEM
municipios = (
    tabela[tabela["MunicipioPaciente"] != "Não informado"]
    .groupby("MunicipioPaciente", sort=False)["pa_qtdpro"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(12, 7))
sns.barplot(data=municipios, x="pa_qtdpro", y="MunicipioPaciente")
plt.title("Top 10 Municípios de Origem dos Pacientes - Ijuí")
plt.xlabel("Quantidade de procedimentos")
plt.ylabel("Município de origem")
plt.tight_layout()
plt.show()

# 3. COMPARAÇÃO: IJUÍ X OUTROS MUNICÍPIOS
origem = (
    tabela.groupby("Origem", sort=False)["pa_qtdpro"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(data=origem, x="Origem", y="pa_qtdpro")
plt.title("Origem dos Atendimentos Realizados em Ijuí")
plt.xlabel("Município de residência")
plt.ylabel("Quantidade de procedimentos")
plt.tight_layout()
plt.show()

# 4. RESUMO DOS RESULTADOS
total_ijui = tabela.loc[tabela["Origem"] == "Ijuí", "pa_qtdpro"].sum()
total_outros = tabela.loc[tabela["Origem"] == "Outros municípios", "pa_qtdpro"].sum()
total_nao_informado = tabela.loc[tabela["Origem"] == "Não informado", "pa_qtdpro"].sum()
total_geral = tabela["pa_qtdpro"].sum()

print("\n===== FLUXOS REGIONAIS E ACESSO =====")
print(f"Município de referência: {municipio_ijui}")
print(f"\nProcedimentos de moradores de Ijuí: {total_ijui}")
print(f"Procedimentos de outros municípios: {total_outros}")
print(f"Procedimentos sem município informado: {total_nao_informado}")

if total_geral > 0:
    percentual_outros = (total_outros / total_geral) * 100
    print(f"\nPercentual de procedimentos de outros municípios: {percentual_outros:.2f}%")

print("\n===== TOP 10 MUNICÍPIOS DE ORIGEM =====")
print(municipios.to_string(index=False))
