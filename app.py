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

# CSS customizado - ADICIONEI ESTILOS MELHORES PARA OS CARDS
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
        color: #1E1E1E;
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
    
    /* CARDS DO DASHBOARD MELHORADOS */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 1.8rem 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        color: #1E1E1E;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0A2647;
        line-height: 1.2;
        margin-bottom: 0.3rem;
    }
    .metric-label {
        color: #5A6A7E;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    .metric-small {
        color: #7F8C8D;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
    
    .countdown-urgent {
        color: #B71C1C;
        font-weight: bold;
        background-color: #FFCDD2;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        display: inline-block;
    }
    .countdown-warning {
        color: #F57C00;
        font-weight: bold;
        background-color: #FFE0B2;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        display: inline-block;
    }
    .countdown-normal {
        color: #2E7D32;
        font-weight: bold;
        background-color: #C8E6C9;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        display: inline-block;
    }
    .search-box {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #0A2647, transparent);
    }
</style>
""", unsafe_allow_html=True)

# Inicializa banco de dados
@st.cache_resource
def init_database():
    init_db()

init_database()
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
        ["📊 Dashboard", "📋 Kanban", "📅 Eventos", "📚 Knowledge Base", "🏢 Empresas Target", "👥 Senior Advisors"]
    )
    st.markdown("---")
    st.caption("Versão 2.0 - Raíssa Azevedo - 2026")

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
    return pd.read_sql_query("SELECT * FROM whitepapers ORDER BY created_at DESC", conn)

def get_cases():
    return pd.read_sql_query("SELECT * FROM knowledge_base WHERE type='case_study' ORDER BY created_at DESC", conn)

# FUNÇÃO DAYS_UNTIL CORRIGIDA (UMA ÚNICA VEZ)
def days_until(date_value):
    """Calcula dias até uma data de forma segura"""
    if pd.isna(date_value) or date_value is None:
        return None
    
    today = datetime.now().date()
    
    # Se for string, converter para date
    if isinstance(date_value, str):
        try:
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None
    # Se for Timestamp do pandas
    elif hasattr(date_value, 'date'):
        date_value = date_value.date()
    # Se já for date, manter
    
    if not isinstance(date_value, date):
        return None
        
    delta = date_value - today
    return delta.days

def format_countdown(days):
    """Formata contagem regressiva com cor"""
    if days is None:
        return ""
    if days < 0:
        return f"<span class='countdown-urgent'>⏰ Atrasado {abs(days)} dias</span>"
    elif days == 0:
        return "<span class='countdown-urgent'>🔥 Hoje!</span>"
    elif days <= 7:
        return f"<span class='countdown-urgent'>⚠️ {days} dias</span>"
    elif days <= 30:
        return f"<span class='countdown-warning'>📅 {days} dias</span>"
    else:
        return f"<span class='countdown-normal'>🗓️ {days} dias</span>"

# ================================
# DASHBOARD CORRIGIDO
# ================================
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Estratégico")

    # Carregar dados
    tasks = get_tasks()
    events = get_events()
    companies = get_companies()
    advisors = get_advisors()
    whitepapers = get_whitepapers()
    
    # Converter datas para datetime para comparação segura
    today = pd.Timestamp.now().normalize()
    
    # ===== MÉTRICAS PRINCIPAIS =====
    total_initiatives = len(tasks)
    completed = len(tasks[tasks['status'] == 'Done']) if not tasks.empty else 0
    in_progress = len(tasks[tasks['status'] == 'In Progress']) if not tasks.empty else 0
    todo = len(tasks[tasks['status'] == 'To Do']) if not tasks.empty else 0
    
    # ===== MÉTRICAS DE OPERAÇÕES =====
    total_events = len(events)
    total_companies = len(companies)
    total_advisors = len(advisors)
    total_whitepapers = len(whitepapers)
    
    # Calcular eventos futuros
    upcoming_events = 0
    if not events.empty and 'start_date' in events.columns:
        events['start_date_dt'] = pd.to_datetime(events['start_date'], errors='coerce')
        upcoming_events = len(events[events['start_date_dt'] >= today])
    
    # Primeira linha de métricas - INICIATIVAS
    st.markdown("### 📊 Visão Geral de Iniciativas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_initiatives}</div>
            <div class="metric-label">Total Iniciativas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        completion_rate = round(completed/total_initiatives*100 if total_initiatives>0 else 0, 1)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{completed}</div>
            <div class="metric-label">Concluídas</div>
            <div class="metric-small">{completion_rate}% do total</div>
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
    
    # Segunda linha de métricas - OPERAÇÕES
    st.markdown("### 🏭 Operações & Mercado")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_events}</div>
            <div class="metric-label">Eventos</div>
            <div class="metric-small">{upcoming_events} futuros</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_companies}</div>
            <div class="metric-label">Empresas Target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_advisors}</div>
            <div class="metric-label">Senior Advisors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_whitepapers}</div>
            <div class="metric-label">Whitepapers</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Gráficos e análises
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Progresso por Categoria")
        if not tasks.empty and 'category' in tasks.columns:
            cat_summary = tasks.groupby('category').size().reset_index(name='count')
            st.bar_chart(cat_summary.set_index('category'))
        else:
            st.info("Nenhuma iniciativa cadastrada.")
    
    with col2:
        st.subheader("🎯 Prioridades")
        if not tasks.empty and 'priority' in tasks.columns:
            priority_summary = tasks.groupby('priority').size().reset_index(name='count')
            st.bar_chart(priority_summary.set_index('priority'))
        else:
            st.info("Nenhuma iniciativa cadastrada.")
    
    # PRÓXIMOS EVENTOS - AGORA FUNCIONANDO CORRETAMENTE
    st.markdown("---")
    st.subheader("📅 Próximos Eventos")
    
    if not events.empty and 'start_date' in events.columns:
        # Garantir que a coluna de data está no formato correto
        events_display = events.copy()
        events_display['start_date_dt'] = pd.to_datetime(events_display['start_date'], errors='coerce')
        today_dt = pd.Timestamp.now().normalize()
        
        # Filtrar apenas eventos futuros ou de hoje
        upcoming = events_display[events_display['start_date_dt'] >= today_dt].sort_values('start_date_dt').head(5)
        
        if not upcoming.empty:
            for _, row in upcoming.iterrows():
                start_date_str = row['start_date'] if pd.notna(row['start_date']) else "Data não informada"
                days = days_until(row['start_date']) if pd.notna(row['start_date']) else None
                countdown_html = format_countdown(days) if days is not None else ""
                
                st.markdown(f"""
                <div class="card">
                    <h4>{row['name'] if 'name' in row else 'Evento sem nome'}</h4>
                    <p><strong>Data:</strong> {start_date_str} | {countdown_html}</p>
                    <p><strong>Local:</strong> {row.get('location', 'N/A')} {'(Virtual)' if row.get('is_virtual', False) else ''}</p>
                    <p><strong>Descrição:</strong> {row.get('description', 'Sem descrição')[:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎉 Nenhum evento futuro agendado. Que tal adicionar um na seção de Eventos?")
    else:
        st.info("📆 Nenhum evento cadastrado. Vá para a seção 'Eventos' e adicione alguns!")
        
        # Botão rápido para ir para eventos
        if st.button("➕ Adicionar Evento Agora"):
            st.switch_page("app.py?menu=📅 Eventos")  # Isso vai mudar para a página de eventos
            
# ================================
# KANBAN
# ================================
elif menu == "📋 Kanban":
    st.header("📋 Kanban - Iniciativas")

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
                    VALUES (%s, %s, %s, %s, %s, 'To Do', %s, %s, %s, %s)
                """, (title, description, category, subcategory, priority, owner_name, due_date, target_companies, document_link))
                conn.commit()
                st.success("Iniciativa criada!")
                st.rerun()

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
                days = days_until(row['due_date']) if row['due_date'] else None
                countdown_html = format_countdown(days) if days is not None else ""
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><span class="{priority_class}">{row['priority']}</span> | {row['category']} | {row['subcategory']}</p>
                    <p><strong>Resp:</strong> {row['owner_name'] or 'N/A'} | <strong>Data:</strong> {row['due_date'] or 'N/A'} {countdown_html}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("→ Iniciar", key=f"start_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("UPDATE tasks SET status='In Progress' WHERE id=%s", (row['id'],))
                    conn.commit()
                    st.rerun()
        with col2:
            st.markdown("### 🔄 In Progress")
            ip_tasks = tasks[tasks['status'] == 'In Progress']
            for _, row in ip_tasks.iterrows():
                priority_class = "priority-high" if row['priority'] == 'Alta' else "priority-medium" if row['priority'] == 'Média' else "priority-low"
                days = days_until(row['due_date']) if row['due_date'] else None
                countdown_html = format_countdown(days) if days is not None else ""
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><span class="{priority_class}">{row['priority']}</span> | {row['category']} | {row['subcategory']}</p>
                    <p><strong>Resp:</strong> {row['owner_name'] or 'N/A'} | <strong>Data:</strong> {row['due_date'] or 'N/A'} {countdown_html}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("✅ Concluir", key=f"done_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("UPDATE tasks SET status='Done', completed_date=%s WHERE id=%s", (date.today(), row['id']))
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
# EVENTOS - CORRIGIDO E REINSERIDO
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
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, description, event_type, industry, start_date, end_date, location, is_virtual))
                conn.commit()
                st.success("Evento adicionado!")
                st.rerun()

    # Filtros
    with st.expander("🔍 Filtrar Eventos"):
        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.multiselect("Tipo", ["conference", "webinar", "workshop", "networking", "forum"])
            filter_industry = st.multiselect("Indústria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "geral"])
        with col2:
            show_past = st.checkbox("Mostrar eventos passados", value=False)
            show_virtual = st.checkbox("Mostrar apenas virtuais", value=False)

    events = get_events()
    
    # Aplicar filtros de forma segura
    if not events.empty:
        events_filtered = events.copy()
        
        if 'start_date' in events_filtered.columns:
            events_filtered['start_date_dt'] = pd.to_datetime(events_filtered['start_date'], errors='coerce')
            today = pd.Timestamp.now().normalize()
            
            if not show_past:
                events_filtered = events_filtered[events_filtered['start_date_dt'] >= today]
        
        if show_virtual and 'is_virtual' in events_filtered.columns:
            events_filtered = events_filtered[events_filtered['is_virtual'] == True]
        
        if filter_type and 'event_type' in events_filtered.columns:
            events_filtered = events_filtered[events_filtered['event_type'].isin(filter_type)]
        
        if filter_industry and 'industry' in events_filtered.columns:
            events_filtered = events_filtered[events_filtered['industry'].isin(filter_industry)]
    else:
        events_filtered = events

    if events_filtered.empty:
        st.info("Nenhum evento encontrado com os filtros selecionados.")
    else:
        for _, row in events_filtered.iterrows():
            days = days_until(row['start_date']) if pd.notna(row['start_date']) else None
            countdown_html = format_countdown(days) if days is not None else ""
            
            st.markdown(f"""
            <div class="card">
                <h4>{row['name']}</h4>
                <p><strong>Tipo:</strong> {row['event_type']} | <strong>Indústria:</strong> {row['industry']}</p>
                <p><strong>Data:</strong> {row['start_date']} a {row['end_date']} | {countdown_html}</p>
                <p><strong>Local:</strong> {row['location'] or 'N/A'} {'(Virtual)' if row['is_virtual'] else ''}</p>
                <p>{row['description']}</p>
            </div>
            """, unsafe_allow_html=True)

# ================================
# KNOWLEDGE BASE
# ================================
elif menu == "📚 Knowledge Base":
    st.header("📚 Knowledge Base")

    tab1, tab2, tab3 = st.tabs(["📄 Whitepapers", "📖 Glossário", "📊 Case Studies"])

    with tab1:
        st.subheader("Whitepapers")
        
        with st.expander("🔍 Buscar Whitepapers", expanded=False):
            search_term = st.text_input("Pesquisar por título, tópico ou autor", key="search_wp")
        
        with st.expander("➕ Novo Whitepaper", expanded=False):
            with st.form("new_wp"):
                title = st.text_input("Título *")
                topic = st.text_input("Tópico")
                author = st.text_input("Autor")
                status = st.selectbox("Status", ["draft", "review", "published"])
                document_link = st.text_input("Link")
                content = st.text_area("Conteúdo (resumo)")
                if st.form_submit_button("Salvar") and title:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO whitepapers (title, topic, author_name, status, document_link, content) VALUES (%s, %s, %s, %s, %s, %s)",
                                (title, topic, author, status, document_link, content))
                    conn.commit()
                    st.success("Whitepaper adicionado!")
                    st.rerun()
        
        wps = get_whitepapers()
        if not wps.empty:
            if search_term:
                wps = wps[
                    wps['title'].str.contains(search_term, case=False, na=False) |
                    wps['topic'].str.contains(search_term, case=False, na=False) |
                    wps['author_name'].str.contains(search_term, case=False, na=False)
                ]
            
            st.write(f"**{len(wps)} whitepapers encontrados**")
            for _, row in wps.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><strong>Tópico:</strong> {row['topic']} | <strong>Autor:</strong> {row['author_name']} | <strong>Status:</strong> {row['status']}</p>
                    <p>{row['content'][:200]}...</p>
                    <p><a href="{row['document_link']}" target="_blank">🔗 Link para documento</a></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum whitepaper cadastrado.")

    with tab2:
        st.subheader("Glossário")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Pesquisar termo ou definição", key="search_glossary")
        with col2:
            filter_category = st.selectbox("Categoria", ["Todos", "technical", "business", "acronym"])
        
        with st.expander("➕ Novo Termo", expanded=False):
            with st.form("new_term"):
                term = st.text_input("Termo *")
                definition = st.text_area("Definição *")
                category = st.selectbox("Categoria", ["technical", "business", "acronym"])
                example = st.text_input("Exemplo")
                if st.form_submit_button("Salvar") and term and definition:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO glossary (term, definition, category, example) VALUES (%s, %s, %s, %s)",
                                (term, definition, category, example))
                    conn.commit()
                    st.success("Termo adicionado!")
                    st.rerun()
        
        glossary = get_glossary()
        if not glossary.empty:
            if search_term:
                glossary = glossary[
                    glossary['term'].str.contains(search_term, case=False, na=False) |
                    glossary['definition'].str.contains(search_term, case=False, na=False)
                ]
            if filter_category != "Todos":
                glossary = glossary[glossary['category'] == filter_category]
            
            st.write(f"**{len(glossary)} termos encontrados**")
            for _, row in glossary.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>{row['term']}</h4>
                    <p><em>{row['definition']}</em></p>
                    <p><strong>Categoria:</strong> {row['category']} | <strong>Exemplo:</strong> {row['example'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum termo cadastrado no glossário.")

    with tab3:
        st.subheader("Case Studies")
        
        with st.expander("🔍 Buscar Cases", expanded=False):
            search_case = st.text_input("Pesquisar por título ou descrição", key="search_case")
        
        with st.expander("➕ Novo Case Study", expanded=False):
            with st.form("new_case"):
                title = st.text_input("Título do Case *")
                category = st.selectbox("Categoria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands"])
                summary = st.text_area("Resumo *")
                content = st.text_area("Conteúdo completo")
                author = st.text_input("Autor")
                document_link = st.text_input("Link para documento")
                tags = st.text_input("Tags (separadas por vírgula)")
                
                if st.form_submit_button("Salvar") and title and summary:
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO knowledge_base (title, type, category, summary, content, author, tags, document_link, is_published)
                        VALUES (%s, 'case_study', %s, %s, %s, %s, %s, %s, TRUE)
                    """, (title, category, summary, content, author, tags, document_link))
                    conn.commit()
                    st.success("Case study adicionado!")
                    st.rerun()
        
        cases = get_cases()
        
        if cases.empty:
            st.info("Nenhum case study cadastrado. Use o formulário acima para adicionar o primeiro case!")
            
            with st.expander("📋 Ver exemplo de Case Study"):
                st.markdown("""
                **Título:** Otimização de Supply Chain com IA na Indústria ABC
                
                **Categoria:** supply_chain
                
                **Resumo:** Implementação de sistema de previsão de demanda usando machine learning reduziu estoques em 30% e aumentou disponibilidade de produtos.
                
                **Resultados:** Redução de custos, aumento de eficiência.
                """)
        else:
            if search_case:
                cases = cases[
                    cases['title'].str.contains(search_case, case=False, na=False) |
                    cases['summary'].str.contains(search_case, case=False, na=False) |
                    cases['tags'].str.contains(search_case, case=False, na=False)
                ]
            
            st.write(f"**{len(cases)} cases encontrados**")
            for _, row in cases.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <p><strong>Categoria:</strong> {row['category']} | <strong>Autor:</strong> {row['author'] or 'N/A'}</p>
                    <p><strong>Resumo:</strong> {row['summary']}</p>
                    <p><strong>Tags:</strong> {row['tags'] or 'N/A'}</p>
                    {f'<p><a href="{row["document_link"]}" target="_blank">🔗 Link para documento</a></p>' if row['document_link'] else ''}
                </div>
                """, unsafe_allow_html=True)

# ================================
# EMPRESAS TARGET
# ================================
elif menu == "🏢 Empresas Target":
    st.header("🏢 Empresas Target")

    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Buscar por nome, indústria ou contato", key="search_companies")
    with col2:
        filter_status = st.selectbox("Status", ["Todos", "prospect", "contacted", "meeting", "proposal", "closed"])

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
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, industry, size, status, contact_person, contact_email, contact_phone, potential_value, notes))
                conn.commit()
                st.success("Empresa adicionada!")
                st.rerun()

    companies = get_companies()
    if companies.empty:
        st.info("Nenhuma empresa target cadastrada.")
    else:
        if search_term:
            companies = companies[
                companies['name'].str.contains(search_term, case=False, na=False) |
                companies['industry'].str.contains(search_term, case=False, na=False) |
                companies['contact_person'].str.contains(search_term, case=False, na=False)
            ]
        if filter_status != "Todos":
            companies = companies[companies['status'] == filter_status]
        
        st.write(f"**{len(companies)} empresas encontradas**")
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

    search_term = st.text_input("🔍 Buscar por nome, expertise, empresa ou tópicos", key="search_advisors")

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
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, expertise, company, topics, events, linkedin, notes))
                conn.commit()
                st.success("Advisor adicionado!")
                st.rerun()

    advisors = get_advisors()
    if advisors.empty:
        st.info("Nenhum advisor cadastrado.")
    else:
        if search_term:
            advisors = advisors[
                advisors['name'].str.contains(search_term, case=False, na=False) |
                advisors['expertise'].str.contains(search_term, case=False, na=False) |
                advisors['company'].str.contains(search_term, case=False, na=False) |
                advisors['topics'].str.contains(search_term, case=False, na=False)
            ]
        
        st.write(f"**{len(advisors)} advisors encontrados**")
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
st.caption("TaskSync - Operações | Desenvolvido com Streamlit | Raíssa Azevedo - 2026")