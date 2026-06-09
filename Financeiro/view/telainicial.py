import tkinter as tk
from tkinter import ttk, messagebox




class TelaInicial:
    """Tela inicial do sistema após login bem-sucedido."""

    def __init__(self, usuario):
        """
        Inicializa a tela inicial.
        
        Args:
            usuario: Objeto usuário autenticado
        """
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title(f"Sistema Financeiro - {usuario.nome}")
        self.root.geometry("1000x700")
        self.root.state("zoomed")  # Maximiza a janela
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self._build_ui()

    def _build_ui(self) -> None:
        """Constrói a interface da tela inicial."""
        # Frame principal com duas colunas
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Menu lateral
        self._build_sidebar(main_frame)
        
        # Área principal
        self._build_content_area(main_frame)

    def _build_sidebar(self, parent) -> None:
        """Constrói o menu lateral com os módulos."""
        sidebar_frame = ttk.Frame(parent, width=250, relief="sunken", borderwidth=2)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        sidebar_frame.grid_rowconfigure(0, weight=1)
        
        # Título
        title_frame = ttk.Frame(sidebar_frame)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=15)
        
        ttk.Label(
            title_frame,
            text="MÓDULOS",
            font=("Arial", 14, "bold")
        ).pack()
        
        ttk.Separator(sidebar_frame, orient="horizontal").grid(
            row=1, column=0, sticky="ew", padx=10, pady=10
        )
        
        # Canvas com scroll
        canvas = tk.Canvas(sidebar_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Módulos
        self._create_menu_item(
            scrollable_frame,
            "📦 OPERAÇÕES DE CAIXA",
            [
                ("🔓 Abertura de Caixa", self._abrir_caixa),
                ("🔒 Fechamento de Caixa", None),
            ]
        )
        
        self._create_menu_item(
            scrollable_frame,
            "💳 PAGAMENTOS",
            [
                ("💰 Registrar Pagamento", None),
            ]
        )
        
        self._create_menu_item(
            scrollable_frame,
            "📄 COMPROVANTES",
            [
                ("🖨️ Emitir Comprovante", None),
            ]
        )
        
        # Botão de sair
        ttk.Separator(scrollable_frame, orient="horizontal").pack(
            fill="x", pady=20
        )
        
        ttk.Button(
            scrollable_frame,
            text="🚪 SAIR",
            command=self._logout,
            width=30
        ).pack(fill="x", padx=5, pady=5)
        
        canvas.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        sidebar_frame.grid_rowconfigure(2, weight=1)

    def _create_menu_item(self, parent, menu_title: str, submenu_items: list) -> None:
        """Cria um item de menu com subitens."""
        module_frame = ttk.LabelFrame(
            parent,
            text=menu_title,
            padding=8,
            relief="groove"
        )
        module_frame.pack(fill="x", padx=5, pady=8)
        
        for label, callback in submenu_items:
            command = callback if callable(callback) else lambda l=label: messagebox.showinfo(
                "Aviso",
                f"{l} será implementado em breve.",
                parent=self.root
            )
            ttk.Button(
                module_frame,
                text=label,
                width=28,
                command=command,
            ).pack(fill="x", pady=3)

    def _build_content_area(self, parent) -> None:
        """Constrói a área principal de conteúdo."""
        content_frame = ttk.Frame(parent, relief="sunken", borderwidth=2)
        content_frame.grid(row=0, column=1, sticky="nsew")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        welcome_frame = ttk.Frame(content_frame)
        welcome_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        welcome_frame.grid_rowconfigure(2, weight=1)
        welcome_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(
            welcome_frame,
            text=f"Bem-vindo, {self.usuario.nome}!",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, sticky="w", pady=10)
        
        ttk.Separator(welcome_frame, orient="horizontal").grid(
            row=1, column=0, sticky="ew", pady=10
        )
        
        info_text = f"""
Perfil: {self.usuario.perfil}
Login: {self.usuario.login}

Selecione uma opção no menu lateral para começar.

Módulos Disponíveis:
• Operações de Caixa: Gerenciar aberturas e fechamentos de caixa
• Pagamentos: Registrar e processar pagamentos
• Comprovantes: Emitir e consultar comprovantes de transações
        """
        
        ttk.Label(
            welcome_frame,
            text=info_text,
            font=("Arial", 11),
            justify="left"
        ).grid(row=2, column=0, sticky="nw", pady=10)
        
        ttk.Separator(welcome_frame, orient="horizontal").grid(
            row=3, column=0, sticky="ew", pady=20
        )
        
        ttk.Label(
            welcome_frame,
            text="Sistema Financeiro - ERP v1.0",
            font=("Arial", 9),
            foreground="gray"
        ).grid(row=4, column=0, sticky="e", pady=10)

        # Caixa atual (grid resumida)
        caixa_frame = ttk.LabelFrame(content_frame, text="Caixa Atual", padding=8)
        caixa_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        caixa_frame.grid_columnconfigure(0, weight=1)

        columns = ("dataAbertura", "saldoInicial", "status")
        self.caixa_tree = ttk.Treeview(caixa_frame, columns=columns, show="headings", height=1)
        self.caixa_tree.heading("dataAbertura", text="Data Abertura")
        self.caixa_tree.heading("saldoInicial", text="Saldo Inicial")
        self.caixa_tree.heading("status", text="Status")
        self.caixa_tree.column("dataAbertura", width=220)
        self.caixa_tree.column("saldoInicial", width=120, anchor="e")
        self.caixa_tree.column("status", width=120)
        self.caixa_tree.grid(row=0, column=0, sticky="ew")

        # placeholder quando não há caixa aberto
        self._set_caixa_placeholder()

    def _abrir_caixa(self) -> None:
        from .caixa_abertura_view import CaixaAberturaView

        CaixaAberturaView(self)

    def _set_caixa_placeholder(self) -> None:
        # Remove linhas existentes e mostra mensagem de vazio
        for i in self.caixa_tree.get_children():
            self.caixa_tree.delete(i)
        self.caixa_tree.insert("", "end", values=("—", "—", "—"))

    def update_caixa(self, caixa_data: dict) -> None:
        """Atualiza a grid de caixa com os dados retornados pela API.

        Espera um dicionário contendo as chaves: `dataAbertura`, `saldoInicial`, `status`.
        """
        for i in self.caixa_tree.get_children():
            self.caixa_tree.delete(i)

        data_abertura = caixa_data.get("dataAbertura") or caixa_data.get("dataAbertura")
        saldo_inicial = caixa_data.get("saldoInicial")
        status = caixa_data.get("status")

        # Formatar saldo
        try:
            saldo_text = f"{float(saldo_inicial):.2f}" if saldo_inicial is not None else "—"
        except Exception:
            saldo_text = str(saldo_inicial)

        self.caixa_tree.insert("", "end", values=(data_abertura or "—", saldo_text, status or "—"))

    def _logout(self) -> None:
        """Callback para logout."""
        if messagebox.askyesno(
            "Logout",
            "Deseja realmente sair do sistema?",
            parent=self.root
        ):
            self.root.destroy()

    def run(self) -> None:
        """Inicia a tela inicial."""
        self.root.mainloop()
