#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-04-30 00:40:55
# desc:   Start Stanford CoreNLP Server

# set parameters to capture the necessary errors
set -ue
set -o pipefail

#set environment
stanford_corenlp_path=$1
stanford_corenlp_model_path=$2
lang=$3

# set language
if [[ ${lang} == "zh" ]]; then
    lang_param="-serverProperties StanfordCoreNLP-chinese.properties"
else
    lang_param=""
fi

# start server
java -mx4g -cp "${stanford_corenlp_path}/*:${stanford_corenlp_model_path}/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer ${lang_param} -port 9000 &
exit_code=$?

if [[ ${exit_code} == 0 ]]; then
    # wait until server starts
    while ! nc -z localhost 9000; do
        sleep 0.1 # wait for 1/10 of the second before check again
    done
fi