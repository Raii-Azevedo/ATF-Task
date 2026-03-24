import streamlit as st
from database import get_connection, init_db
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import io
import calendar
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json
import hashlib

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TaskSync - Operations Strategy",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SESSION STATE INITIALIZATION =====
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "dark_mode": False,
        "notifications": [],
        "saved_filters": {},
        "comments": {},
        "user_name": "Usuário",
        "user_email": None,
        "user_role": "viewer"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ===== DATABASE INITIALIZATION =====
@st.cache_resource
def init_database():
    init_db()

init_database()
conn = get_connection()

# ===== ENHANCED STYLES =====
def get_enhanced_styles(dark_mode=False):
    """Get enhanced CSS styles with glassmorphism and modern effects"""
    if dark_mode:
        return """
        <style>
        /* Dark Mode Base */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        
        /* Modern Cards */
        .card-modern {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.18);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .card-modern:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 35px rgba(0,0,0,0.3);
            border-color: rgba(255,255,255,0.3);
        }
        .card-modern::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5, #00d2ff);
        }
        
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            color: #a0a0a0;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-trend-up { color: #00ff88; }
        .metric-trend-down { color: #ff4444; }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin: 0 0.25rem;
        }
        .badge-urgent { background: #ff4444; color: white; }
        .badge-high { background: #ff6b6b; color: white; }
        .badge-medium { background: #ffb347; color: white; }
        .badge-low { background: #4ecdc4; color: white; }
        .badge-todo { background: #3498db; color: white; }
        .badge-progress { background: #f39c12; color: white; }
        .badge-done { background: #2ecc71; color: white; }
        
        /* Tags */
        .tag {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-right: 0.5rem;
            background: rgba(255,255,255,0.1);
            color: #e0e0e0;
        }
        
        /* Countdown */
        .countdown-urgent {
            background: rgba(255,68,68,0.2);
            color: #ff8888;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-weight: bold;
        }
        .countdown-warning {
            background: rgba(255,180,71,0.2);
            color: #ffb347;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
        }
        .countdown-normal {
            background: rgba(46,204,113,0.2);
            color: #2ecc71;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
        }
        
        /* Search Box */
        .search-box {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Progress Bar */
        .progress-bar {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        /* Timeline */
        .timeline-item {
            border-left: 2px solid #00d2ff;
            padding-left: 1rem;
            margin: 1rem 0;
            position: relative;
        }
        .timeline-dot {
            position: absolute;
            left: -0.5rem;
            top: 0;
            width: 0.8rem;
            height: 0.8rem;
            border-radius: 50%;
            background: #00d2ff;
        }
        
        /* Text Colors */
        h1, h2, h3, h4, p, span, label, .stMarkdown {
            color: #e0e0e0;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,210,255,0.3);
        }
        
        hr {
            border-color: rgba(255,255,255,0.1);
        }
        </style>
        """
    else:
        return """
        <style>
        /* Light Mode Base */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8edf5 100%);
        }
        
        /* Modern Cards */
        .card-modern {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 1px solid #e5e7eb;
            position: relative;
            overflow: hidden;
        }
        .card-modern:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.12);
        }
        .card-modern::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #0A2647, #2C5F8A, #4A9FD8);
        }
        
        /* Metric Cards */
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border: 1px solid #e5e7eb;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0A2647;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            color: #6b7280;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-trend-up { color: #10b981; }
        .metric-trend-down { color: #ef4444; }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin: 0 0.25rem;
        }
        .badge-urgent { background: #ef4444; color: white; }
        .badge-high { background: #f97316; color: white; }
        .badge-medium { background: #eab308; color: white; }
        .badge-low { background: #10b981; color: white; }
        .badge-todo { background: #3b82f6; color: white; }
        .badge-progress { background: #f59e0b; color: white; }
        .badge-done { background: #22c55e; color: white; }
        
        /* Tags */
        .tag {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-right: 0.5rem;
            background: #f3f4f6;
            color: #374151;
        }
        
        /* Countdown */
        .countdown-urgent {
            background: #fee2e2;
            color: #dc2626;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-weight: bold;
        }
        .countdown-warning {
            background: #fed7aa;
            color: #ea580c;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
        }
        .countdown-normal {
            background: #d1fae5;
            color: #059669;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
        }
        
        /* Search Box */
        .search-box {
            background: #f9fafb;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid #e5e7eb;
        }
        
        /* Progress Bar */
        .progress-bar {
            background: #e5e7eb;
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, #0A2647, #2C5F8A);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        /* Timeline */
        .timeline-item {
            border-left: 2px solid #0A2647;
            padding-left: 1rem;
            margin: 1rem 0;
            position: relative;
        }
        .timeline-dot {
            position: absolute;
            left: -0.5rem;
            top: 0;
            width: 0.8rem;
            height: 0.8rem;
            border-radius: 50%;
            background: #0A2647;
        }
        
        h1, h2, h3, h4, p, span, label {
            color: #1f2937;
        }
        </style>
        """

# Apply enhanced styles
st.markdown(get_enhanced_styles(st.session_state.dark_mode), unsafe_allow_html=True)

# ===== NOTIFICATION SYSTEM =====
def add_notification(message, type="info"):
    """Add notification to session state"""
    st.session_state.notifications.append({
        "message": message,
        "type": type,
        "timestamp": datetime.now()
    })

def show_notifications():
    """Display all notifications"""
    for notif in st.session_state.notifications[-5:]:
        if notif["type"] == "success":
            st.success(notif["message"])
        elif notif["type"] == "error":
            st.error(notif["message"])
        elif notif["type"] == "warning":
            st.warning(notif["message"])
        else:
            st.info(notif["message"])
    st.session_state.notifications = []

# ===== HELPER FUNCTIONS =====
def days_until(date_value):
    """Calcula dias até uma data de forma segura"""
    if pd.isna(date_value) or date_value is None:
        return None
    
    today = datetime.now().date()
    
    if isinstance(date_value, str):
        try:
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None
    elif hasattr(date_value, 'date'):
        date_value = date_value.date()
    
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
    elif days <= 3:
        return f"<span class='countdown-urgent'>⚠️ {days} dias</span>"
    elif days <= 7:
        return f"<span class='countdown-warning'>📅 {days} dias</span>"
    else:
        return f"<span class='countdown-normal'>🗓️ {days} dias</span>"

def render_tag(tag):
    """Renderiza tag colorida"""
    tag_colors = {
        "urgente": "#FF6B6B",
        "prioritario": "#FFB347",
        "planejamento": "#4ECDC4",
        "execução": "#45B7D1",
        "revisão": "#96CEB4",
        "manufacturing": "#FF6B6B",
        "supply_chain": "#4ECDC4",
        "digital_twin": "#45B7D1",
        "ia_ml": "#96CEB4",
        "healthcare": "#FFB347"
    }
    
    color = tag_colors.get(tag.lower(), "#95A5A6")
    return f'<span style="background-color: {color}; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px;">{tag}</span>'

def get_priority_badge(priority):
    """Retorna badge de prioridade"""
    badges = {
        "Alta": "badge-high",
        "Média": "badge-medium",
        "Baixa": "badge-low"
    }
    return f'<span class="badge {badges.get(priority, "badge-medium")}">{priority}</span>'

def get_status_badge(status):
    """Retorna badge de status"""
    badges = {
        "To Do": "badge-todo",
        "In Progress": "badge-progress",
        "Done": "badge-done"
    }
    return f'<span class="badge {badges.get(status, "badge-todo")}">{status}</span>'

def calculate_productivity(tasks_df):
    """Calcula métricas de produtividade"""
    if tasks_df.empty:
        return 0
    
    total = len(tasks_df)
    completed = len(tasks_df[tasks_df['status'] == 'Done'])
    return (completed / total * 100) if total > 0 else 0

def check_deadlines():
    """Verifica prazos próximos e adiciona notificações"""
    tasks = get_tasks()
    today = date.today()
    
    for _, task in tasks.iterrows():
        if task['due_date'] and task['status'] != 'Done':
            days_left = (task['due_date'] - today).days
            if days_left <= 3 and days_left >= 0:
                add_notification(f"⚠️ Tarefa '{task['title']}' vence em {days_left} dias!", "warning")
            elif days_left < 0:
                add_notification(f"❌ Tarefa '{task['title']}' está atrasada!", "error")

def get_realtime_metrics():
    """Calcula métricas em tempo real"""
    tasks = get_tasks()
    
    if tasks.empty:
        return {
            "total": 0,
            "completed": 0,
            "in_progress": 0,
            "todo": 0,
            "on_track": 0,
            "delayed": 0,
            "productivity_rate": 0
        }
    
    today = date.today()
    total = len(tasks)
    completed = len(tasks[tasks['status'] == 'Done'])
    in_progress = len(tasks[tasks['status'] == 'In Progress'])
    todo = len(tasks[tasks['status'] == 'To Do'])
    
    delayed = len(tasks[
        (tasks['due_date'] < today) & 
        (tasks['status'] != 'Done')
    ]) if 'due_date' in tasks.columns else 0
    
    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "todo": todo,
        "on_track": total - delayed,
        "delayed": delayed,
        "productivity_rate": (completed / total * 100) if total > 0 else 0
    }

def export_to_excel(data, filename):
    """Exporta dados para Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name='Relatório', index=False)
    
    return st.download_button(
        label="📥 Exportar para Excel",
        data=output.getvalue(),
        file_name=f"{filename}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def export_to_pdf(data, title):
    """Exporta dados para PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))
    
    if not data.empty:
        table_data = [data.columns.tolist()] + data.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    
    return st.download_button(
        label="📥 Exportar para PDF",
        data=buffer,
        file_name=f"{title}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )

def global_search(search_term):
    """Busca global em todas as tabelas"""
    results = {}
    
    # Buscar em tarefas
    tasks = get_tasks()
    if not tasks.empty:
        tasks_result = tasks[
            tasks['title'].str.contains(search_term, case=False, na=False) |
            tasks['description'].str.contains(search_term, case=False, na=False)
        ]
        if not tasks_result.empty:
            results["Tarefas"] = tasks_result
    
    # Buscar em eventos
    events = get_events()
    if not events.empty:
        events_result = events[
            events['name'].str.contains(search_term, case=False, na=False) |
            events['description'].str.contains(search_term, case=False, na=False)
        ]
        if not events_result.empty:
            results["Eventos"] = events_result
    
    # Buscar em empresas
    companies = get_companies()
    if not companies.empty:
        companies_result = companies[
            companies['name'].str.contains(search_term, case=False, na=False) |
            companies['contact_person'].str.contains(search_term, case=False, na=False)
        ]
        if not companies_result.empty:
            results["Empresas"] = companies_result
    
    # Buscar em advisors
    advisors = get_advisors()
    if not advisors.empty:
        advisors_result = advisors[
            advisors['name'].str.contains(search_term, case=False, na=False) |
            advisors['expertise'].str.contains(search_term, case=False, na=False)
        ]
        if not advisors_result.empty:
            results["Advisors"] = advisors_result
    
    return results

def save_filter(filter_name, filters):
    """Salva filtro personalizado"""
    st.session_state.saved_filters[filter_name] = filters
    add_notification(f"✅ Filtro '{filter_name}' salvo!", "success")

def load_filter(filter_name):
    """Carrega filtro salvo"""
    return st.session_state.saved_filters.get(filter_name, {})

# ===== DATA FUNCTIONS =====
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

# ===== VISUALIZATION FUNCTIONS =====
def show_progress_charts(tasks_df):
    """Mostra gráficos de progresso interativos"""
    if tasks_df.empty:
        st.info("Nenhuma tarefa para exibir nos gráficos")
        return
    
    # Gráfico de pizza por status
    status_counts = tasks_df['status'].value_counts()
    fig_pie = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Distribuição por Status",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Gráfico de barras por categoria
    if 'category' in tasks_df.columns:
        category_counts = tasks_df['category'].value_counts()
        fig_bar = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            title="Iniciativas por Categoria",
            color=category_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(
            xaxis_title="Categoria",
            yaxis_title="Quantidade",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            st.plotly_chart(fig_bar, use_container_width=True)

def show_timeline(tasks_df):
    """Cria uma linha do tempo visual dos projetos"""
    if tasks_df.empty or 'due_date' not in tasks_df.columns:
        st.info("Dados insuficientes para criar timeline")
        return
    
    # Preparar dados para timeline
    timeline_data = tasks_df[tasks_df['due_date'].notna()].copy()
    if timeline_data.empty:
        st.info("Nenhuma data definida para timeline")
        return
    
    timeline_data['start'] = pd.to_datetime(timeline_data['created_at'] if 'created_at' in timeline_data.columns else datetime.now())
    timeline_data['end'] = pd.to_datetime(timeline_data['due_date'])
    
    fig = px.timeline(
        timeline_data,
        x_start="start",
        x_end="end",
        y="title",
        color="priority",
        title="Linha do Tempo de Projetos",
        color_discrete_map={
            "Alta": "#ff6b6b",
            "Média": "#ffb347",
            "Baixa": "#4ecdc4"
        }
    )
    
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Projeto",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_upcoming_deadlines():
    """Mostra prazos próximos"""
    tasks = get_tasks()
    today = date.today()
    
    # Filtrar tarefas não concluídas com data
    upcoming = tasks[
        (tasks['status'] != 'Done') & 
        (tasks['due_date'].notna())
    ].copy()
    
    if upcoming.empty:
        st.info("🎉 Nenhum prazo próximo!")
        return
    
    # Calcular dias restantes
    upcoming['days_left'] = upcoming['due_date'].apply(
        lambda x: (x - today).days if pd.notna(x) else None
    )
    
    # Ordenar por dias restantes
    upcoming = upcoming.sort_values('days_left').head(10)
    
    for _, task in upcoming.iterrows():
        days = task['days_left']
        if days <= 0:
            st.error(f"❌ **{task['title']}** - Atrasado!")
        elif days <= 3:
            st.warning(f"⚠️ **{task['title']}** - Vence em {days} dias")
        else:
            st.info(f"📅 **{task['title']}** - Vence em {days} dias")

def show_recent_activity():
    """Mostra atividade recente"""
    tasks = get_tasks()
    
    if tasks.empty:
        st.info("Nenhuma atividade recente")
        return
    
    # Últimas tarefas concluídas
    completed_recent = tasks[
        (tasks['status'] == 'Done') & 
        (tasks['completed_date'].notna())
    ].sort_values('completed_date', ascending=False).head(5)
    
    if not completed_recent.empty:
        st.markdown("#### ✅ Recentemente Concluídas")
        for _, task in completed_recent.iterrows():
            st.markdown(f"- {task['title']} (concluída em {task['completed_date']})")
    
    # Tarefas em andamento mais antigas
    in_progress_old = tasks[
        (tasks['status'] == 'In Progress') & 
        (tasks['start_date'].notna())
    ].sort_values('start_date').head(5)
    
    if not in_progress_old.empty:
        st.markdown("#### 🔄 Em Andamento (mais antigas)")
        for _, task in in_progress_old.iterrows():
            days = (date.today() - task['start_date']).days if pd.notna(task['start_date']) else 0
            st.markdown(f"- {task['title']} (em andamento há {days} dias)")

def show_calendar_view(events_df):
    """Mostra eventos em formato de calendário"""
    if events_df.empty:
        st.info("Nenhum evento para exibir")
        return
    
    today = datetime.now().date()
    
    # Criar grid do mês atual
    cal = calendar.monthcalendar(today.year, today.month)
    
    # Destacar dias com eventos
    events_df['start_date_dt'] = pd.to_datetime(events_df['start_date'], errors='coerce')
    event_days = set()
    for _, event in events_df.iterrows():
        if pd.notna(event['start_date_dt']):
            event_days.add(event['start_date_dt'].day)
    
    # Criar tabela do calendário
    st.markdown(f"### 📅 {today.strftime('%B %Y')}")
    
    # Cabeçalho
    cols = st.columns(7)
    for i, day in enumerate(['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']):
        with cols[i]:
            st.markdown(f"**{day}**")
    
    # Dias do mês
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                elif day in event_days:
                    st.markdown(f"<div style='background: #ffb347; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{day}</div>", unsafe_allow_html=True)
                elif day == today.day:
                    st.markdown(f"<div style='background: #0A2647; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{day}</div>", unsafe_allow_html=True)
                else:
                    st.write(day)

# ===== MAIN APP =====
# Sidebar
with st.sidebar:
    st.markdown("## 🎯 TaskSync")
    st.markdown("Operations Strategy")
    
    st.markdown("---")
    
    # Dark mode toggle
    if st.toggle("🌙 Modo Escuro", value=st.session_state.dark_mode):
        if not st.session_state.dark_mode:
            st.session_state.dark_mode = True
            st.rerun()
    else:
        if st.session_state.dark_mode:
            st.session_state.dark_mode = False
            st.rerun()
    
    st.markdown("---")
    
    # Menu de navegação
    menu = st.radio(
        "Navegação",
        ["📊 Dashboard", "📋 Kanban", "📅 Eventos", "📚 Knowledge Base", "🏢 Empresas Target", "👥 Senior Advisors"]
    )
    
    st.markdown("---")
    
    # Busca global
    st.markdown("### 🔍 Busca Global")
    search_term = st.text_input("Buscar", placeholder="Digite para buscar...")
    
    if search_term:
        results = global_search(search_term)
        if results:
            st.markdown("#### Resultados:")
            for category, items in results.items():
                st.markdown(f"**{category}:** {len(items)} resultados")
    
    st.markdown("---")
    st.caption("TaskSync v3.0 | Raíssa Azevedo - 2026")

# Main content
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🎯 TaskSync - Operations Strategy</h1>
    <p>Gestão de desafios, próximos passos, ferramentas e conhecimento em operações</p>
</div>
""", unsafe_allow_html=True)

# Show notifications
show_notifications()

# Check deadlines
check_deadlines()

# ===== DASHBOARD =====
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Estratégico")
    
    # Carregar dados
    tasks = get_tasks()
    events = get_events()
    companies = get_companies()
    advisors = get_advisors()
    whitepapers = get_whitepapers()
    
    # Métricas em tempo real
    metrics = get_realtime_metrics()
    
    # Row 1: KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['total']}</div>
            <div class="metric-label">Total Iniciativas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        trend = "up" if metrics['productivity_rate'] > 50 else "down"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['productivity_rate']:.1f}%</div>
            <div class="metric-label">Taxa de Conclusão</div>
            <div class="metric-trend-{trend}">{'▲' if trend == 'up' else '▼'} {abs(metrics['productivity_rate'] - 50):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['delayed']}</div>
            <div class="metric-label">Atrasadas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(events)}</div>
            <div class="metric-label">Eventos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 2: Segunda linha de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['in_progress']}</div>
            <div class="metric-label">Em Andamento</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(companies)}</div>
            <div class="metric-label">Empresas Target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(advisors)}</div>
            <div class="metric-label">Senior Advisors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(whitepapers)}</div>
            <div class="metric-label">Whitepapers</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos
    st.subheader("📈 Análises e Tendências")
    show_progress_charts(tasks)
    
    # Timeline
    st.subheader("⏰ Linha do Tempo")
    show_timeline(tasks)
    
    # Próximos prazos
    st.subheader("⚠️ Prazos Próximos")
    show_upcoming_deadlines()
    
    # Atividade recente
    with st.expander("📊 Atividade Recente", expanded=False):
        show_recent_activity()
    
    # Exportação
    st.markdown("---")
    st.subheader("📥 Exportar Relatórios")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Exportar Dashboard", use_container_width=True):
            report_data = pd.DataFrame({
                "Métrica": ["Total Iniciativas", "Concluídas", "Em Andamento", "Atrasadas", "Taxa de Conclusão"],
                "Valor": [metrics['total'], metrics['completed'], metrics['in_progress'], metrics['delayed'], f"{metrics['productivity_rate']:.1f}%"]
            })
            export_to_excel(report_data, "dashboard_report")
    
    with col2:
        if st.button("📋 Exportar Tarefas", use_container_width=True):
            export_to_excel(tasks, "tasks_report")

# ===== KANBAN =====
elif menu == "📋 Kanban":
    st.header("📋 Kanban - Iniciativas")
    
    # Formulário para nova tarefa
    with st.expander("➕ Nova Iniciativa", expanded=False):
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
            tags = st.text_input("Tags (separadas por vírgula)")
            
            submitted = st.form_submit_button("Salvar")
            if submitted and title:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO tasks (title, description, category, subcategory, priority, status, owner_name, due_date, target_companies, document_link, tags)
                    VALUES (%s, %s, %s, %s, %s, 'To Do', %s, %s, %s, %s, %s)
                """, (title, description, category, subcategory, priority, owner_name, due_date, target_companies, document_link, tags))
                conn.commit()
                add_notification(f"✅ Iniciativa '{title}' criada!", "success")
                st.rerun()
    
    # Filtros avançados
    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_category = st.multiselect("Categoria", ["challenge", "next_step", "tool", "whitepaper", "initiative"])
            filter_priority = st.multiselect("Prioridade", ["Alta", "Média", "Baixa"])
        with col2:
            filter_owner = st.text_input("Responsável")
            filter_tags = st.text_input("Tags")
        with col3:
            show_completed = st.checkbox("Mostrar concluídas", value=False)
            # Salvar filtros
            filter_name = st.text_input("Nome do filtro")
            if st.button("💾 Salvar filtro atual"):
                if filter_name:
                    current_filters = {
                        "category": filter_category,
                        "priority": filter_priority,
                        "owner": filter_owner,
                        "tags": filter_tags,
                        "show_completed": show_completed
                    }
                    save_filter(filter_name, current_filters)
    
    tasks = get_tasks()
    
    if tasks.empty:
        st.info("Nenhuma tarefa cadastrada. Use o botão acima para adicionar!")
    else:
        # Aplicar filtros
        if filter_category:
            tasks = tasks[tasks['category'].isin(filter_category)]
        if filter_priority:
            tasks = tasks[tasks['priority'].isin(filter_priority)]
        if filter_owner:
            tasks = tasks[tasks['owner_name'].str.contains(filter_owner, case=False, na=False)]
        if filter_tags:
            tasks = tasks[tasks['tags'].str.contains(filter_tags, case=False, na=False)]
        if not show_completed:
            tasks = tasks[tasks['status'] != 'Done']
        
        col1, col2, col3 = st.columns(3)
        
        # COLUNA TO DO
        with col1:
            st.markdown("### 📝 To Do")
            todo_tasks = tasks[tasks['status'] == 'To Do']
            for _, row in todo_tasks.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card-modern">
                        <h4>{row['title']}</h4>
                        <div style="margin: 0.5rem 0;">
                            {get_priority_badge(row['priority'])}
                            {get_status_badge(row['status'])}
                        </div>
                        <p><strong>Responsável:</strong> {row['owner_name'] or 'N/A'}</p>
                        <p><strong>Data:</strong> {row['due_date'] or 'N/A'} {format_countdown(days_until(row['due_date'])) if row['due_date'] else ''}</p>
                        <p><small>{row['description'][:100]}...</small></p>
                        <div style="margin-top: 0.5rem;">
                            {''.join([render_tag(tag.strip()) for tag in str(row.get('tags', '')).split(',') if tag.strip()])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
                    with col_a:
                        if st.button("→ Iniciar", key=f"start_{row['id']}"):
                            cur = conn.cursor()
                            cur.execute("UPDATE tasks SET status='In Progress', start_date=%s WHERE id=%s", (date.today(), row['id']))
                            conn.commit()
                            add_notification(f"✅ Tarefa '{row['title']}' iniciada!", "success")
                            st.rerun()
                    with col_b:
                        if st.button("✏️", key=f"edit_{row['id']}"):
                            st.session_state[f"editing_{row['id']}"] = True
                    with col_c:
                        if st.button("🗑️", key=f"delete_{row['id']}"):
                            cur = conn.cursor()
                            cur.execute("DELETE FROM tasks WHERE id=%s", (row['id'],))
                            conn.commit()
                            add_notification(f"✅ Tarefa '{row['title']}' excluída!", "success")
                            st.rerun()
                    with col_d:
                        if st.button("📋", key=f"details_{row['id']}"):
                            st.session_state[f"details_{row['id']}"] = not st.session_state.get(f"details_{row['id']}", False)
                    
                    # Modal de edição
                    if st.session_state.get(f"editing_{row['id']}", False):
                        with st.form(f"edit_form_{row['id']}"):
                            st.markdown("**✏️ Editando tarefa**")
                            new_title = st.text_input("Título", value=row['title'])
                            new_description = st.text_area("Descrição", value=row['description'] or "")
                            new_priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"],
                                                       index=["Alta", "Média", "Baixa"].index(row['priority']) if row['priority'] in ["Alta", "Média", "Baixa"] else 0)
                            new_owner = st.text_input("Responsável", value=row['owner_name'] or "")
                            new_tags = st.text_input("Tags", value=row.get('tags', '') or "")
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Salvar"):
                                    cur = conn.cursor()
                                    cur.execute("""
                                        UPDATE tasks 
                                        SET title=%s, description=%s, priority=%s, owner_name=%s, tags=%s
                                        WHERE id=%s
                                    """, (new_title, new_description, new_priority, new_owner, new_tags, row['id']))
                                    conn.commit()
                                    st.session_state[f"editing_{row['id']}"] = False
                                    add_notification(f"✅ Tarefa '{new_title}' atualizada!", "success")
                                    st.rerun()
                            with col_cancel:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f"editing_{row['id']}"] = False
                                    st.rerun()
                    
                    # Detalhes expandidos
                    if st.session_state.get(f"details_{row['id']}", False):
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.05); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                            <p><strong>Descrição completa:</strong> {row['description'] or 'Sem descrição'}</p>
                            <p><strong>Empresas alvo:</strong> {row['target_companies'] or 'N/A'}</p>
                            <p><strong>Link:</strong> <a href="{row['document_link']}" target="_blank">{row['document_link'] or 'N/A'}</a></p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # COLUNA IN PROGRESS
        with col2:
            st.markdown("### 🔄 In Progress")
            ip_tasks = tasks[tasks['status'] == 'In Progress']
            for _, row in ip_tasks.iterrows():
                with st.container():
                    days_in_progress = (date.today() - row['start_date']).days if pd.notna(row['start_date']) else 0
                    
                    st.markdown(f"""
                    <div class="card-modern">
                        <h4>{row['title']}</h4>
                        <div style="margin: 0.5rem 0;">
                            {get_priority_badge(row['priority'])}
                            {get_status_badge(row['status'])}
                        </div>
                        <p><strong>Responsável:</strong> {row['owner_name'] or 'N/A'}</p>
                        <p><strong>Data:</strong> {row['due_date'] or 'N/A'} {format_countdown(days_until(row['due_date'])) if row['due_date'] else ''}</p>
                        <p><strong>Em andamento há:</strong> {days_in_progress} dias</p>
                        <div style="margin-top: 0.5rem;">
                            {''.join([render_tag(tag.strip()) for tag in str(row.get('tags', '')).split(',') if tag.strip()])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        if st.button("✅ Concluir", key=f"done_{row['id']}"):
                            cur = conn.cursor()
                            cur.execute("UPDATE tasks SET status='Done', completed_date=%s WHERE id=%s", (date.today(), row['id']))
                            conn.commit()
                            add_notification(f"✅ Tarefa '{row['title']}' concluída!", "success")
                            st.rerun()
                    with col_b:
                        if st.button("← Voltar", key=f"back_{row['id']}"):
                            cur = conn.cursor()
                            cur.execute("UPDATE tasks SET status='To Do' WHERE id=%s", (row['id'],))
                            conn.commit()
                            st.rerun()
                    with col_c:
                        if st.button("🗑️", key=f"delete_ip_{row['id']}"):
                            cur = conn.cursor()
                            cur.execute("DELETE FROM tasks WHERE id=%s", (row['id'],))
                            conn.commit()
                            add_notification(f"✅ Tarefa '{row['title']}' excluída!", "success")
                            st.rerun()
        
        # COLUNA DONE
        with col3:
            st.markdown("### ✅ Done")
            done_tasks = tasks[tasks['status'] == 'Done']
            for _, row in done_tasks.iterrows():
                st.markdown(f"""
                <div class="card-modern">
                    <h4>✓ {row['title']}</h4>
                    <p><strong>Concluído em:</strong> {row['completed_date'] or 'N/A'}</p>
                    <p><strong>Responsável:</strong> {row['owner_name'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗑️ Excluir", key=f"delete_done_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("DELETE FROM tasks WHERE id=%s", (row['id'],))
                    conn.commit()
                    add_notification(f"✅ Tarefa '{row['title']}' excluída!", "success")
                    st.rerun()

# ===== EVENTOS =====
elif menu == "📅 Eventos":
    st.header("📅 Eventos do Setor")
    
    # Filtros
    with st.expander("🔍 Filtrar Eventos", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.multiselect("Tipo", ["conference", "webinar", "workshop", "networking", "forum"])
            filter_industry = st.multiselect("Indústria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "geral"])
        with col2:
            show_past = st.checkbox("Mostrar eventos passados", value=False)
            show_virtual = st.checkbox("Mostrar apenas virtuais", value=False)
    
    # Formulário para novo evento
    with st.expander("➕ Novo Evento", expanded=False):
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
            event_link = st.text_input("Link do evento")
            
            submitted = st.form_submit_button("Salvar")
            if submitted and name:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO events (name, description, event_type, industry, start_date, end_date, location, is_virtual, event_link)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, description, event_type, industry, start_date, end_date, location, is_virtual, event_link))
                conn.commit()
                add_notification(f"✅ Evento '{name}' adicionado!", "success")
                st.rerun()
    
    events = get_events()
    
    # Visualização em calendário
    with st.expander("📅 Visualização em Calendário", expanded=False):
        show_calendar_view(events)
    
    # Lista de eventos
    st.subheader("📋 Lista de Eventos")
    
    if events.empty:
        st.info("Nenhum evento cadastrado.")
    else:
        # Aplicar filtros
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
        
        for _, row in events_filtered.iterrows():
            days = days_until(row['start_date']) if pd.notna(row['start_date']) else None
            countdown_html = format_countdown(days) if days is not None else ""
            
            st.markdown(f"""
            <div class="card-modern">
                <h4>{row['name']}</h4>
                <p><strong>Tipo:</strong> {row['event_type']} | <strong>Indústria:</strong> {row['industry']}</p>
                <p><strong>Data:</strong> {row['start_date']} a {row['end_date']} | {countdown_html}</p>
                <p><strong>Local:</strong> {row['location'] or 'N/A'} {'(Virtual)' if row['is_virtual'] else ''}</p>
                {f'<p><strong>Link:</strong> <a href="{row["event_link"]}" target="_blank">{row["event_link"]}</a></p>' if row['event_link'] else ''}
                <p>{row['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar", key=f"edit_event_{row['id']}"):
                    st.session_state[f"editing_event_{row['id']}"] = True
            with col2:
                if st.button("🗑️ Excluir", key=f"delete_event_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("DELETE FROM events WHERE id=%s", (row['id'],))
                    conn.commit()
                    add_notification(f"✅ Evento '{row['name']}' excluído!", "success")
                    st.rerun()
            
            # Modal de edição
            if st.session_state.get(f"editing_event_{row['id']}", False):
                with st.form(f"edit_event_form_{row['id']}"):
                    st.markdown("**✏️ Editando evento**")
                    new_name = st.text_input("Nome", value=row['name'])
                    new_type = st.selectbox("Tipo", ["conference", "webinar", "workshop", "networking", "forum"],
                                          index=["conference", "webinar", "workshop", "networking", "forum"].index(row['event_type']) if row['event_type'] in ["conference", "webinar", "workshop", "networking", "forum"] else 0)
                    new_industry = st.selectbox("Indústria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "geral"],
                                              index=["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "geral"].index(row['industry']) if row['industry'] in ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands", "geral"] else 0)
                    new_location = st.text_input("Local", value=row['location'] or "")
                    new_description = st.text_area("Descrição", value=row['description'] or "")
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Salvar"):
                            cur = conn.cursor()
                            cur.execute("""
                                UPDATE events 
                                SET name=%s, event_type=%s, industry=%s, location=%s, description=%s
                                WHERE id=%s
                            """, (new_name, new_type, new_industry, new_location, new_description, row['id']))
                            conn.commit()
                            st.session_state[f"editing_event_{row['id']}"] = False
                            add_notification(f"✅ Evento '{new_name}' atualizado!", "success")
                            st.rerun()
                    with col_cancel:
                        if st.form_submit_button("❌ Cancelar"):
                            st.session_state[f"editing_event_{row['id']}"] = False
                            st.rerun()

# ===== KNOWLEDGE BASE =====
elif menu == "📚 Knowledge Base":
    st.header("📚 Knowledge Base")
    
    tab1, tab2, tab3 = st.tabs(["📄 Whitepapers", "📖 Glossário", "📊 Case Studies"])
    
    # ===== TAB 1: WHITEPAPERS =====
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
                    add_notification(f"✅ Whitepaper '{title}' adicionado!", "success")
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
                <div class="card-modern">
                    <h4>{row['title']}</h4>
                    <p><strong>Tópico:</strong> {row['topic']} | <strong>Autor:</strong> {row['author_name']} | <strong>Status:</strong> {row['status']}</p>
                    <p>{row['content'][:200]}...</p>
                    <p><a href="{row['document_link']}" target="_blank">🔗 Link para documento</a></p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Editar", key=f"edit_wp_{row['id']}"):
                        st.session_state[f"editing_wp_{row['id']}"] = True
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_wp_{row['id']}"):
                        cur = conn.cursor()
                        cur.execute("DELETE FROM whitepapers WHERE id=%s", (row['id'],))
                        conn.commit()
                        add_notification(f"✅ Whitepaper '{row['title']}' excluído!", "success")
                        st.rerun()
                
                # Modal de edição
                if st.session_state.get(f"editing_wp_{row['id']}", False):
                    with st.form(f"edit_wp_form_{row['id']}"):
                        st.markdown("**✏️ Editando whitepaper**")
                        new_title = st.text_input("Título", value=row['title'])
                        new_topic = st.text_input("Tópico", value=row['topic'] or "")
                        new_author = st.text_input("Autor", value=row['author_name'] or "")
                        new_status = st.selectbox("Status", ["draft", "review", "published"],
                                                index=["draft", "review", "published"].index(row['status']) if row['status'] in ["draft", "review", "published"] else 0)
                        new_link = st.text_input("Link", value=row['document_link'] or "")
                        new_content = st.text_area("Conteúdo", value=row['content'] or "")
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Salvar"):
                                cur = conn.cursor()
                                cur.execute("""
                                    UPDATE whitepapers 
                                    SET title=%s, topic=%s, author_name=%s, status=%s, document_link=%s, content=%s
                                    WHERE id=%s
                                """, (new_title, new_topic, new_author, new_status, new_link, new_content, row['id']))
                                conn.commit()
                                st.session_state[f"editing_wp_{row['id']}"] = False
                                add_notification(f"✅ Whitepaper '{new_title}' atualizado!", "success")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f"editing_wp_{row['id']}"] = False
                                st.rerun()
        else:
            st.info("Nenhum whitepaper cadastrado.")
    
    # ===== TAB 2: GLOSSÁRIO =====
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
                    add_notification(f"✅ Termo '{term}' adicionado!", "success")
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
                <div class="card-modern">
                    <h4>{row['term']}</h4>
                    <p><em>{row['definition']}</em></p>
                    <p><strong>Categoria:</strong> {row['category']} | <strong>Exemplo:</strong> {row['example'] or 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Editar", key=f"edit_term_{row['id']}"):
                        st.session_state[f"editing_term_{row['id']}"] = True
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_term_{row['id']}"):
                        cur = conn.cursor()
                        cur.execute("DELETE FROM glossary WHERE id=%s", (row['id'],))
                        conn.commit()
                        add_notification(f"✅ Termo '{row['term']}' excluído!", "success")
                        st.rerun()
                
                if st.session_state.get(f"editing_term_{row['id']}", False):
                    with st.form(f"edit_term_form_{row['id']}"):
                        st.markdown("**✏️ Editando termo**")
                        new_term = st.text_input("Termo", value=row['term'])
                        new_definition = st.text_area("Definição", value=row['definition'])
                        new_category = st.selectbox("Categoria", ["technical", "business", "acronym"],
                                                  index=["technical", "business", "acronym"].index(row['category']) if row['category'] in ["technical", "business", "acronym"] else 0)
                        new_example = st.text_input("Exemplo", value=row['example'] or "")
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Salvar"):
                                cur = conn.cursor()
                                cur.execute("""
                                    UPDATE glossary 
                                    SET term=%s, definition=%s, category=%s, example=%s
                                    WHERE id=%s
                                """, (new_term, new_definition, new_category, new_example, row['id']))
                                conn.commit()
                                st.session_state[f"editing_term_{row['id']}"] = False
                                add_notification(f"✅ Termo '{new_term}' atualizado!", "success")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f"editing_term_{row['id']}"] = False
                                st.rerun()
        else:
            st.info("Nenhum termo cadastrado no glossário.")
    
    # ===== TAB 3: CASE STUDIES =====
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
                    add_notification(f"✅ Case Study '{title}' adicionado!", "success")
                    st.rerun()
        
        cases = get_cases()
        
        if cases.empty:
            st.info("Nenhum case study cadastrado.")
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
                <div class="card-modern">
                    <h4>{row['title']}</h4>
                    <p><strong>Categoria:</strong> {row['category']} | <strong>Autor:</strong> {row['author'] or 'N/A'}</p>
                    <p><strong>Resumo:</strong> {row['summary']}</p>
                    <p><strong>Tags:</strong> {row['tags'] or 'N/A'}</p>
                    {f'<p><a href="{row["document_link"]}" target="_blank">🔗 Link para documento</a></p>' if row['document_link'] else ''}
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Editar", key=f"edit_case_{row['id']}"):
                        st.session_state[f"editing_case_{row['id']}"] = True
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_case_{row['id']}"):
                        cur = conn.cursor()
                        cur.execute("DELETE FROM knowledge_base WHERE id=%s", (row['id'],))
                        conn.commit()
                        add_notification(f"✅ Case Study '{row['title']}' excluído!", "success")
                        st.rerun()
                
                if st.session_state.get(f"editing_case_{row['id']}", False):
                    with st.form(f"edit_case_form_{row['id']}"):
                        st.markdown("**✏️ Editando case study**")
                        new_title = st.text_input("Título", value=row['title'])
                        new_category = st.selectbox("Categoria", ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands"],
                                                  index=["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands"].index(row['category']) if row['category'] in ["manufacturing", "supply_chain", "digital_twin", "ia_ml", "healthcare", "b2b", "brands"] else 0)
                        new_summary = st.text_area("Resumo", value=row['summary'])
                        new_content = st.text_area("Conteúdo", value=row['content'] or "")
                        new_author = st.text_input("Autor", value=row['author'] or "")
                        new_tags = st.text_input("Tags", value=row['tags'] or "")
                        new_link = st.text_input("Link", value=row['document_link'] or "")
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Salvar"):
                                cur = conn.cursor()
                                cur.execute("""
                                    UPDATE knowledge_base 
                                    SET title=%s, category=%s, summary=%s, content=%s, author=%s, tags=%s, document_link=%s
                                    WHERE id=%s
                                """, (new_title, new_category, new_summary, new_content, new_author, new_tags, new_link, row['id']))
                                conn.commit()
                                st.session_state[f"editing_case_{row['id']}"] = False
                                add_notification(f"✅ Case Study '{new_title}' atualizado!", "success")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f"editing_case_{row['id']}"] = False
                                st.rerun()

# ===== EMPRESAS TARGET =====
elif menu == "🏢 Empresas Target":
    st.header("🏢 Empresas Target")
    
    # Buscador e filtros
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Buscar por nome, indústria ou contato", key="search_companies")
    with col2:
        filter_status = st.selectbox("Status", ["Todos", "prospect", "contacted", "meeting", "proposal", "closed"])
    
    with st.expander("➕ Nova Empresa", expanded=False):
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
                add_notification(f"✅ Empresa '{name}' adicionada!", "success")
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
            <div class="card-modern">
                <h4>{row['name']}</h4>
                <p><strong>Indústria:</strong> {row['industry']} | <strong>Porte:</strong> {row['size']} | <strong>Status:</strong> {row['status']}</p>
                <p><strong>Contato:</strong> {row['contact_person'] or 'N/A'} | {row['contact_email'] or 'N/A'} | {row['contact_phone'] or 'N/A'}</p>
                <p><strong>Valor potencial:</strong> {row['potential_value'] or 'N/A'}</p>
                <p><em>{row['notes']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar", key=f"edit_company_{row['id']}"):
                    st.session_state[f"editing_company_{row['id']}"] = True
            with col2:
                if st.button("🗑️ Excluir", key=f"delete_company_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("DELETE FROM target_companies WHERE id=%s", (row['id'],))
                    conn.commit()
                    add_notification(f"✅ Empresa '{row['name']}' excluída!", "success")
                    st.rerun()
            
            if st.session_state.get(f"editing_company_{row['id']}", False):
                with st.form(f"edit_company_form_{row['id']}"):
                    st.markdown("**✏️ Editando empresa**")
                    new_name = st.text_input("Nome", value=row['name'])
                    new_industry = st.selectbox("Indústria", ["manufacturing", "healthcare", "b2b", "brands", "supply_chain", "tech"],
                                              index=["manufacturing", "healthcare", "b2b", "brands", "supply_chain", "tech"].index(row['industry']) if row['industry'] in ["manufacturing", "healthcare", "b2b", "brands", "supply_chain", "tech"] else 0)
                    new_status = st.selectbox("Status", ["prospect", "contacted", "meeting", "proposal", "closed"],
                                            index=["prospect", "contacted", "meeting", "proposal", "closed"].index(row['status']) if row['status'] in ["prospect", "contacted", "meeting", "proposal", "closed"] else 0)
                    new_contact = st.text_input("Contato", value=row['contact_person'] or "")
                    new_email = st.text_input("Email", value=row['contact_email'] or "")
                    new_notes = st.text_area("Observações", value=row['notes'] or "")
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Salvar"):
                            cur = conn.cursor()
                            cur.execute("""
                                UPDATE target_companies 
                                SET name=%s, industry=%s, status=%s, contact_person=%s, contact_email=%s, notes=%s
                                WHERE id=%s
                            """, (new_name, new_industry, new_status, new_contact, new_email, new_notes, row['id']))
                            conn.commit()
                            st.session_state[f"editing_company_{row['id']}"] = False
                            add_notification(f"✅ Empresa '{new_name}' atualizada!", "success")
                            st.rerun()
                    with col_cancel:
                        if st.form_submit_button("❌ Cancelar"):
                            st.session_state[f"editing_company_{row['id']}"] = False
                            st.rerun()

# ===== SENIOR ADVISORS =====
elif menu == "👥 Senior Advisors":
    st.header("👥 Senior Advisors")
    
    search_term = st.text_input("🔍 Buscar por nome, expertise, empresa ou tópicos", key="search_advisors")
    
    with st.expander("➕ Novo Advisor", expanded=False):
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
                add_notification(f"✅ Advisor '{name}' adicionado!", "success")
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
            <div class="card-modern">
                <h4>{row['name']}</h4>
                <p><strong>Expertise:</strong> {row['expertise']} | <strong>Empresa:</strong> {row['company'] or 'N/A'}</p>
                <p><strong>Tópicos:</strong> {row['topics'] or 'N/A'}</p>
                <p><strong>Eventos:</strong> {row['events_participated'] or 'N/A'}</p>
                <p><strong>LinkedIn:</strong> <a href="{row['linkedin']}" target="_blank">{row['linkedin']}</a></p>
                <p><em>{row['notes']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar", key=f"edit_advisor_{row['id']}"):
                    st.session_state[f"editing_advisor_{row['id']}"] = True
            with col2:
                if st.button("🗑️ Excluir", key=f"delete_advisor_{row['id']}"):
                    cur = conn.cursor()
                    cur.execute("DELETE FROM senior_advisors WHERE id=%s", (row['id'],))
                    conn.commit()
                    add_notification(f"✅ Advisor '{row['name']}' excluído!", "success")
                    st.rerun()
            
            if st.session_state.get(f"editing_advisor_{row['id']}", False):
                with st.form(f"edit_advisor_form_{row['id']}"):
                    st.markdown("**✏️ Editando advisor**")
                    new_name = st.text_input("Nome", value=row['name'])
                    new_expertise = st.text_input("Expertise", value=row['expertise'] or "")
                    new_company = st.text_input("Empresa", value=row['company'] or "")
                    new_topics = st.text_input("Tópicos", value=row['topics'] or "")
                    new_linkedin = st.text_input("LinkedIn", value=row['linkedin'] or "")
                    new_notes = st.text_area("Notas", value=row['notes'] or "")
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Salvar"):
                            cur = conn.cursor()
                            cur.execute("""
                                UPDATE senior_advisors 
                                SET name=%s, expertise=%s, company=%s, topics=%s, linkedin=%s, notes=%s
                                WHERE id=%s
                            """, (new_name, new_expertise, new_company, new_topics, new_linkedin, new_notes, row['id']))
                            conn.commit()
                            st.session_state[f"editing_advisor_{row['id']}"] = False
                            add_notification(f"✅ Advisor '{new_name}' atualizado!", "success")
                            st.rerun()
                    with col_cancel:
                        if st.form_submit_button("❌ Cancelar"):
                            st.session_state[f"editing_advisor_{row['id']}"] = False
                            st.rerun()

# Rodapé
st.markdown("---")
st.caption("TaskSync v3.0 - Operations Strategy | Desenvolvido com Streamlit | Raíssa Azevedo - 2026")