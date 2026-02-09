FROM jupyter/pyspark-notebook:x86_64-spark-3.5.0

USER root

# Dodajemy tylko Delta Lake JAR-y do Sparka
RUN curl -L https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.0/delta-spark_2.12-3.2.0.jar -o ${SPARK_HOME}/jars/delta-spark_2.12-3.2.0.jar && \
    curl -L https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar -o ${SPARK_HOME}/jars/delta-storage-3.2.0.jar

# Włączamy rozszerzenia Delta Lake
RUN echo "spark.sql.extensions io.delta.sql.DeltaSparkSessionExtension" >> ${SPARK_HOME}/conf/spark-defaults.conf && \
    echo "spark.sql.catalog.spark_catalog org.apache.spark.sql.delta.catalog.DeltaCatalog" >> ${SPARK_HOME}/conf/spark-defaults.conf

USER ${NB_UID}