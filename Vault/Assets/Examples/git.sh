#!/bin/bash

MESSAGE=${1}

git add .
git add *
git commit -m "${MESSAGE}"

git push -u origin master
