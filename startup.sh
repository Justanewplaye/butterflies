#!/bin/bash
if [ ! -d .git ]; then
    git init
    git remote add origin https://github.com/Justanewplaye/butterflies.git
    git fetch origin
    git checkout -b master origin/master
fi
git pull origin master
pip install --prefix .local -r requirements.txt
python main.py
