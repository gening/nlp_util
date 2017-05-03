#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-04-30 00:41:09
# desc:   Stop Stanford CoreNLP Server

# set parameters to capture the necessary errors
set -ue
set -o pipefail

# stop server
if [ -f "/tmp/corenlp.shutdown" ]; then
    wget "localhost:9000/shutdown?key=`cat /tmp/corenlp.shutdown`" -O -
else
    ps aux | grep StanfordCoreNLPServer | grep -v grep | awk '{print $2}' | xargs kill -9
    # macOS does not accept -r as parameter of xargs
fi
