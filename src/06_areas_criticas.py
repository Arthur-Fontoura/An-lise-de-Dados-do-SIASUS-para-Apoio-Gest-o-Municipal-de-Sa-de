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
colunas_numericas = ["pa_qtdpro", "pa_qtdapr", "pa_valpro", "pa_valapr"]
for coluna in colunas_numericas:
    tabela[coluna] = pd.to_numeric(tabela[coluna], errors="coerce").fillna(0)

colunas_texto = ["Procedimento", "Ocupacao", "Diagnostico", "Estabelecimento"]
for coluna in colunas_texto:
    tabela[coluna] = (
        tabela[coluna]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

tabela["Informacoes"] = (
    tabela["Procedimento"] + " "
    + tabela["Ocupacao"] + " "
    + tabela["Diagnostico"]
)

# 2. ONCOLOGIA: QUIMIOTERAPIA E RADIOTERAPIA
quimioterapia = tabela["Procedimento"].str.contains(r"quimioter|quimio", na=False)
radioterapia = tabela["Procedimento"].str.contains(r"radioter|radio", na=False)

oncologia = pd.DataFrame({
    "Procedimento": ["Quimioterapia", "Radioterapia"],
    "Produzidos": [
        tabela.loc[quimioterapia, "pa_qtdpro"].sum(),
        tabela.loc[radioterapia, "pa_qtdpro"].sum()
    ],
    "Aprovados": [
        tabela.loc[quimioterapia, "pa_qtdapr"].sum(),
        tabela.loc[radioterapia, "pa_qtdapr"].sum()
    ]
})

oncologia_melt = oncologia.melt(
    id_vars="Procedimento",
    value_vars=["Produzidos", "Aprovados"],
    var_name="Tipo",
    value_name="Quantidade"
)

plt.figure(figsize=(10, 6))
sns.barplot(data=oncologia_melt, x="Procedimento", y="Quantidade", hue="Tipo")
plt.title("Oncologia: Procedimentos Produzidos x Aprovados")
plt.xlabel("Procedimento")
plt.ylabel("Quantidade de procedimentos")
plt.legend(title="Tipo")
plt.tight_layout()
plt.show()

# 3. SAÚDE MENTAL: PSIQUIATRIA E PSICOLOGIA
psiquiatria = tabela["Informacoes"].str.contains(r"psiquiatr|saude mental|saúde mental", na=False)
psicologia = tabela["Informacoes"].str.contains(r"psicolog", na=False)

saude_mental = pd.DataFrame({
    "Especialidade": ["Psiquiatria", "Psicologia"],
    "Quantidade": [
        tabela.loc[psiquiatria, "pa_qtdpro"].sum(),
        tabela.loc[psicologia, "pa_qtdpro"].sum()
    ]
})

plt.figure(figsize=(10, 6))
sns.barplot(data=saude_mental, x="Especialidade", y="Quantidade")
plt.title("Atendimentos de Saúde Mental - Ijuí")
plt.xlabel("Especialidade")
plt.ylabel("Quantidade de atendimentos")
plt.tight_layout()
plt.show()

# 4. ATENÇÃO BÁSICA E DOENÇAS CRÔNICAS
ubs = tabela["Estabelecimento"].str.contains(r"\bubs\b|unidade basica|unidade básica", na=False)
consultas_basicas = tabela["Procedimento"].str.contains(r"consulta|atendimento individual|atencao basica|atenção básica", na=False)
doencas_cronicas = tabela["Diagnostico"].str.contains(r"hipertens|diabet|neoplas|cancer|câncer|doenca cronica|doença crônica", na=False)

atencao_basica = pd.DataFrame({
    "Categoria": ["Atendimentos em UBS", "Consultas básicas", "Doenças crônicas"],
    "Quantidade": [
        tabela.loc[ubs, "pa_qtdpro"].sum(),
        tabela.loc[consultas_basicas, "pa_qtdpro"].sum(),
        tabela.loc[doencas_cronicas, "pa_qtdpro"].sum()
    ]
})

plt.figure(figsize=(12, 6))
sns.barplot(data=atencao_basica, x="Categoria", y="Quantidade")
plt.title("Atenção Básica e Doenças Crônicas - Ijuí")
plt.xlabel("Categoria")
plt.ylabel("Quantidade de procedimentos")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# 5. RESUMO DOS RESULTADOS
print("\n===== ONCOLOGIA =====")
print(oncologia.to_string(index=False))

print("\n===== SAÚDE MENTAL =====")
print(saude_mental.to_string(index=False))

print("\n===== ATENÇÃO BÁSICA =====")
print(atencao_basica.to_string(index=False))

print("\n===== TOTAIS DAS ÁREAS CRÍTICAS =====")
print(f"Procedimentos oncológicos produzidos: {oncologia['Produzidos'].sum()}")
print(f"Procedimentos oncológicos aprovados: {oncologia['Aprovados'].sum()}")
print(f"Atendimentos de saúde mental: {saude_mental['Quantidade'].sum()}")
print(f"Procedimentos identificados na atenção básica: {atencao_basica['Quantidade'].sum()}")
