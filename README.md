# Análise de Dados do SIA/SUS para Apoio à Gestão Municipal de Saúde — Ijuí/RS

Projeto de análise exploratória e visualização de dados da produção ambulatorial do Sistema Único de Saúde (SIA/SUS) nos estabelecimentos de saúde do município de Ijuí/RS (código IBGE `431020`).

## Fontes de Dados e Período Analisado
* **Fonte:** Sistema de Informações Ambulatoriais do SUS (SIA/SUS - Tabela `pars`), cruzada com tabelas auxiliares do CNES (`cadgerrs`), SIGTAP (`procedimentos`), CBO (`cbo`), CID-10 (`cid`) e IBGE (`tb_municip`).
* **Recorte Geográfico:** Estabelecimentos localizados em Ijuí/RS (`pa_ufmun = '431020'`).
* **Período Analisado:** Competência **Julho de 2026 (`2026-07`)**.

## Ambiente e Tecnologias
* **Banco de Dados:** MySQL 8+ (Banco `dbsia`, tabela dimensional `DIMTEMPO` e view consolidada `pa_ijui`)
* **Linguagem:** Python 3.10+
* **Bibliotecas:** `pandas`, `mysql-connector-python`, `matplotlib`, `seaborn`

## Estrutura do Repositório
* `sql/`: Scripts SQL para criação da dimensão temporal (`DIMTEMPO`) e da view `pa_ijui`.
* `src/`: Scripts Python responsáveis pela extração, tratamento e geração dos gráficos.
* `img/`: Gráficos e visualizações gerados a partir das análises.
* `requirements.txt`: Lista de dependências Python do projeto.

##  Instruções de Execução
1. **Banco de Dados:** Execute `sql/01_dimtempo.sql` para criar a dimensão temporal e `sql/02_view_pa_ijui.sql` para gerar a view `pa_ijui` no banco `dbsia`.
2. **Dependências Python:**
   ```bash
   pip install -r requirements.txt



* **Arthur F. Fontoura** — [GitHub](https://github.com/Arthur-Fontoura)
* * **Kevin adiel** — [GitHub](https://github.com/kevinadieldasilva-crypto)
