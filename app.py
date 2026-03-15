import streamlit as st
from database import get_connection, init_db
import pandas as pd
from datetime import datetime, date

# Configuração da página
st.set_page_config(
    page_title="TaskSync - Operations",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para garantir legibilidade
st.markdown("""
<style>
    /* Cores seguras para texto */
    .main-header {
        background: linear-gradient(135deg, #0A2647, #2C5F8A);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1E1E1E;  /* texto escuro */
    }
    .card h4, .card p {
        color: #1E1E1E;
    }
    .priority-high {
        color: #B71C1C;
        font-weight: bold;
    }
    .priority-medium {
        color: #F57C00;
        font-weight: bold;
    }
    .priority-low {
        color: #2E7D32;
        font-weight: bold;
    }
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
        background-color: #E0E0E0;
        color: #1E1E1E;
    }
    .status-todo { background-color: #BBDEFB; color: #0D47A1; }
    .status-progress { background-color: #FFF9C4; color: #F57F17; }
    .status-done { background-color: #C8E6C9; color: #1B5E20; }
    .stButton>button {
        background-color: #0A2647;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.4rem 1rem;
    }
    .stButton>button:hover {
        background-color: #2C5F8A;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1E1E1E;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0A2647;
    }
    .metric-label {
        color: #555;
        font-size: 0.9rem;
        text-transform: uppercase;
    }
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #0A2647, transparent);
    }
</style>
""", unsafe_allow_html=True)

# Inicializa banco de dados
init_db()
conn = get_connection()

# Cabeçalho
st.markdown("""
<div class="main-header">
    <h1>🎯 TaskSync - Operations Strategy</h1>
    <p>Gestão de desafios, próximos passos, ferramentas e conhecimento em operações</p>
</div>
""", unsafe_allow_html=True)

# Sidebar de navegação
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/0A2647/FFFFFF?text=TaskSync", use_column_width=True)
    menu = st.radio(
        "Navegação",
        ["📊 Dashboard", "📋 Kanban", "📅 Eventos", "📚 Knowledge Base", "🎯 Desafios & Próximos Passos", "🏢 Empresas Target", "👥 Senior Advisors"]
    )
    st.markdown("---")
    st.caption("Versão 2.0 - Pronto para PostgreSQL")

# Funções auxiliares para obter dados
def get_tasks():
    return pd.read_sql_query("SELECT * FROM tasks ORDER BY priority DESC, due_date", conn)

def get_events():
    return pd.read_sql_query("SELECT * FROM events ORDER BY start_date", conn)

def get_companies():
    return pd.read_sql_query("SELECT * FROM target_companies", conn)

def get_advisors():
    return pd.read_sql_query("SELECT * FROM senior_advisors", conn)

def get_glossary():
    return pd.read_sql_query("SELECT * FROM glossary ORDER BY term", conn)

def get_whitepapers():
    return pd.read_sql_query("SELECT * FROM whitepapers", conn)

# ================================
# DASHBOARD
# ================================
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Estratégico")

    # Métricas principais
    tasks = get_tasks()
    total_initiatives = len(tasks)
    completed = len(tasks[tasks['status'] == 'Done'])
    in_progress = len(tasks[tasks['status'] == 'In Progress'])
    todo = len(tasks[tasks['status'] == 'To Do'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_initiatives}</div>
            <div class="metric-label">Total Iniciativas</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{completed}</div>
            <div class="metric-label">Concluídas</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{in_progress}</div>
            <div class="metric-label">Em Andamento</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{todo}</div>
            <div class="metric-label">A Fazer</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 Progresso por Categoria")
    if not tasks.empty:
        cat_summary = tasks.groupby('category').size().reset_index(name='count')
        st.bar_chart(cat_summary.set_index('category'))
    else:
        st.info("Nenhuma iniciativa cadastrada.")

# ================================
# KANBAN
# ================================
elif menu == "📋 Kanban":
    st.header("📋 Kanban - Iniciativas")

    # Formulário para adicionar nova tarefa
    with st.expander("➕ Nova Iniciativa"):
        with st.form("new_task"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Título *")
                category = st.selectbox("Categoria", ["challenge", "next_step", "tool", "whitepaper", "initiative"])
                subcategory = st.selectbox("Subcategoria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "outros"])
                priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
            with col2:
                owner_name = st.text_input("Responsável")
                due_date = st.date_input("Data limite", value=None)
                target_companies = st.text_input("Empresas alvo (separadas por vírgula)")
                document_link = st.text_input("Link documento")

            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Salvar")
            if submitted and title:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO tasks (title, description, category, subcategory, priority, status, owner_name, due_date, target_companies, document_link)
                    VALUES (?, ?, ?, ?, ?, 'To Do', ?, ?, ?, ?)
                """, (title, description, category, subcategory, priority, owner_name, due_date, target_companies, document_link))
                conn.commit()
                st.success("Iniciativa criada!")
                st.rerun()

    # Exibir Kanban
    tasks = get_tasks()
    if tasks.empty:
        st.info("Nenhuma tarefa cadastrada.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 📝 To Do")
            todo_tasks = tasks[tasks['status'] == 'To Do']
            for _, row in todo_tasks.iterrows():
                priority_class = "priority-high" if row['priority'] == 'Alta' else "priority-medium" if row['priority'] == 'Média' else "priority-low"
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><span class="{priority_class}">{row['priority']}</span> | {row['category']} | {row['subcategory']}</p>
                    <p><strong>Resp:</strong> {row['owner_name'] or 'N/A'} | <strong>Data:</strong> {row['due_date'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("→ Iniciar", key=f"start_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("UPDATE tasks SET status='In Progress' WHERE id=?", (row['id'],))
                    conn.commit()
                    st.rerun()
        with col2:
            st.markdown("### 🔄 In Progress")
            ip_tasks = tasks[tasks['status'] == 'In Progress']
            for _, row in ip_tasks.iterrows():
                priority_class = "priority-high" if row['priority'] == 'Alta' else "priority-medium" if row['priority'] == 'Média' else "priority-low"
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><span class="{priority_class}">{row['priority']}</span> | {row['category']} | {row['subcategory']}</p>
                    <p><strong>Resp:</strong> {row['owner_name'] or 'N/A'} | <strong>Data:</strong> {row['due_date'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("✅ Concluir", key=f"done_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("UPDATE tasks SET status='Done', completed_date=? WHERE id=?", (date.today(), row['id']))
                    conn.commit()
                    st.rerun()
        with col3:
            st.markdown("### ✅ Done")
            done_tasks = tasks[tasks['status'] == 'Done']
            for _, row in done_tasks.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>✓ {row['title']}</h4>
                    <p>Concluído em: {row['completed_date'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)

# ================================
# EVENTOS
# ================================
elif menu == "📅 Eventos":
    st.header("📅 Eventos do Setor")

    with st.expander("➕ Novo Evento"):
        with st.form("new_event"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nome do evento *")
                event_type = st.selectbox("Tipo", ["conference", "webinar", "workshop", "networking", "forum"])
                industry = st.selectbox("Indústria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "geral"])
            with col2:
                start_date = st.date_input("Data início")
                end_date = st.date_input("Data fim")
                location = st.text_input("Local")
                is_virtual = st.checkbox("Evento virtual")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Salvar")
            if submitted and name:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO events (name, description, event_type, industry, start_date, end_date, location, is_virtual)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, description, event_type, industry, start_date, end_date, location, is_virtual))
                conn.commit()
                st.success("Evento adicionado!")
                st.rerun()

    events = get_events()
    if events.empty:
        st.info("Nenhum evento cadastrado.")
    else:
        for _, row in events.iterrows():
            st.markdown(f"""
            <div class="card">
                <h4>{row['name']}</h4>
                <p><strong>Tipo:</strong> {row['event_type']} | <strong>Indústria:</strong> {row['industry']}</p>
                <p><strong>Data:</strong> {row['start_date']} a {row['end_date']} | <strong>Local:</strong> {row['location'] or 'N/A'} {'(Virtual)' if row['is_virtual'] else ''}</p>
                <p>{row['description']}</p>
            </div>
            """, unsafe_allow_html=True)

# ================================
# KNOWLEDGE BASE
# ================================
elif menu == "📚 Knowledge Base":
    st.header("📚 Knowledge Base")

    tab1, tab2, tab3 = st.tabs(["📄 Whitepapers", "📖 Glossário", "📊 Cases"])

    with tab1:
        st.subheader("Whitepapers")
        with st.expander("➕ Novo Whitepaper"):
            with st.form("new_wp"):
                title = st.text_input("Título *")
                topic = st.text_input("Tópico")
                author = st.text_input("Autor")
                status = st.selectbox("Status", ["draft", "review", "published"])
                document_link = st.text_input("Link")
                content = st.text_area("Conteúdo (resumo)")
                if st.form_submit_button("Salvar") and title:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO whitepapers (title, topic, author_name, status, document_link, content) VALUES (?, ?, ?, ?, ?, ?)",
                                (title, topic, author, status, document_link, content))
                    conn.commit()
                    st.success("Whitepaper adicionado!")
                    st.rerun()
        wps = get_whitepapers()
        if not wps.empty:
            for _, row in wps.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><strong>Tópico:</strong> {row['topic']} | <strong>Autor:</strong> {row['author_name']} | <strong>Status:</strong> {row['status']}</p>
                    <p>{row['content'][:200]}...</p>
                    <p><a href="{row['document_link']}" target="_blank">Link</a></p>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Glossário")
        with st.expander("➕ Novo Termo"):
            with st.form("new_term"):
                term = st.text_input("Termo *")
                definition = st.text_area("Definição *")
                category = st.selectbox("Categoria", ["technical", "business", "acronym"])
                example = st.text_input("Exemplo")
                if st.form_submit_button("Salvar") and term and definition:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO glossary (term, definition, category, example) VALUES (?, ?, ?, ?)",
                                (term, definition, category, example))
                    conn.commit()
                    st.success("Termo adicionado!")
                    st.rerun()
        glossary = get_glossary()
        if not glossary.empty:
            for _, row in glossary.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>{row['term']}</h4>
                    <p><em>{row['definition']}</em></p>
                    <p><strong>Categoria:</strong> {row['category']} | <strong>Exemplo:</strong> {row['example'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.subheader("Case Studies")
        st.info("Funcionalidade em desenvolvimento. Em breve você poderá adicionar cases.")

# ================================
# DESAFIOS & PRÓXIMOS PASSOS
# ================================
elif menu == "🎯 Desafios & Próximos Passos":
    st.header("🎯 Desafios e Próximos Passos")

    # Filtro por tipo
    tipo = st.radio("Mostrar:", ["Desafios", "Próximos Passos", "Ferramentas"], horizontal=True)
    cat_map = {"Desafios": "challenge", "Próximos Passos": "next_step", "Ferramentas": "tool"}
    cat = cat_map[tipo]

    tasks = get_tasks()
    filtered = tasks[tasks['category'] == cat]

    if filtered.empty:
        st.info(f"Nenhum {tipo.lower()} cadastrado.")
    else:
        for _, row in filtered.iterrows():
            priority_class = "priority-high" if row['priority'] == 'Alta' else "priority-medium" if row['priority'] == 'Média' else "priority-low"
            st.markdown(f"""
            <div class="card">
                <h4>{row['title']}</h4>
                <p><span class="{priority_class}">{row['priority']}</span> | {row['subcategory']} | Resp: {row['owner_name'] or 'N/A'}</p>
                <p>{row['description']}</p>
                <p><strong>Data limite:</strong> {row['due_date'] or 'N/A'}</p>
            </div>
            """, unsafe_allow_html=True)

# ================================
# EMPRESAS TARGET
# ================================
elif menu == "🏢 Empresas Target":
    st.header("🏢 Empresas Target")

    with st.expander("➕ Nova Empresa"):
        with st.form("new_company"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nome da empresa *")
                industry = st.selectbox("Indústria", ["manufacturing", "healthcare", "b2b", "brands", "supply_chain", "tech"])
                size = st.selectbox("Porte", ["small", "medium", "large"])
                status = st.selectbox("Status", ["prospect", "contacted", "meeting", "proposal", "closed"])
            with col2:
                contact_person = st.text_input("Contato")
                contact_email = st.text_input("Email")
                contact_phone = st.text_input("Telefone")
                potential_value = st.text_input("Valor potencial")
            notes = st.text_area("Observações")
            submitted = st.form_submit_button("Salvar")
            if submitted and name:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO target_companies (name, industry, size, status, contact_person, contact_email, contact_phone, potential_value, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, industry, size, status, contact_person, contact_email, contact_phone, potential_value, notes))
                conn.commit()
                st.success("Empresa adicionada!")
                st.rerun()

    companies = get_companies()
    if companies.empty:
        st.info("Nenhuma empresa target cadastrada.")
    else:
        for _, row in companies.iterrows():
            st.markdown(f"""
            <div class="card">
                <h4>{row['name']}</h4>
                <p><strong>Indústria:</strong> {row['industry']} | <strong>Porte:</strong> {row['size']} | <strong>Status:</strong> {row['status']}</p>
                <p><strong>Contato:</strong> {row['contact_person'] or 'N/A'} | {row['contact_email'] or 'N/A'} | {row['contact_phone'] or 'N/A'}</p>
                <p><strong>Valor potencial:</strong> {row['potential_value'] or 'N/A'}</p>
                <p><em>{row['notes']}</em></p>
            </div>
            """, unsafe_allow_html=True)

# ================================
# SENIOR ADVISORS
# ================================
elif menu == "👥 Senior Advisors":
    st.header("👥 Senior Advisors")

    with st.expander("➕ Novo Advisor"):
        with st.form("new_advisor"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nome *")
                expertise = st.text_input("Expertise")
                company = st.text_input("Empresa")
            with col2:
                topics = st.text_input("Tópicos (separados por vírgula)")
                events = st.text_input("Eventos que participa")
                linkedin = st.text_input("LinkedIn")
            notes = st.text_area("Notas")
            if st.form_submit_button("Salvar") and name:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO senior_advisors (name, expertise, company, topics, events_participated, linkedin, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, expertise, company, topics, events, linkedin, notes))
                conn.commit()
                st.success("Advisor adicionado!")
                st.rerun()

    advisors = get_advisors()
    if advisors.empty:
        st.info("Nenhum advisor cadastrado.")
    else:
        for _, row in advisors.iterrows():
            st.markdown(f"""
            <div class="card">
                <h4>{row['name']}</h4>
                <p><strong>Expertise:</strong> {row['expertise']} | <strong>Empresa:</strong> {row['company'] or 'N/A'}</p>
                <p><strong>Tópicos:</strong> {row['topics'] or 'N/A'}</p>
                <p><strong>Eventos:</strong> {row['events_participated'] or 'N/A'}</p>
                <p><strong>LinkedIn:</strong> <a href="{row['linkedin']}" target="_blank">{row['linkedin']}</a></p>
                <p><em>{row['notes']}</em></p>
            </div>
            """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.caption("TaskSync - Operações | Desenvolvido com Streamlit | Pronto para deploy com PostgreSQL")