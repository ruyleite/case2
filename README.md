# Premissas
1. Uso da Cloud GCP
2. Como Oracle não é "supportado", assume que esteja em um ambiente on-premisse com conecção por Interconnect ou algum serviço gerenciado de Oracla DB para GCP, ex "Accenture Managed Services for Oracle" encontrado no marketplace da GCP.

# Arquitetura
![](/arquitetura_gcp.png)

Temos 3 sources as seguintes carateristicas.
1. SalesForce - realtime/near realtime, usando Streamin API
2. Oracle - D-1 e realtime/near realtime, com Oracle Goden Gate usando "Plugins" para gcp, seja para armazenar no GS e Pub/Sub. Configurado por time ou tamanho de arquivo, acionado o que vier primeiro.
3. Google Analytics - D-1 com schedules, de forma automatica na propria ferramenta ou atravez de chamada de API por algum agente de schedule não mencionado no desenho.

Como armazenamento do Datalake será usado o Bigquery.

O Pub/Sub como fila de streaming, com consumidor o Dataflow.

O componente Cloud Dataflow irá gravar as informações no BigQuery e/ou Cloud Storage.

O componente Cloud EndPoints é utilizado para ser chamado pelo SalesForce via Streamin API, grando no pub/sub e interagindo com Cloud ML para aplicação de modelos.

Para informações D-1 originarias do Oracle, as mesmas serão gravadas no Cloud Storage, um triggers para uma cloud Function que ira disparar um Job em Cluster Dataproc, esse ultimo pode ser substituido por Dataflow, uma fez a estrutura do dado é o mesmo, e armazenar no Bigquery.

O Google Analytics/360 tem a opção de exportar os dados para Bigquery nativamente. O conteudo exportado pode ser consumido diretamente dessa tabela ou transformado por um job em spark, ou mesmo Jobs Bigquery, em tabelas de mais facil entendimento por parte o usuario.

# MER
Como a exportação dos dados do Google Analytics 360 para o Bigquery é Tabular, a informação possui a seguinte visão estruturada:

![](/BQ-Rows.png)

Para Datalake, uma unica tabela já suficiente.

Podemos usar essa tabela como uma rawdata e usar algum processo para transformar uma estrutura mais User-friendly e ou em uma estrutura de BI, dividido em dimensoes e fatos.

![](/mer_simples.png)


# Código
1. Contagem de Pageviews;

SELECT
  COUNT(*) as qtd_pageviews
FROM [bigquery-public-data.google_analytics_sample.ga_sessions_*], unnest(hits) as hits 
WHERE hits.type = "PAGE"

2. Número de sessões por usuário;

SELECT fullVisitorId, COUNT(totals.visits) AS Num_Sessoes
FROM [bigquery-public-data.google_analytics_sample.ga_sessions_*]
GROUP BY fullVisitorId

3. Sessões distintas por data;

SELECT date, 
SUM(totals.visits) AS Sessoes
FROM [bigquery-public-data.google_analytics_sample.ga_sessions_*]
GROUP BY date

4. Média de duração da sessão por data;

SELECT date, SUM(totals.timeOnSite)/COUNT(totals.visits) AS Media_Duração
FROM [bigquery-public-data.google_analytics_sample.ga_sessions_*]
GROUP BY date

5. Sessões diárias por tipo de browser;

SELECT date, device.browser AS Browser,
SUM(totals.visits) AS sessions
FROM [bigquery-public-data.google_analytics_sample.ga_sessions_*]
GROUP BY date, device.browser

# Exemplo em spark.
veja o arquivo bigquery.py
