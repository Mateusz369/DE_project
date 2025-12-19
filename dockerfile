FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        tar \
        openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

RUN curl https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz --output hadoop-3.3.6.tar.gz && \
    tar -xvf hadoop-3.3.6.tar.gz && \
    rm hadoop-3.3.6.tar.gz

ENV HADOOP_HOME=/hadoop-3.3.6
ENV PATH="$HADOOP_HOME/bin:$PATH"

CMD ["bash"]