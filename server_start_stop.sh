#!/usr/bin/env bash

# Start Hadoop
$HADOOP_HOME/sbin/start-dfs.sh

# Start Zookeeper
$ZOOKEEPER_HOME/bin/zookeeper-server-start.sh $ZOOKEEPER_HOME/config/zookeeper.properties

# Start Hbase
$HBASE_HOME/bin/start-hbase.sh

# Start Thrift server
$HBASE_HOME/bin/hbase-daemon.sh start thrift

# Start Kafka
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties