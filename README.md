# Arquitetura

# MER
Como a exportação dos dados do Google Analytics 360 para o Bigquery é Tabular, a informação possui a seguinte visão estruturada:

![](/BQ-Rows.png)

Podemos usar essa tabela com uma rawdata e transformar uma uma estrutura User-friendly.

# Código
1. Contagem de Pageviews;
2. Número de sessões por usuário;
3. Sessões distintas por data;
4. Média de duração da sessão por data;
5. Sessões diárias por tipo de browser;

# Exemplo em spark
