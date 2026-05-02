[README.md](https://github.com/user-attachments/files/27294372/README.md)
# 📈 Dashboard de Análise de Ações Brasileiras — B3 (2024)

Análise exploratória do desempenho de 10 ações do Ibovespa ao longo de 2024, com foco em retorno acumulado, volatilidade, correlação entre ativos e comparativo setorial frente ao índice Ibovespa.

---

## 📊 Análises Realizadas

| # | Análise | Descrição |
|---|---------|-----------|
| 1 | **Retorno Acumulado** | Evolução do retorno de cada ativo vs Ibovespa ao longo do ano |
| 2 | **Volatilidade Anualizada** | Risco de cada ativo com o retorno anual em destaque |
| 3 | **Matriz de Correlação** | Correlação entre os retornos diários de todos os ativos |
| 4 | **Desempenho Setorial** | Retorno mensal médio por setor (bancário, energia, varejo etc.) vs Ibovespa |
| 5 | **Risco x Retorno** | Gráfico de dispersão posicionando cada ativo em quadrantes de risco/retorno |
| 6 | **Sazonalidade Setorial** | Heatmap do retorno médio mensal por setor ao longo dos 12 meses |

---

## 🗂️ Estrutura do Projeto

```
acoes-b3-dashboard/
│
├── data/
│   ├── gerar_dados.py          # Simulação de dados históricos com parâmetros reais
│   ├── acoes_b3_2024.csv       # Preços diários dos 10 ativos (dias úteis 2024)
│   └── ibovespa_2024.csv       # Série histórica do índice Ibovespa (benchmark)
│
├── outputs/
│   ├── 01_retorno_acumulado.png
│   ├── 02_volatilidade.png
│   ├── 03_correlacao.png
│   ├── 04_desempenho_setorial.png
│   ├── 05_risco_retorno.png
│   └── 06_sazonalidade_setorial.png
│
├── analise_acoes.py            # Script principal com todas as análises
└── README.md
```

---

## 📦 Ativos Analisados

| Ticker | Empresa | Setor |
|--------|---------|-------|
| PETR4 | Petrobras | Energia |
| VALE3 | Vale | Mineração |
| ITUB4 | Itaú Unibanco | Bancário |
| BBDC4 | Bradesco | Bancário |
| BBAS3 | Banco do Brasil | Bancário |
| ABEV3 | Ambev | Consumo |
| MGLU3 | Magazine Luiza | Varejo |
| RENT3 | Localiza | Varejo |
| WEGE3 | WEG | Indústria |
| SUZB3 | Suzano | Papel/Celulose |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **pandas** — manipulação de séries temporais financeiras
- **numpy** — cálculo de retornos, volatilidade e correlação
- **matplotlib** — visualizações de linha, barras e dispersão
- **seaborn** — heatmaps de correlação e sazonalidade
- **Power BI** — dashboard interativo com filtros por ativo, setor e período

---

## ▶️ Como Executar

```bash
# Clone o repositório
git clone https://github.com/eddie478/acoes-b3-dashboard
cd acoes-b3-dashboard

# Instale as dependências
pip install pandas matplotlib seaborn numpy

# Gere os dados históricos
python data/gerar_dados.py

# Execute as análises
python analise_acoes.py
```

Os gráficos serão salvos automaticamente na pasta `outputs/`.

> **Nota:** Os dados foram simulados com base em parâmetros reais de volatilidade e retorno do mercado brasileiro em 2024. Para dados reais, substituir a fonte pela API do Yahoo Finance (`yfinance`) ou pela API da B3.

---

## 📌 Principais Achados

- O setor bancário foi o de melhor desempenho em 2024, superando consistentemente o Ibovespa
- MGLU3 apresentou a maior volatilidade do período, com retorno negativo expressivo
- A correlação entre ativos do mesmo setor (bancário) é alta (>0.70), reduzindo o benefício de diversificação intra-setor
- O gráfico risco x retorno evidencia BBAS3 e WEGE3 como destaques positivos em relação ao benchmark
- A sazonalidade setorial mostra queda generalizada nos meses de setembro e outubro

---

## 👤 Autor

**Clayton Liberatori Gomes**  
Estudante de Ciência Matemática — Ênfase em Análise de Dados | UFRJ  
[LinkedIn](https://linkedin.com/in/claytonlgomes) · [GitHub](https://github.com/eddie478)
