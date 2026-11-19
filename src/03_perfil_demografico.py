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
tabela["pa_idade"] = pd.to_numeric(tabela["pa_idade"], errors="coerce")
tabela["pa_qtdpro"] = pd.to_numeric(tabela["pa_qtdpro"], errors="coerce").fillna(0)
tabela["pa_sexo"] = tabela["pa_sexo"].astype(str)
tabela["Diagnostico"] = tabela["Diagnostico"].fillna("Não informado").astype(str)

# 2. DISTRIBUIÇÃO POR SEXO
sexo = (
    tabela.groupby("pa_sexo", sort=False)["pa_qtdpro"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(9, 6))
sns.barplot(data=sexo, x="pa_sexo", y="pa_qtdpro")
plt.title("Distribuição de Procedimentos por Sexo - Ijuí")
plt.xlabel("Sexo")
plt.ylabel("Quantidade de procedimentos")
plt.tight_layout()
plt.show()

# 3. DISTRIBUIÇÃO POR FAIXA ETÁRIA
tabela["FaixaEtaria"] = pd.cut(
    tabela["pa_idade"],
    bins=[-1, 12, 18, 30, 45, 60, 75, 120],
    labels=[
        "0-12 anos",
        "13-18 anos",
        "19-30 anos",
        "31-45 anos",
        "46-60 anos",
        "61-75 anos",
        "76+ anos"
    ]
)

faixa_etaria = (
    tabela.groupby("FaixaEtaria", observed=False, sort=False)["pa_qtdpro"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))
sns.barplot(data=faixa_etaria, x="FaixaEtaria", y="pa_qtdpro")
plt.title("Distribuição de Procedimentos por Faixa Etária - Ijuí")
plt.xlabel("Faixa etária")
plt.ylabel("Quantidade de procedimentos")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# 4. PRINCIPAIS DIAGNÓSTICOS (CID)
diagnosticos = (
    tabela.groupby("Diagnostico", sort=False)["pa_qtdpro"]
    .sum()
    .nlargest(10)
    .reset_index()
)

plt.figure(figsize=(12, 7))
sns.barplot(data=diagnosticos, x="pa_qtdpro", y="Diagnostico")
plt.title("Top 10 Diagnósticos Atendidos - Ijuí")
plt.xlabel("Quantidade de procedimentos")
plt.ylabel("Diagnóstico")
plt.tight_layout()
plt.show()

# 5. RESUMO DOS RESULTADOS
print("\n===== DISTRIBUIÇÃO POR SEXO =====")
print(sexo.to_string(index=False))

print("\n===== DISTRIBUIÇÃO POR FAIXA ETÁRIA =====")
print(faixa_etaria.to_string(index=False))

print("\n===== PRINCIPAIS DIAGNÓSTICOS =====")
print(diagnosticos.to_string(index=False))
