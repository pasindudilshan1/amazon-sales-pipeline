import os
import sys


if sys.platform == 'win32' and 'HADOOP_HOME' not in os.environ:
    # Create a minimal Hadoop directory structure
    hadoop_home = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hadoop')
    bin_dir = os.path.join(hadoop_home, 'bin')
    os.makedirs(bin_dir, exist_ok=True)
    os.environ['HADOOP_HOME'] = hadoop_home
    
from pyspark.sql import SparkSession
from pyspark.sql.functions import ( col, count, avg, sum as spark_sum, max as spark_max, min as spark_min, round as spark_round, desc, asc, split, regexp_replace, trim, expr)
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

def create_spark_session():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("Amazon Sales Batch Processing") \
        .config("spark.sql.warehouse.dir", "file:///C:/Users/USER/Project_01/amazon-sales-pipeline/spark-warehouse") \
        .config("spark.driver.extraJavaOptions", "-Duser.timezone=GMT") \
        .config("spark.executor.extraJavaOptions", "-Duser.timezone=GMT") \
        .config("spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs", "false") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem") \
        .getOrCreate()
    
   
    spark.sparkContext.setLogLevel("ERROR")
    
    return spark

def get_schema():
    schema = StructType([
        StructField("product_id", StringType(), True),
        StructField("product_name", StringType(), True),
        StructField("category", StringType(), True),
        StructField("discounted_price", StringType(), True),  
        StructField("actual_price", StringType(), True),
        StructField("discount_percentage", StringType(), True),  
        StructField("rating", FloatType(), True),
        StructField("rating_count", StringType(), True),  # Has commas, parse later
        StructField("about_product", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("user_name", StringType(), True),
        StructField("review_id", StringType(), True),
        StructField("review_title", StringType(), True),
        StructField("review_content", StringType(), True),
        StructField("img_link", StringType(), True),
        StructField("product_link", StringType(), True)
    ])
    return schema

def read_csv_data(spark,file_path,schema):
    df= spark.read\
    .option("header","true")\
    .schema(get_schema())\
    .csv(file_path)
    return df

def clean_data(df):
  
    df = df.withColumn("category_array", split(col("category"), "\\|"))
    df = df.withColumn("category", col("category_array").getItem(0))
    df = df.drop("category_array")
    
   
    df = df.withColumn("discounted_price", 
                       expr("try_cast(regexp_replace(discounted_price, '[₹,]', '') as float)"))
    df = df.withColumn("actual_price", 
                       expr("try_cast(regexp_replace(actual_price, '[₹,]', '') as float)"))
    
    # Parse rating_count - remove commas, handle NULL/invalid values
    df = df.withColumn("rating_count", 
                       expr("try_cast(regexp_replace(rating_count, ',', '') as int)"))
    
    # Parse discount_percentage - remove % sign
    df = df.withColumn("discount_percentage", 
                       expr("try_cast(regexp_replace(discount_percentage, '%', '') as float)"))
    
    # Filter only rows with valid critical data
    df = df.filter(col("category").isNotNull())
    df = df.filter(col("product_id").isNotNull())
    df = df.filter(col("discounted_price").isNotNull() & (col("discounted_price") > 0))
    df = df.filter(col("rating").isNotNull() & (col("rating") > 0))
    
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
    top_rated_products_df=df.filter((col("rating")>4.5)& (col("rating_count")>30000))\
    .select("product_id","Product_name","category","discounted_price","actual_Price","discount_percentage","rating","rating_count")\
    .orderBy(desc("rating_count"))\
    .limit(top_n)
    return top_rated_products_df

def save_to_parquet(df, output_path):
    """Save DataFrame to Parquet format using toPandas to avoid Windows Hadoop DLL issues"""
    print(f"Saving to {output_path}...")
    # Convert to pandas and save (bypasses Hadoop issues)
    pandas_df = df.toPandas()
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pandas_df.to_parquet(output_path, index=False, engine='pyarrow')
    print(f"Successfully saved {len(pandas_df)} rows to {output_path}")

def display_result(df, name, num_rows=5):
    print(f"{name}")
    print(f"\n{'='*40  }")
    print(df.show(num_rows,truncate=False))

def main():
    INPUT_CSV_PATH = '../data/raw/amazon.csv'
   
    OUTPUT_PATH = "../data/parquet"
    print("Creating Spark Session...")
    spark = create_spark_session()

    print("Reading CSV data...")
    df = read_csv_data(spark, INPUT_CSV_PATH, get_schema())
    df.show(5, truncate=False)

    print("Cleaning data...")
    df_clean = clean_data(df)
    print(f"Clean data count: {df_clean.count()}")
    
    print("Generating sales by category...")
    sales_by_category_df = sales_by_category(df_clean)
    display_result(sales_by_category_df, "sales_by_category_df Result")
    save_to_parquet(sales_by_category_df, f"{OUTPUT_PATH}/sales_by_category.parquet")

    print("Generating top rated products...")
    top_rated_products_df = top_rated_products(df_clean, top_n=20)
    save_to_parquet(top_rated_products_df, f"{OUTPUT_PATH}/top_rated_products.parquet")
    print("Processing completed successfully.")
    spark.stop()

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")