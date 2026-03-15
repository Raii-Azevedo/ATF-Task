import os
import psycopg2
from psycopg2 import pool
import streamlit as st

# Connection pool for better performance
_connection_pool = None

def get_connection_pool():
    """Get or create a connection pool (singleton pattern)"""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,  # minconn
            10,  # maxconn
            os.environ["DATABASE_URL"]
        )
    return _connection_pool

def get_connection():
    """Get a connection from the pool"""
    pool = get_connection_pool()
    return pool.getconn()

def return_connection(conn):
    """Return a connection to the pool"""
    pool = get_connection_pool()
    pool.putconn(conn)


def init_db():
    """Cria as tabelas e insere dados iniciais se necessário."""
    conn = get_connection()
    cur = conn.cursor()

    # ========== CRIAÇÃO DAS TABELAS ==========

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE,
        role VARCHAR(50) DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Projects
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        area VARCHAR(100) NOT NULL,
        owner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status VARCHAR(50) DEFAULT 'active',
        priority VARCHAR(50) DEFAULT 'Média',
        start_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tasks (iniciativas, desafios, próximos passos, etc.)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100) NOT NULL,
        subcategory VARCHAR(100),
        status VARCHAR(50) DEFAULT 'To Do',
        priority VARCHAR(50) DEFAULT 'Média',
        progress INTEGER DEFAULT 0,
        owner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        owner_name VARCHAR(255),
        created_date DATE DEFAULT CURRENT_DATE,
        due_date DATE,
        start_date DATE,
        completed_date DATE,
        estimated_hours REAL,
        actual_hours REAL,
        related_initiative VARCHAR(255),
        document_link TEXT,
        notion_link TEXT,
        tags TEXT,
        notes TEXT,
        target_companies TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Whitepapers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS whitepapers (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        topic VARCHAR(255),
        status VARCHAR(50) DEFAULT 'draft',
        progress INTEGER DEFAULT 0,
        author_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        author_name VARCHAR(255),
        content TEXT,
        document_link TEXT,
        published_date DATE,
        target_audience TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Events
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        event_type VARCHAR(100),
        industry VARCHAR(100),
        start_date DATE,
        end_date DATE,
        location VARCHAR(255),
        is_virtual BOOLEAN DEFAULT FALSE,
        event_link TEXT,
        participants TEXT,
        notes TEXT,
        status VARCHAR(50) DEFAULT 'upcoming',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Senior Advisors
    cur.execute("""
    CREATE TABLE IF NOT EXISTS senior_advisors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        expertise TEXT,
        topics TEXT,
        events_participated TEXT,
        company VARCHAR(255),
        contact_info TEXT,
        linkedin TEXT,
        notes TEXT,
        status VARCHAR(50) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Target Companies
    cur.execute("""
    CREATE TABLE IF NOT EXISTS target_companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        industry VARCHAR(100),
        size VARCHAR(50),
        contact_person VARCHAR(255),
        contact_email VARCHAR(255),
        contact_phone VARCHAR(50),
        potential_value VARCHAR(255),
        notes TEXT,
        status VARCHAR(50) DEFAULT 'prospect',
        last_contact DATE,
        next_action TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Knowledge Base
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_base (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        type VARCHAR(100),
        category VARCHAR(100),
        content TEXT,
        summary TEXT,
        author VARCHAR(255),
        tags TEXT,
        document_link TEXT,
        is_published BOOLEAN DEFAULT FALSE,
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Glossary
    cur.execute("""
    CREATE TABLE IF NOT EXISTS glossary (
        id SERIAL PRIMARY KEY,
        term VARCHAR(255) UNIQUE NOT NULL,
        definition TEXT NOT NULL,
        category VARCHAR(100),
        related_terms TEXT,
        example TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ========== ÍNDICES PARA PERFORMANCE ==========
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_events_start_date ON events(start_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_target_companies_status ON target_companies(status)")

    conn.commit()

    # ========== DADOS INICIAIS ==========
    # Verificar se já existem dados para não duplicar

    # Glossário
    cur.execute("SELECT COUNT(*) FROM glossary")
    if cur.fetchone()['count'] == 0:
        glossary_terms = [
            ('Digital Twin', 'Réplica virtual de processos, produtos ou serviços', 'technical', 'Simulação, Gêmeo Digital', 'Usado para otimizar processos de manufatura'),
            ('Manufacturing', 'Processo de transformação de matérias-primas em produtos acabados', 'business', 'Produção, Indústria', 'Indústria 4.0 na manufacturing'),
            ('Supply Chain', 'Rede entre empresa e fornecedores para produção e distribuição', 'business', 'Logística, Cadeia de suprimentos', 'Otimização da supply chain com IA'),
            ('Machine Learning', 'Subcampo da IA que permite aprendizado a partir de dados', 'technical', 'IA, Deep Learning', 'ML para controle de qualidade'),
            ('Computer Vision', 'Campo da IA que treina computadores para interpretar o mundo visual', 'technical', 'Visão computacional, IA', 'Inspeção visual automatizada'),
            ('Industry 4.0', 'Quarta revolução industrial com automação e troca de dados', 'business', 'Indústria, Automação', 'Implementação de indústria 4.0'),
            ('Predictive Maintenance', 'Manutenção preditiva usando análise de dados', 'technical', 'Manutenção, IA', 'Redução de downtime com manutenção preditiva'),
            ('B2B', 'Business to Business - negócios entre empresas', 'business', 'Business', 'Estratégias B2B para manufacturing'),
            ('Healthcare', 'Setor de saúde e cuidados médicos', 'business', 'Saúde, Medical', 'Inovação em healthcare operations'),
            ('Brands', 'Empresas de bens de consumo e marcas', 'business', 'Consumo, Varejo', 'Supply chain para marcas globais')
        ]
        cur.executemany(
            "INSERT INTO glossary (term, definition, category, related_terms, example) VALUES (%s, %s, %s, %s, %s)",
            glossary_terms
        )

    # Target Companies
    cur.execute("SELECT COUNT(*) FROM target_companies")
    if cur.fetchone()['count'] == 0:
        companies = [
            ('Indústrias ABC', 'manufacturing', 'large', 'João Silva', 'joao@abc.com', '11 99999-9999', 'Alto', 'Empresa líder em manufatura', 'prospect', '2024-01-15', 'Agendar reunião'),
            ('SaúdeTech', 'healthcare', 'medium', 'Maria Santos', 'maria@saudetech.com', '11 88888-8888', 'Médio', 'Startup de saúde digital', 'contacted', '2024-01-10', 'Enviar proposta'),
            ('Global Brands', 'brands', 'large', 'Pedro Oliveira', 'pedro@global.com', '11 77777-7777', 'Alto', 'Multinacional de bens de consumo', 'meeting', '2024-01-20', 'Preparar apresentação')
        ]
        cur.executemany(
            """INSERT INTO target_companies 
               (name, industry, size, contact_person, contact_email, contact_phone, potential_value, notes, status, last_contact, next_action) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            companies
        )

    # Events
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()['count'] == 0:
        events = [
            ('Industry 4.0 Summit', 'Conferência sobre indústria 4.0 e inovação', 'conference', 'manufacturing', '2024-03-15', '2024-03-17', 'São Paulo', False, 'www.industry40summit.com', 'Empresas: ABC, XYZ', 'Evento principal do setor', 'upcoming'),
            ('Supply Chain Tech', 'Workshop de tecnologia em supply chain', 'workshop', 'supply_chain', '2024-02-10', '2024-02-10', 'Online', True, 'www.supplychaintech.com', 'Palestrantes internacionais', 'Inscrições abertas', 'upcoming'),
            ('Digital Twin Forum', 'Fórum sobre gêmeos digitais', 'forum', 'digital_twin', '2024-04-05', '2024-04-06', 'Rio de Janeiro', False, 'www.digitaltwinforum.com', 'Networking com especialistas', 'Agendar participação', 'upcoming')
        ]
        cur.executemany(
            """INSERT INTO events 
               (name, description, event_type, industry, start_date, end_date, location, is_virtual, event_link, participants, notes, status) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            events
        )

    # Senior Advisors
    cur.execute("SELECT COUNT(*) FROM senior_advisors")
    if cur.fetchone()['count'] == 0:
        advisors = [
            ('Dr. Carlos Silva', 'Digital Twin, Indústria 4.0', 'Implementação, Estratégia, Tecnologia', 'Web Summit, Tech Forum', 'Consultor Independente', 'carlos.silva@email.com', 'linkedin.com/in/carlossilva', 'Especialista em transformação digital'),
            ('Ana Souza', 'Supply Chain, Logística', 'Otimização, IA em Logística', 'Supply Chain Conference, LogTech', 'LogConsult', 'ana.souza@email.com', 'linkedin.com/in/anasouza', 'Ex-diretora de logística de grande empresa'),
            ('Prof. Roberto Santos', 'IA, Machine Learning', 'Visão Computacional, Controle de Qualidade', 'AI Summit, Tech Conference', 'Universidade de São Paulo', 'roberto@usp.br', 'linkedin.com/in/robertosantos', 'Pesquisador renomado em IA aplicada')
        ]
        cur.executemany(
            """INSERT INTO senior_advisors 
               (name, expertise, topics, events_participated, company, contact_info, linkedin, notes) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            advisors
        )

    # Tasks (iniciativas de exemplo)
    cur.execute("SELECT COUNT(*) FROM tasks")
    if cur.fetchone()['count'] == 0:
        initiatives = [
            # (title, description, category, subcategory, status, priority, progress, owner_id, owner_name, created_date, due_date, notes, related_initiative, document_link, notion_link, target_companies)
            ('Fortalecer conexão com Manufacturing', 'Grande potencial de geração de valor em áreas de Manufacturing', 'challenge', 'manufacturing', 'To Do', 'Alta', 0, 1, 'João', '2024-01-01', '2024-03-31', 'Iniciativa estratégica', 'initiative_001', '/docs/manufacturing', 'notion.link/123', 'Indústrias ABC, XYZ'),
            ('Replicar estrutura de Finanças para Operations', 'Adaptar modelo de sucesso de Finanças', 'next_step', 'operations', 'In Progress', 'Alta', 30, 2, 'Maria', '2024-01-15', '2024-02-28', 'Prioridade Q1', 'initiative_002', '/docs/operations', 'notion.link/456', ''),
            ('Criar Glossário Operations', 'Consolidar terminologias e conceitos de OP', 'tool', 'knowledge', 'In Progress', 'Média', 60, 3, 'Pedro', '2024-01-10', '2024-02-15', 'Base para novos membros', 'initiative_003', '/docs/glossary', 'notion.link/789', ''),
            ('Whitepaper sobre Digital Twin', 'Documentar aplicações e cases de Digital Twin', 'whitepaper', 'digital_twin', 'In Progress', 'Alta', 45, 1, 'João', '2024-01-05', '2024-03-30', 'Pesquisa com especialistas', 'whitepaper_dt', '/whitepapers/dt', 'notion.link/dt', ''),
            ('Mapear eventos de Supply Chain', 'Identificar principais eventos do setor', 'initiative', 'supply_chain', 'To Do', 'Baixa', 0, 4, 'Ana', '2024-02-01', '2024-03-01', 'Lista de eventos 2024', 'events_001', '/docs/events', 'notion.link/events', '')
        ]
        for init in initiatives:
            cur.execute("""
                INSERT INTO tasks (
                    title, description, category, subcategory, status, priority, 
                    progress, owner_id, owner_name, created_date, due_date, notes,
                    related_initiative, document_link, notion_link, target_companies
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, init)

    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")

def migrate_database():
    """Função para futuras migrações (a ser chamada quando necessário)."""
    # Aqui você pode adicionar ALTER TABLE etc. usando comandos SQL.
    # Como estamos usando CREATE TABLE IF NOT EXISTS, não precisamos de migração inicial.
    pass

if __name__ == "__main__":
    init_db()