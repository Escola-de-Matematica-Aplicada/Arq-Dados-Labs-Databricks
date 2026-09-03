"""Simula a execução do seed lodlog_lab3_seed_v3.py num Spark local com Delta."""
import os, sys, time
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

WAREHOUSE = "/tmp/claude-0/-workspaces/f209aedd-7cbf-4af5-840f-f53030ae5fea/scratchpad/warehouse"

builder = (SparkSession.builder.appName("lodlog-sim")
    .master("local[4]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", WAREHOUSE)
    .config("spark.driver.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.hadoop.javax.jdo.option.ConnectionURL",
            f"jdbc:derby:;databaseName={WAREHOUSE}/metastore_db;create=true")
    .enableHiveSupport())
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

t0 = time.time()
seed_path = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/Labs/lodlog_lab3_seed_v3.py"
src = open(seed_path).read()
exec(compile(src, seed_path, "exec"), {"spark": spark, "__name__": "__main__"})
print(f"\n=== SEED CONCLUÍDO em {time.time()-t0:.0f}s ===")
