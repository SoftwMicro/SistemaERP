# styles/theme.py
from tkinter import ttk

class AppTheme:
    def __init__(self, root):
        self.style = ttk.Style(root)
        
        # Opcional: Forçar um tema que aceita mudança de cores (ex: clam)
        self.style.theme_use("clam")
        
        # Chamamos o método que vai configurar todos os nossos estilos
        self._configurar_estilos()

    def _configurar_estilos(self):
        # Cor de fundo padrão para os frames
        self.style.configure(".", background="#f5f5f5")
        
        # Estilo para o Botão de Confirmar (Verde)
        self.style.configure("Confirmar.TButton", 
                             background="#2ecc71", 
                             foreground="white", 
                             font=("Arial", 10, "bold"),
                             padding=6)
        
        # Estilo para o Botão de Cancelar (Vermelho)
        self.style.configure("Cancelar.TButton", 
                             background="#e74c3c", 
                             foreground="white", 
                             font=("Arial", 10, "bold"),
                             padding=6)
        
        self.style.configure("Entregue.TButton", 
                             background="#cc552e", 
                             foreground="white", 
                             font=("Arial", 10, "bold"),
                             padding=6)