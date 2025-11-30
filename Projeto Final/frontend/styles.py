COLORS = {
    'primary': '#2c3e50',           # Azul escuro principal
    'primary_light': '#34495e',     # Azul escuro claro
    'secondary': '#1abc9c',         # Verde turquesa
    'secondary_dark': '#16a085',    # Verde turquesa escuro
    'accent': '#3498db',            # Azul claro
    'accent_dark': '#2980b9',       # Azul claro escuro
    'background': '#ecf0f1',        # Cinza muito claro
    'surface': '#ffffff',           # Branco
    'surface_dark': '#f8f9fa',      # Cinza clarinho
    'text': '#2c3e50',              # Texto escuro
    'text_light': '#7f8c8d',        # Texto claro
    'text_white': '#ffffff',        # Texto branco
    'border': '#bdc3c7',            # Bordas
    'border_light': '#ecf0f1',      # Bordas claras
    'success': '#27ae60',           # Verde sucesso
    'warning': '#f39c12',           # Laranja aviso
    'error': '#e74c3c',             # Vermelho erro
    'disabled': '#95a5a6',          # Cinza desabilitado
}

# Tamanhos e dimensões
SIZES = {
    'header_height': 80,
    'button_height': 36,
    'input_height': 36,
    'card_padding': 16,
    'border_radius': 6,
    'border_radius_small': 4,
    'spacing': 12,
    'spacing_small': 6,
    'spacing_large': 20,
}

# Fontes
FONTS = {
    'family': "'Segoe UI', 'Roboto', 'Arial', sans-serif",
    'size_small': 11,
    'size_normal': 12,
    'size_medium': 14,
    'size_large': 16,
    'size_xlarge': 18,
    'size_title': 20,
}

def get_global_stylesheet():
    """Retorna o stylesheet global da aplicação"""
    return f"""
        /* Configurações globais */
        QMainWindow {{
            background-color: {COLORS['background']};
            color: {COLORS['text']};
            font-family: {FONTS['family']};
            font-size: {FONTS['size_normal']}px;
        }}
        
        QWidget {{
            font-family: {FONTS['family']};
            font-size: {FONTS['size_normal']}px;
            color: {COLORS['text']};
        }}
        
        /* Scrollbars */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: {COLORS['border_light']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {COLORS['border']};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['text_light']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        
        /* Cards e containers */
        .card {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border_light']};
            border-radius: {SIZES['border_radius']}px;
            padding: {SIZES['card_padding']}px;
        }}
        
        .card:hover {{
            border-color: {COLORS['secondary']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    """

def get_button_stylesheet(button_type='primary'):
    """Retorna stylesheet para botões com diferentes tipos"""
    styles = {
        'primary': {
            'bg': COLORS['secondary'],
            'bg_hover': COLORS['secondary_dark'],
            'bg_pressed': '#138d75',
            'text': COLORS['text_white']
        },
        'secondary': {
            'bg': COLORS['accent'],
            'bg_hover': COLORS['accent_dark'],
            'bg_pressed': '#21618c',
            'text': COLORS['text_white']
        },
        'outline': {
            'bg': 'transparent',
            'bg_hover': COLORS['surface_dark'],
            'bg_pressed': COLORS['border_light'],
            'text': COLORS['text']
        },
        'danger': {
            'bg': COLORS['error'],
            'bg_hover': '#c0392b',
            'bg_pressed': '#a93226',
            'text': COLORS['text_white']
        }
    }
    
    style = styles.get(button_type, styles['primary'])
    border = f"1px solid {COLORS['border']}" if button_type == 'outline' else "none"
    
    return f"""
        QPushButton {{
            background-color: {style['bg']};
            color: {style['text']};
            border: {border};
            border-radius: {SIZES['border_radius']}px;
            font-weight: 600;
            padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
            min-height: {SIZES['button_height'] - 16}px;
            font-size: {FONTS['size_normal']}px;
        }}
        
        QPushButton:hover {{
            background-color: {style['bg_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {style['bg_pressed']};
        }}
        
        QPushButton:disabled {{
            background-color: {COLORS['disabled']};
            color: {COLORS['text_white']};
            border: none;
        }}
    """

def get_input_stylesheet():
    """Retorna stylesheet para campos de entrada"""
    return f"""
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: {SIZES['border_radius_small']}px;
            padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
            font-size: {FONTS['size_normal']}px;
            color: {COLORS['text']};
            min-height: {SIZES['input_height'] - 16}px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {COLORS['secondary']};
            outline: none;
        }}
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background-color: {COLORS['surface_dark']};
            color: {COLORS['text_light']};
        }}
    """

def get_header_stylesheet():
    """Retorna stylesheet específico para o cabeçalho"""
    return f"""
        HeaderWidget {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 {COLORS['primary_light']}, stop: 1 {COLORS['primary']});
            border-bottom: 3px solid {COLORS['secondary']};
            color: {COLORS['text_white']};
            min-height: {SIZES['header_height']}px;
            max-height: {SIZES['header_height']}px;
        }}
        
        HeaderWidget QLabel {{
            color: {COLORS['text_white']};
            font-weight: 600;
        }}
        
        HeaderWidget QLabel#logo {{
            color: {COLORS['secondary']};
            font-size: {FONTS['size_large']}px;
            font-weight: 700;
        }}
        
        HeaderWidget QPushButton {{
            background-color: {COLORS['secondary']};
            color: {COLORS['text_white']};
            border: none;
            border-radius: {SIZES['border_radius']}px;
            font-weight: 600;
            padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
            min-height: {SIZES['button_height'] - 8}px;
            font-size: {FONTS['size_normal']}px;
        }}
        
        HeaderWidget QPushButton:hover {{
            background-color: {COLORS['secondary_dark']};
        }}
        
        HeaderWidget QPushButton:pressed {{
            background-color: #138d75;
        }}
        
        HeaderWidget QPushButton:disabled {{
            background-color: {COLORS['disabled']};
            color: #bdc3c7;
        }}
    """

def get_table_stylesheet():
    """Retorna stylesheet para tabelas"""
    return f"""
        QTableWidget {{
            background-color: {COLORS['surface']};
            alternate-background-color: {COLORS['surface_dark']};
            border: 1px solid {COLORS['border_light']};
            border-radius: {SIZES['border_radius_small']}px;
            gridline-color: {COLORS['border_light']};
            font-size: {FONTS['size_normal']}px;
        }}
        
        QTableWidget::item {{
            padding: {SIZES['spacing_small']}px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {COLORS['secondary']};
            color: {COLORS['text_white']};
        }}
        
        QHeaderView::section {{
            background-color: {COLORS['primary']};
            color: {COLORS['text_white']};
            padding: {SIZES['spacing']}px;
            border: none;
            font-weight: 600;
            font-size: {FONTS['size_normal']}px;
        }}
    """

def get_dialog_stylesheet():
    """Retorna stylesheet para diálogos"""
    return f"""
        QDialog {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: {SIZES['border_radius']}px;
        }}
        
        QDialog QLabel {{
            color: {COLORS['text']};
            font-size: {FONTS['size_normal']}px;
        }}
        
        QDialog QLabel#title {{
            font-size: {FONTS['size_large']}px;
            font-weight: 600;
            color: {COLORS['primary']};
        }}
    """
