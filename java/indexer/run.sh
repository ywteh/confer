#!/bin/sh
abspath=$(cd "$(dirname "$0")"; pwd)
CLASSPATH=$CLASSPATH:$abspath/"lib/*":$abspath/"bin"
export CLASSPATH
java -classpath $CLASSPATH edu.mit.csail.confer.Indexer $abspath/../../data/sigmod2013/papers.json $abspath/../../index $abspath/../../data/sigmod2013/similar_papers.json