# Análise de Produção Ambulatorial (SIA/SUS) — Ijuí/RS

Projeto de análise exploratória e visualização de dados da produção ambulatorial do Sistema Único de Saúde (SIA/SUS) nos estabelecimentos de saúde do município de Ijuí/RS (código IBGE `431020`).

## Fontes de Dados e Período Analisado
* **Fonte:** Sistema de Informações Ambulatoriais do SUS (SIA/SUS - Tabela `pars`), cruzada com tabelas auxiliares do CNES (`cadgerrs`), SIGTAP (`procedimentos`), CBO (`cbo`), CID-10 (`cid`) e IBGE (`tb_municip`).
* **Recorte Geográfico:** Estabelecimentos localizados em Ijuí/RS (`pa_ufmun = '431020'`).
* **Período Analisado:** Competência **Julho de 2026 (`2026-07`)**.

## Ambiente e Tecnologias
* **Banco de Dados:** MySQL 8+ (Banco `dbsia`, tabela dimensional `DIMTEMPO` e view consolidada `pa_ijui`)
* **Linguagem:** Python 3.10+
* **Bibliotecas:** `pandas`, `mysql-connector-python`, `matplotlib`, `seaborn`

## Instruções de Execução

1. **Banco de Dados:** Execute `sql/01_dimtempo.sql` para criar a dimensão temporal e `sql/02_view_pa_ijui.sql` para gerar a view `pa_ijui` no banco `dbsia`.
2. **Dependências Python:**
   ```bash
   pip install -r requirements.txt
