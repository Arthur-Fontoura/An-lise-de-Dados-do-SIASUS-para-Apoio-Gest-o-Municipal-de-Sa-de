from getpass import getpass
from mysql.connector import connect, Error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

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

formato_reais = FuncFormatter(
    lambda x, _: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

# 1. TRATAMENTO DOS DADOS
colunas_numericas = ["pa_valpro", "pa_valapr", "pa_qtdpro"]
for coluna in colunas_numericas:
    tabela[coluna] = pd.to_numeric(tabela[coluna], errors="coerce").fillna(0)

tabela["Ano"] = pd.to_numeric(tabela["Ano"], errors="coerce")
tabela["Mes"] = pd.to_numeric(tabela["Mes"], errors="coerce")

dados = tabela.dropna(subset=["Ano", "Mes"]).copy()

dados["Periodo"] = pd.to_datetime(
    dados["Ano"].astype(int).astype(str)
    + "-"
    + dados["Mes"].astype(int).astype(str).str.zfill(2)
    + "-01"
)

# 2. VALORES PRODUZIDOS X APROVADOS
total_produzido = dados["pa_valpro"].sum()
total_aprovado = dados["pa_valapr"].sum()

valores = pd.DataFrame({
    "Tipo": ["Produzido", "Aprovado"],
    "Valor": [total_produzido, total_aprovado]
})

plt.figure(figsize=(10, 6))
ax = sns.barplot(data=valores, x="Tipo", y="Valor")
ax.yaxis.set_major_formatter(formato_reais)
plt.title("Valores Produzidos x Aprovados pelo SUS - Ijuí")
plt.xlabel("Tipo de valor")
plt.ylabel("Valor financeiro (R$)")
plt.tight_layout()
plt.show()

# 3. DIFERENÇA ENTRE PRODUZIDOS E APROVADOS
financeiro_mensal = (
    dados.groupby("Periodo")[["pa_valpro", "pa_valapr"]]
    .sum()
    .reset_index()
    .sort_values("Periodo")
)

financeiro_mensal["Diferenca"] = (
    financeiro_mensal["pa_valpro"] - financeiro_mensal["pa_valapr"]
)

plt.figure(figsize=(14, 6))
sns.barplot(data=financeiro_mensal, x="Periodo", y="Diferenca")
plt.axhline(y=0, color="black", linewidth=1)
plt.title("Diferença Mensal entre Valores Produzidos e Aprovados")
plt.xlabel("Período")
plt.ylabel("Diferença financeira (R$)")
plt.gca().yaxis.set_major_formatter(formato_reais)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. EVOLUÇÃO DO GASTO MÉDIO POR PROCEDIMENTO
gasto_medio = (
    dados.groupby("Periodo")[["pa_valpro", "pa_qtdpro"]]
    .sum()
    .reset_index()
    .sort_values("Periodo")
)

gasto_medio["Media"] = (
    gasto_medio["pa_valpro"] / gasto_medio["pa_qtdpro"].replace(0, float("nan"))
)

plt.figure(figsize=(14, 6))
sns.lineplot(data=gasto_medio, x="Periodo", y="Media", marker="o")
plt.title("Evolução do Valor Médio por Procedimento Ambulatorial - Ijuí")
plt.xlabel("Período")
plt.ylabel("Valor médio por procedimento (R$)")
plt.gca().yaxis.set_major_formatter(formato_reais)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. RESUMO DOS RESULTADOS
diferenca_total = total_produzido - total_aprovado
total_procedimentos = dados["pa_qtdpro"].sum()

print("\n===== RECURSOS FINANCEIROS =====")
print(f"Total produzido: R$ {total_produzido:,.2f}")
print(f"Total aprovado: R$ {total_aprovado:,.2f}")
print(f"Diferença entre produzido e aprovado: R$ {diferenca_total:,.2f}")

if total_procedimentos > 0:
    media_geral = total_produzido / total_procedimentos
    print(f"Valor médio por procedimento: R$ {media_geral:,.2f}")

print("\n===== MAIOR VALOR MÉDIO MENSAL =====")
maior_media = gasto_medio.loc[gasto_medio["Media"].idxmax()]
print(f"Período: {maior_media['Periodo'].strftime('%m/%Y')}")
print(f"Valor médio: R$ {maior_media['Media']:.2f}")

print("\n===== DIFERENÇA FINANCEIRA =====")
print(
    "Diferença positiva: valores produzidos superiores aos aprovados."
    if diferenca_total > 0
    else "Diferença negativa: valores aprovados superiores aos produzidos."
    if diferenca_total < 0
    else "Os valores produzidos e aprovados são iguais."
)
