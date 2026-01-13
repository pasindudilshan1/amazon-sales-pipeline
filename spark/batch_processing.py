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
        df=df.filter(col("category").isNotNull())
        df=df.filter((col("discounted_price") > 0) & (col("rating")>0))
        df=df.dropna()
        return df
    

    def sales_by_category(df):
        sales_by_category_df=df.groupby("category")\
        .agg(
            count("product_id").alias("total_products"),
            spark_round(avg("discounted_price"),2).alias("avg_discounted_price"),
            spark_round(avg("rating"),2).alias("avg_rating"),
            spark_round(spark_sum("rating_count"),2).alias("total_rating_count")
        )\
        .orderBy(desc("total_products"))
        return sales_by_category_df

    def top_rated_products(df,top_n=20):
            top_rated_products_df=df.filter((col("rating")>4.5)& (col("rating_count")>35000))\
            .select("product_id","Product_name","category","discounted_price","actual_Price","discount_percentage","rating","rating_count")\
            .orderBy(desc("rating_count"))\
            .limit(top_n)
            return top_rated_products_df

    def save_to_parquet(df,output_path, partition_by=None):
            if partition_by:
                df.write.mode("overwrite").partitionBy(partition_by).parquet(output_path)
            else:
                df.write.mode("overwrite").parquet(output_path)

    def display_result(df, name, num_rows=5):
        print(f"{name}")
        print(f"\n{'='*40  }")
        print(df.show(num_rows,truncate=False))
    
    def main():

        INPUT_CSV_PATH ='../data/raw/amazon.csv'
        OUTPUT_PATH ='../data/parquet'
        print("Creating Spark Session...")
        spark= create_spark_session()

        print("Reading CSV data...")
        df= read_csv_data(spark,INPUT_CSV_PATH,get_schema())
        df.show(5,truncate=False)

        df_clean= clean_data(df)
        sales_by_category_df= sales_by_category(df_clean)
        display_result(sales_by_category_df, "sales_by_category_df Result")
        save_to_parquet(sales_by_category_df, f"{OUTPUT_PATH}/sales_by_category", partition_by='category')


        top_rated_products_df=top_rated_products(df_clean,top_n=20)
        save_to_parquet(top_rated_products_df,f"{OUTPUT_PATH}/top_rated_products", partition_by='category')
    print("Processing completed successfully.")
        spark.stop()
        if __name__=="__main__":
            try:
                main()
            except Exception as e:
                print(f"Error occurred: {e}")