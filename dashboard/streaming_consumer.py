import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, window, from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

# Set Hadoop home to use local winutils
os.environ['HADOOP_HOME'] = r'C:\Users\USER\Project_01\amazon-sales-pipeline\spark\hadoop'

# Create Spark session with Kafka
spark = SparkSession.builder \
    .appName("Amazon Sales Streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0") \
    .getOrCreate()

# Define schema for Amazon sales data
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("category", StringType(), True),
    StructField("discounted_price", DoubleType(), True),
    StructField("actual_price", DoubleType(), True),
    StructField("rating", DoubleType(), True),
    StructField("rating_count", IntegerType(), True)
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "amazon-sales-stream") \
    .load()

# Parse JSON and process
sales_stream = df.selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json(col("json_value"), schema).alias("data")) \
    .select("data.*")

# Calculate real-time metrics
metrics = sales_stream \
    .groupBy("category") \
    .agg(
        avg("discounted_price").alias("avg_price"),
        count("*").alias("sales_count")
    )

# Output to console
query = metrics.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()