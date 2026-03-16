# 🎯 TaskSync - Operations Strategy Platform

![TaskSync Banner](https://github.com/Raii-Azevedo/ATF-Task/blob/main/logo.png)

Plataforma completa para gestão de operações, desafios estratégicos, próximos passos e knowledge base, desenvolvida com Streamlit e PostgreSQL.

---

## 📋 Sobre o Projeto

O **TaskSync Operations** é uma ferramenta de gestão estratégica desenvolvida para times de operações que precisam:

- 📊 Gerenciar iniciativas e desafios
- ⏰ Acompanhar próximos passos e prazos
- 📚 Manter uma base de conhecimento organizada
- 📅 Mapear eventos do setor
- 🤝 Gerenciar relacionamento com empresas target e senior advisors

---

## ✨ Funcionalidades

### 📊 Dashboard Estratégico
- Visão geral de todas as iniciativas
- Métricas de conclusão e progresso
- Gráficos por categoria e prioridade
- Próximos eventos em destaque
- Contagem regressiva para prazos

### 📋 Kanban de Iniciativas
- Gestão visual de tarefas (To Do, In Progress, Done)
- Prioridades (Alta, Média, Baixa)
- Categorias: challenges, next_steps, tools, whitepapers
- Datas limite com alertas visuais
- CRUD completo (criar, editar, excluir)

### 📅 Eventos do Setor
- Cadastro de eventos com datas
- Filtros por tipo, indústria e status
- Contagem regressiva automática
- Destaque para eventos próximos

### 📚 Knowledge Base
- **Whitepapers**: Gestão de documentos técnicos
- **Glossário**: Termos e definições do setor
- **Case Studies**: Exemplos práticos e resultados

### 🏢 Empresas Target
- Pipeline de relacionamento com empresas
- Status: prospect, contacted, meeting, proposal, closed
- Informações de contato e valor potencial

### 👥 Senior Advisors
- Mapeamento de influenciadores do setor
- Expertise, tópicos e eventos
- Links para LinkedIn

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Streamlit | 1.28+ | Framework web |
| Python | 3.9+ | Linguagem principal |
| PostgreSQL | 14+ | Banco de dados (produção) |
| SQLite | 3.x | Banco de dados (desenvolvimento) |
| Pandas | 2.0+ | Manipulação de dados |
| psycopg2-binary | 2.9+ | Driver PostgreSQL |
| SQLAlchemy | 2.0+ | ORM (opcional) |
| python-dotenv | 1.0+ | Variáveis de ambiente |

---

## 📦 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes)
- Git

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/tasksync-operations.git
   cd tasksync-operations
Crie um ambiente virtual

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instale as dependências

bash
pip install -r requirements.txt
Configure as variáveis de ambiente

Crie um arquivo .env na raiz do projeto:

env
# Para PostgreSQL (produção)
DATABASE_URL=postgresql://usuario:senha@localhost:5432/tasksync_db

# Para SQLite (desenvolvimento)
# DATABASE_URL=sqlite:///db.sqlite
Inicialize o banco de dados

bash
python database.py
Execute a aplicação

bash
streamlit run app.py
Acesse no navegador

text
http://localhost:8501
📁 Estrutura do Projeto
text
tasksync-operations/
├── app.py                 # Aplicação principal (frontend + lógica)
├── database.py            # Configuração do banco de dados
├── requirements.txt       # Dependências do projeto
├── .env                   # Variáveis de ambiente (não versionar)
├── .gitignore             # Arquivos ignorados pelo git
├── README.md              # Documentação
└── db.sqlite              # Banco SQLite (gerado automaticamente)
📄 Arquivo requirements.txt
txt
streamlit==1.28.0
pandas==2.0.3
psycopg2-binary==2.9.7
python-dotenv==1.0.0
sqlalchemy==2.0.19
🔧 Configuração do Banco de Dados
SQLite (Desenvolvimento)
python
# database.py
DATABASE_URL = "sqlite:///db.sqlite"
PostgreSQL (Produção)
python
# database.py
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/tasksync")
🚀 Deploy no Railway
Passo 1: Prepare o repositório
bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seu-usuario/tasksync-operations.git
git push -u origin main
Passo 2: Configure no Railway
Acesse railway.app

Clique em "New Project" → "Deploy from GitHub"

Selecione seu repositório

Adicione um banco PostgreSQL

O Railway configurará automaticamente a variável DATABASE_URL

Passo 3: Deploy automático
A cada push no repositório, o Railway faz deploy automático.

🎨 Design System
Cores
Primária: #0A2647 (azul escuro - confiança)

Secundária: #2C5F8A (azul médio - tecnologia)

Sucesso: #2E7D32 (verde - concluído)

Atenção: #F57C00 (laranja - médio)

Urgente: #B71C1C (vermelho - alta prioridade)

Cards
Fundo branco com borda suave

Sombra sutil

Efeito hover

Bordas arredondadas (8px)

Tipografia
Fonte: Inter (sans-serif)

Títulos: negrito

Texto: regular

📱 Responsividade
O app se adapta automaticamente a diferentes tamanhos de tela:

Desktop (> 1200px): Layout em múltiplas colunas

Tablet (768px - 1199px): Colunas ajustadas

Mobile (< 768px): Layout em coluna única

🔒 Segurança
✅ Variáveis de ambiente para dados sensíveis

✅ Prepared statements contra SQL injection

✅ Session state para controle de edição

✅ Validação de dados nos formulários

✅ Sanitização de inputs

🤝 Como Contribuir
Fork o projeto

Crie uma branch (git checkout -b feature/nova-funcionalidade)

Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request

🐛 Reportando Bugs
Encontrou um bug? Abra uma issue com:

Descrição do problema

Passos para reproduzir

Comportamento esperado

Screenshots (se aplicável)

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

text
MIT License

Copyright (c) 2026 Raíssa Azevedo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
✨ Autora
Raíssa Azevedo

Desenvolvimento Full Stack

Arquitetura de Software

UX/UI Design

🙏 Agradecimentos
Streamlit - Framework incrível

Railway - Hospedagem simplificada

PostgreSQL - Banco de dados robusto

Comunidade open source pelas bibliotecas

📊 Roadmap
Versão 2.0 (Atual) ✅
Dashboard estratégico

Kanban completo

Gestão de eventos

Knowledge Base

CRUD em todas as seções

Buscadores

Contagem regressiva

Versão 2.1 (Próxima) 🚧
Autenticação de usuários

Relatórios exportáveis (PDF/Excel)

Notificações por email

Integração com Google Calendar

API REST

Versão 3.0 (Futuro) 🎯
App mobile (React Native)

IA para recomendações

Chat integrado

Analytics avançado

📞 Contato
Email: raissa.azevedo@email.com

LinkedIn: linkedin.com/in/raissa-azevedo

GitHub: github.com/raissa-azevedo

⚡ Quick Start (1 minuto)
bash
# Clone e execute em segundos
git clone https://github.com/seu-usuario/tasksync-operations.git
cd tasksync-operations
pip install -r requirements.txt
streamlit run app.py
<div align="center"> <br> <img src="https://github.com/Raii-Azevedo/ATF-Task/blob/main/logo.png" alt="TaskSync Logo"> <br> <br> <p><strong>Versão 2.0</strong> - Março 2026</p> <p>Desenvolvido com ❤️ para gestão estratégica de operações</p> <br> <p> <a href="#-sobre-o-projeto">Sobre</a> • <a href="#-funcionalidades">Funcionalidades</a> • <a href="#-instalação">Instalação</a> • <a href="#-deploy-no-railway">Deploy</a> • <a href="#-licença">Licença</a> </p> <br> </div> ```