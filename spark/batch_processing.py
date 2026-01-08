from pyspark.sql import SparkSession
from pyspark.sql.functions import ( col, count, avg, sum as spark_sum, max as spark_max, min as spark_min, round as spark_round, desc, asc)
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
import os

def create_spark_session():
    spark =SparkSession.builder\
    .appName("BatchProcessing")\
    .master("local[*]")\
    .getOrCreate()
    return spark

def get_schema():
    schema=StructType([
        StructField("product_id",StringType(),True),
        StructField("Product_name",StringType(),True),
        StructField("category",StringType(),True),
        StructField("discounted_price",FloatType(),True),
        StructField("actual_Price",FloatType(),True),
        StructField("discount_percentage",FloatType(),True),
        StructField("rating",FloatType(),True),
        StructField("rating_count",IntegerType(),True),


    ])
    return schema

    def read_csv_data(spark,file_path,schema):
       df= spark.read\
        .option("header","true")\
        .schema(get_schema())\
        .csv(file_path)
        return df
    
    def clean_data(df):
        df_cleaned=df.filter(col("category").isNotNull())
        df_cleaned=df_cleaned.filter((col("discounted_price") > 0) & (col("rating")>0))
        df_cleaned=df_cleaned.dropna()
        return df_cleaned
    

    def sales_by_category(df_cleaned):
        sales_by_category_df=df_cleaned.groupby("category")\
        .agg(
            count("product_id").alias("total_products"),
            spark_round(avg("discounted_price"),2).alias("avg_discounted_price"),
            spark_round(avg("rating"),2).alias("avg_rating"),
            spark_round(spark_sum("rating_count"),2).alias("total_rating_count")
        )\
        .orderBy(desc("total_products"))
        return sales_by_category_df

        def top_rated_products(df_cleaned,top_n=20):
            top_rated_products_df=df_cleaned.filter((col("rating")>4.5)& (col("rating_count")>35000))\
            .select("product_id","Product_name","category","discounted_price","actual_Price","discount_percentage","rating","rating_count")\
            .orderBy(desc("rating_count"))\
            .limit(top_n)
            return top_rated_products_df

        def save_to__parquet(df,output_path, partition_by=None):
            if partition_by:
                df.write.mode("overwrite").partitionBy(partition_by).parquet(output_path)
            else:
                df.write.mode("overwrite").parquet(output_path)

                
           
