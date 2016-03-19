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


################# REDIS GENERATION ########################################3
links.sort(key=lambda x: x.url, reverse=True)
keys duplicate-filter:1457926628

== Remove all
EVAL "return redis.call('del', unpack(redis.call('keys', ARGV[1])))" 0 duplicate*
EVAL "return redis.call('del', unpack(redis.call('keys', ARGV[1])))" 0 product:*
EVAL "return redis.call('del', unpack(redis.call('keys', ARGV[1])))" 0 product:tiki.vn:http://*

l=re.findall('(http:\/\/.+)',response.body)
l=re.findall('(https:\/\/.+)',response.body)

celery -A product_spiders worker -P eventlet -c 10
celery flower -A product_spiders --broker=redis://localhost:6379// --basic_auth=mongooselabs:mongoose@Prod --address=127.0.0.1 --port=6666

