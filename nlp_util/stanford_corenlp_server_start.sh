#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-04-30 00:40:55
# desc:   Start Stanford CoreNLP Server

# set parameters to capture the necessary errors
set -ue
set -o pipefail

#set environment
stanford_corenlp_path="/Volumes/Documents/Projects/~stanford_nlp/stanford-corenlp-full-2016-10-31"
stanford_corenlp_models="/Volumes/Documents/Projects/~stanford_nlp/stanford-corenlp-models"

# set language
if [[ $# == 1 ]] && [[ $1 == "zh" ]]; then
    lang="-serverProperties StanfordCoreNLP-chinese.properties"
else
    lang=""
fi

# start server
java -mx4g -cp "${stanford_corenlp_path}/*:${stanford_corenlp_models}/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer ${lang} -port 9000 &
exit_code=$?

if [[ ${exit_code} == 0 ]]; then
    # wait until server starts
    while ! nc -z localhost 9000; do
        sleep 0.1 # wait for 1/10 of the second before check again
    done
fi