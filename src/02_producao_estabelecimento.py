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

# 1. RANKING DE PRODUÇÃO POR ESTABELECIMENTO
ranking = (
    tabela.groupby("Estabelecimento")["pa_qtdpro"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(12, 7))
sns.barplot(data=ranking, x="pa_qtdpro", y="Estabelecimento")
plt.title("Ranking de Produção por Estabelecimento - Ijuí")
plt.xlabel("Quantidade de procedimentos produzidos")
plt.ylabel("Estabelecimento")
plt.tight_layout()
plt.show()

# 2. COMPARAÇÃO: PRODUZIDOS X APROVADOS
comparacao = (
    tabela.groupby("Estabelecimento")[["pa_qtdpro", "pa_qtdapr"]]
    .sum()
    .reset_index()
)

comparacao_melt = comparacao.melt(
    id_vars="Estabelecimento",
    value_vars=["pa_qtdpro", "pa_qtdapr"],
    var_name="Tipo",
    value_name="Quantidade"
)

comparacao_melt["Tipo"] = comparacao_melt["Tipo"].replace({
    "pa_qtdpro": "Produzidos",
    "pa_qtdapr": "Aprovados"
})

plt.figure(figsize=(14, 7))
sns.barplot(data=comparacao_melt, x="Estabelecimento", y="Quantidade", hue="Tipo")
plt.title("Procedimentos Produzidos x Aprovados por Estabelecimento")
plt.xlabel("Estabelecimento")
plt.ylabel("Quantidade de procedimentos")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Tipo de produção")
plt.tight_layout()
plt.show()

# 3. RESUMO DOS RESULTADOS
print("\n===== RANKING DE PRODUÇÃO =====")
print(ranking.to_string(index=False))

print("\n===== COMPARAÇÃO PRODUZIDOS X APROVADOS =====")
print(comparacao.to_string(index=False))

print("\n===== TOTAIS GERAIS =====")
total_produzidos = tabela["pa_qtdpro"].sum()
total_aprovados = tabela["pa_qtdapr"].sum()
print(f"Total produzido: {total_produzidos}")
print(f"Total aprovado: {total_aprovados}")

if total_produzidos > 0:
    percentual_aprovado = (total_aprovados / total_produzidos) * 100
    print(f"Percentual aprovado: {percentual_aprovado:.2f}%")
