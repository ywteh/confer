#!/bin/sh
abspath=$(cd "$(dirname "$0")"; pwd)
rm -rf $abspath/bin
mkdir $abspath/bin
CLASSPATH=$CLASSPATH:$abspath/lib/*:$abspath/bin
javac -classpath $CLASSPATH -d $abspath/bin $abspath/src/edu/mit/csail/confer/Indexer.java
target=$abspath/../../data/$1
index=$abspath/../../index/$1
echo $target
rm -rf $index
mkdir $index
export CLASSPATH
java -classpath $CLASSPATH edu.mit.csail.confer.Indexer $target/papers.json $target/offline_recs.json $index
echo "offline_recs=" | cat - $target/offline_recs.json > $target/../../server/static/conf/$1/data/offline_recs.json