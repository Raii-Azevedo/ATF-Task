import os
import psycopg2


# ==============================
# CONNECTION
# ==============================

def get_connection():
    """Create a new database connection"""
    return psycopg2.connect(os.environ["DATABASE_URL"])


# ==============================
# DATABASE INITIALIZATION
# ==============================

def init_db():
    """Create tables and initial data (without tasks)."""

    conn = get_connection()
    cur = conn.cursor()

    # USERS
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

    # PROJECTS
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

    # TASKS
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

    # WHITEPAPERS - ADICIONADA COLUNA TAGS
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
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # EVENTS
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

    # SENIOR ADVISORS
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

    # TARGET COMPANIES
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

    # KNOWLEDGE BASE
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

    # GLOSSARY
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

    # ==============================
    # INDEXES
    # ==============================

    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_events_start_date ON events(start_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_target_companies_status ON target_companies(status)")

    conn.commit()

    # ==============================
    # MIGRATIONS PARA TABELAS EXISTENTES
    # ==============================
    
    # Adicionar coluna tags na tabela whitepapers se não existir
    try:
        cur.execute("ALTER TABLE whitepapers ADD COLUMN IF NOT EXISTS tags TEXT")
        conn.commit()
        print("✅ Coluna 'tags' adicionada à tabela whitepapers")
    except Exception as e:
        print(f"⚠️ Coluna 'tags' já existe ou erro: {e}")
    
    # Adicionar coluna description na tabela whitepapers se não existir
    try:
        cur.execute("ALTER TABLE whitepapers ADD COLUMN IF NOT EXISTS description TEXT")
        conn.commit()
        print("✅ Coluna 'description' adicionada à tabela whitepapers")
    except Exception as e:
        print(f"⚠️ Coluna 'description' já existe ou erro: {e}")

    # ==============================
    # INITIAL DATA
    # ==============================

    # GLOSSARY
    cur.execute("SELECT COUNT(*) FROM glossary")
    if cur.fetchone()[0] == 0:

        glossary_terms = [
            ('Digital Twin', 'Réplica virtual de processos ou produtos', 'technical', 'Simulação', 'Usado em manufatura'),
            ('Manufacturing', 'Processo de produção industrial', 'business', 'Produção', 'Indústria 4.0'),
            ('Supply Chain', 'Rede logística de produção e distribuição', 'business', 'Logística', 'IA na cadeia de suprimentos'),
            ('Machine Learning', 'IA que aprende com dados', 'technical', 'IA', 'Controle de qualidade'),
            ('Computer Vision', 'IA para interpretar imagens', 'technical', 'IA', 'Inspeção visual automática')
        ]

        cur.executemany(
            "INSERT INTO glossary (term, definition, category, related_terms, example) VALUES (%s,%s,%s,%s,%s)",
            glossary_terms
        )

    # TARGET COMPANIES
    cur.execute("SELECT COUNT(*) FROM target_companies")
    if cur.fetchone()[0] == 0:

        companies = [
            ('Indústrias ABC', 'manufacturing', 'large', 'João Silva', 'joao@abc.com', '11 99999-9999', 'Alto', 'Empresa líder', 'prospect', '2024-01-15', 'Agendar reunião'),
            ('SaúdeTech', 'healthcare', 'medium', 'Maria Santos', 'maria@saudetech.com', '11 88888-8888', 'Médio', 'Startup saúde', 'contacted', '2024-01-10', 'Enviar proposta')
        ]

        cur.executemany("""
        INSERT INTO target_companies
        (name,industry,size,contact_person,contact_email,contact_phone,potential_value,notes,status,last_contact,next_action)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, companies)

    # EVENTS
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()[0] == 0:

        events = [
            ('Industry 4.0 Summit', 'Conferência indústria 4.0', 'conference', 'manufacturing', '2024-03-15', '2024-03-17', 'São Paulo', False, 'www.industry40summit.com', '', '', 'upcoming'),
            ('Supply Chain Tech', 'Workshop supply chain', 'workshop', 'supply_chain', '2024-02-10', '2024-02-10', 'Online', True, 'www.supplychaintech.com', '', '', 'upcoming')
        ]

        cur.executemany("""
        INSERT INTO events
        (name,description,event_type,industry,start_date,end_date,location,is_virtual,event_link,participants,notes,status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, events)

    conn.commit()

    cur.close()
    conn.close()

    print("✅ Database initialized successfully")


# ==============================
# MIGRATIONS
# ==============================

def migrate_database():
    """Future migrations"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Adicionar coluna tags na tabela whitepapers se não existir
    try:
        cur.execute("ALTER TABLE whitepapers ADD COLUMN IF NOT EXISTS tags TEXT")
        conn.commit()
        print("✅ Migração: coluna 'tags' adicionada")
    except Exception as e:
        print(f"⚠️ Migração tags: {e}")
    
    # Adicionar coluna description na tabela whitepapers se não existir
    try:
        cur.execute("ALTER TABLE whitepapers ADD COLUMN IF NOT EXISTS description TEXT")
        conn.commit()
        print("✅ Migração: coluna 'description' adicionada")
    except Exception as e:
        print(f"⚠️ Migração description: {e}")
    
    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()
    migrate_database()