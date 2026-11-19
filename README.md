# Análise de Produção Ambulatorial (SIA/SUS) — Ijuí/RS

Projeto desenvolvido para análise exploratória e visualização de dados da produção ambulatorial do Sistema Único de Saúde (SIA/SUS) no município de Ijuí/RS (código IBGE `431020`).

## Fontes de Dados e Período Analisado
* **Base de Dados:** Sistema de Informações Ambulatoriais do SUS (SIA/SUS - Tabela `pars`), integrada às tabelas auxiliares de estabelecimentos (`cadgerrs`), procedimentos (`procedimentos`), ocupações (`cbo`), diagnósticos (`cid`) e municípios (`tb_municip`).
* **Recorte Geográfico:** Estabelecimentos de saúde localizados em Ijuí/RS (`pa_ufmun = '431020'`).
* **Período Analisado:** [INSERIR PERÍODO EXATO DOS DADOS — Ex: Janeiro de 2024 a Dezembro de 2025].

## Tecnologias Utilizadas
* **Banco de Dados:** MySQL 8+
* **Linguagem:** Python 3.10+
* **Bibliotecas:** `pandas`, `mysql-connector-python`, `matplotlib`, `seaborn`

## Instruções de Execução

### 1. Configuração do Banco de Dados (MySQL)
1. Certifique-se de que o banco `dbsia` está criado e populado com as tabelas base do SIA/SUS.
2. Execute o script `sql/01_dimtempo.sql` para criar e popular a tabela de granularidade temporal (`DIMTEMPO`).
3. Execute o script `sql/02_view_pa_ijui.sql` para criar a view consolidada `pa_ijui`.

### 2. Configuração do Ambiente Python
Clone o repositório e instale as dependências:
```bash
git clone <LINK_DO_SEU_REPOSITORIO>
cd analise-sia-sus-ijui
pip install -r requirements.txt
