# 📊 Sistema de Monitoramento com psutil + Dash

Este projeto tem como objetivo monitorar métricas de sistema em tempo real utilizando `psutil`, armazenar dados críticos em `SQLite` e exibir tudo em um painel moderno criado com `Dash`. O projeto é executado em um ambiente Docker e está em constante evolução.

## 🚀 Funcionalidades Atuais

- Coleta de métricas de sistema (CPU, RAM, Swap, Disco, Rede, etc) com [psutil](https://pypi.org/project/psutil/)
- Métricas comuns salvas em arquivos `.json` (sobrescritos a cada 1 segundo)
- Detecção de métricas críticas com **média móvel** (5 coletas) utilizando `collections.deque`
- Armazenamento de métricas críticas em banco de dados `SQLite` via [SQLAlchemy](https://www.sqlalchemy.org/)
- Dashboard web responsivo com [Dash (Plotly)](https://dash.plotly.com/)
- Execução assíncrona com `asyncio` para desempenho otimizado
- Docker container para fácil implantação


## 📦 Tecnologias Utilizadas

- Python 3.11+
- psutil
- Dash (Plotly)
- SQLAlchemy
- SQLite
- asyncio / deque
- Docker

## 🛠 Em Desenvolvimento

- 🔌 **API REST** para incluir múltiplos hosts no monitoramento
- 🖥️ **Melhoria visual** e usabilidade da interface do dashboard
- 📁 Organização de arquivos por hostname ou data
- 📤 Exportação de relatórios críticos (CSV ou PDF)

## 📄 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados

### Subir a aplicação:

```bash
docker-compose up --build
```

### Começar a monitorar:

```bash
na raiz do projeto:

python main.py
```
📬 Contribuição

Sinta-se à vontade para sugerir melhorias, abrir issues ou enviar pull requests.
---

## 👨‍💻 Autor

Desenvolvido por **Gabriel Lima** — Estudante de Engenharia de Software com foco em automação, monitoramento e back-end Python.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e contribuir!