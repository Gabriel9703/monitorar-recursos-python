# 🖥️ Sistema de Monitoramento de Recursos com Python, psutil e MySQL

Este projeto monitora os principais recursos do sistema — CPU, RAM, Disco e Rede — em tempo real, utilizando `psutil`, e registra automaticamente **logs críticos** em um banco de dados MySQL, executado via Docker.

---

## 📋 Funcionalidades

- ✅ Monitoramento contínuo da **CPU**
- ✅ Monitoramento da **memória RAM**
- ✅ Monitoramento da **Rede (envios, recebimentos, erros, pacotes)**
- ✅ Salvamento automático dos logs **críticos** no MySQL
- ✅ Estrutura modular com classes bem definidas
- ✅ Uso de `logging` estruturado com timestamps
- ✅ Pronto para ser expandido com métricas de disco e processos
- ✅ Threads paralelas para execução simultânea dos monitores

---


## ⚙️ Pré-requisitos

- Python 3.10+
- Docker + Docker Compose
- `psutil`, `mysql-connector-python`

Instale os pacotes Python:

```bash
pip install -r requirements.txt
```

---

## 🐳 Subindo o Banco de Dados com Docker

Antes de executar os monitores, suba o banco MySQL com:

```bash
docker-compose up --build
```

Isso irá:

- Criar o container do MySQL
- Executar o script `init.sql` com as tabelas de `cpu_logs`, `ram_logs`, `network_logs`

---

## 🚀 Executando o Monitoramento

Depois que o container do MySQL estiver de pé, execute:

```bash
python main.py
```

> O sistema começará a monitorar a CPU, RAM, SWAP e Rede. Logs críticos (acima de 80% de uso, erros ou drops) serão salvos no banco de dados automaticamente.

---

## 🧪 Testando anomalias

Para simular situações críticas e testar o sistema, use o utilitário `stress` (no Linux):

```bash
sudo apt install stress

# Estressar a CPU
stress --cpu 4 --timeout 10

# Estressar a RAM
stress --vm 2 --vm-bytes 2G --timeout 10
```

---

## 🛠️ Extensível para:

- Processos: usando `psutil.process_iter()`
- Streamlit ou Dash para exibir dashboards em tempo real



---

## 👨‍💻 Autor

Desenvolvido por **Gabriel Lima** — Estudante de Engenharia de Software com foco em automação, monitoramento e back-end Python.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e contribuir!