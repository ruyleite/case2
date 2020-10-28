# Premissas
1. Uso da Cloud GCP
2. Como Oracle não é "supportado", assume que esteja em um ambiente on-premisse com conecção por Interconnect ou algum serviço gerenciado de Oracla DB para GCP, ex "Accenture Managed Services for Oracle" encontrado no marketplace da GCP.

# Arquitetura
![](/arquitetura.png)

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

Podemos usar essa tabela como uma rawdata e usar algum processo para transformar uma uma estrutura User-friendly.

# Código
1. Contagem de Pageviews;
2. Número de sessões por usuário;
3. Sessões distintas por data;

SELECT date, 
SUM(totals.visits) AS sessions
FROM [google.com:analytics-bigquery:dataset.ga_sessions_20121028]
GROUP BY date

4. Média de duração da sessão por data;
5. Sessões diárias por tipo de browser;

# Exemplo em spark
