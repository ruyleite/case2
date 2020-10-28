#!/usr/bin/python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('yarn').appName('spark-bigquery').getOrCreate()

bucket = "gs://projeto_id_temp"
spark.conf.set('temporaryGcsBucket', bucket)

ga_sessions_= spark.read.format('bigquery').option('table', 'bigquery-public-data.google_analytics_sample.ga_sessions_*').load()
ga_sessions.createOrReplaceTempView('ga_sessions')

products = spark.sql(
    'SELECT distinct hits.product.productSKU as productSKU, hits.product.v2ProductName as ProductName FROM ga_sessions')

hits = spark.sql(
    'SELECT fullVisitorId, visitId, date, hits.hour as,  hits.hitNumber as hitNumber,  hits.page.pagePath as pagePath,  hits.eventInfo.eventCategory as eventCategory, hits.eventInfo.eventAction as eventAction, hits.eventInfo.eventLabel as eventLabel, hits.product.productSKU as productSKU FROM ga_sessions, unnest(hits) as hits')

#Nesse ponto ate poderia fazer via sparkSQL, é so registrar o dataframe como uma TempView
joins = products.join(products,hits.productSKU == products.productSKU, "inner")


joins.write.format('bigquery').option('table', 'wordcount_dataset.resultado_output').save()

