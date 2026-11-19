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
            print("Conexão estabelecida:", connection)
            return acao(connection)
    except Error as e:
        print("Ocorreu um erro ao conectar com o BD:", e)

def carregar_dados(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dbsia.pa_ijui")
        return pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)

tabela = usar_conexao(carregar_dados)

# Configuração visual
sns.set_theme(style="darkgrid")
plt.rcParams["figure.figsize"] = (12, 6)

# 1. QUANTIDADE DE PROCEDIMENTOS POR PERÍODO
ultimo_ano = tabela["Ano"].max()
ultimo_mes = tabela.loc[tabela["Ano"] == ultimo_ano, "Mes"].max()

ultimo_registro = tabela[
    (tabela["Ano"] == ultimo_ano) &
    (tabela["Mes"] == ultimo_mes)
]

ultimo_bimestre = ultimo_registro["AnoBimestre"].iloc[0]
ultimo_trimestre = ultimo_registro["AnoTrimestre"].iloc[0]

dados_mes = tabela[(tabela["Ano"] == ultimo_ano) & (tabela["Mes"] == ultimo_mes)]
dados_bimestre = tabela[tabela["AnoBimestre"] == ultimo_bimestre]
dados_trimestre = tabela[tabela["AnoTrimestre"] == ultimo_trimestre]

total_mes = dados_mes["pa_qtdpro"].sum()
total_bimestre = dados_bimestre["pa_qtdpro"].sum()
total_trimestre = dados_trimestre["pa_qtdpro"].sum()

periodos = ["Último mês", "Último bimestre", "Último trimestre"]
quantidades = [total_mes, total_bimestre, total_trimestre]

plt.figure()
sns.barplot(x=periodos, y=quantidades)
plt.title("Procedimentos Ambulatoriais - Ijuí")
plt.xlabel("Período")
plt.ylabel("Quantidade de procedimentos")
plt.tight_layout()
plt.show()

# 2. DISTRIBUIÇÃO POR PROCEDIMENTO
procedimentos = (
    dados_trimestre
    .groupby("Procedimento")["pa_qtdpro"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(12, 7))
sns.barplot(data=procedimentos, x="pa_qtdpro", y="Procedimento")
plt.title("Top 10 Procedimentos Ambulatoriais - Ijuí")
plt.xlabel("Quantidade de procedimentos")
plt.ylabel("Procedimento")
plt.tight_layout()
plt.show()

# 3. EVOLUÇÃO TEMPORAL DA DEMANDA
evolucao = (
    tabela.groupby(["Ano", "Mes"])["pa_qtdpro"]
    .sum()
    .reset_index()
    .sort_values(by=["Ano", "Mes"])
)

evolucao["Periodo"] = (
    evolucao["Ano"].astype(str)
    + "-"
    + evolucao["Mes"].astype(str).str.zfill(2)
)

plt.figure(figsize=(14, 6))
sns.lineplot(data=evolucao, x="Periodo", y="pa_qtdpro", marker="o")
plt.title("Evolução Mensal dos Procedimentos Ambulatoriais - Ijuí")
plt.xlabel("Período")
plt.ylabel("Quantidade de procedimentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. IDENTIFICAÇÃO DOS PICOS E QUEDAS
print("\n===== RESUMO DA PRODUÇÃO AMBULATORIAL =====")
print(f"Último mês: {total_mes} procedimentos")
print(f"Último bimestre: {total_bimestre} procedimentos")
print(f"Último trimestre: {total_trimestre} procedimentos")

maior_demanda = evolucao.loc[evolucao["pa_qtdpro"].idxmax()]
menor_demanda = evolucao.loc[evolucao["pa_qtdpro"].idxmin()]

print("\n===== EVOLUÇÃO DA DEMANDA =====")
print(f"Pico de demanda: {maior_demanda['Periodo']} ({maior_demanda['pa_qtdpro']} procedimentos)")
print(f"Menor demanda: {menor_demanda['Periodo']} ({menor_demanda['pa_qtdpro']} procedimentos)")
