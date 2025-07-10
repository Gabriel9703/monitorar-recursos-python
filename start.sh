#!/bin/bash

# Define o diretório raiz do projeto como PYTHONPATH
export PYTHONPATH=$(pwd)

# Roda o Streamlit a partir da raiz, apontando para o app dentro da pasta dashboard
streamlit run /app/dashboard/Home.py --server.port=8501 --server.address=0.0.0.0
