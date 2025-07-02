#!/bin/bash

# Define o diretório raiz do projeto como PYTHONPATH
export PYTHONPATH=$(pwd)

# Roda o Streamlit a partir da raiz, apontando para o app dentro da pasta dashboard
streamlit run dashboard/Home.py
