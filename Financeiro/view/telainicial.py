import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from .caixa_abertura_view import CaixaAberturaView
from .caixa_fechamento_view import CaixaFechamentoView
from .comprovante_view import EmitirComprovanteView
from .registrar_pagamento_view import RegistrarPagamentoView
from ..repository.caixa_repository import CaixaRepository



class TelaInicial:
    """Tela inicial do sistema após login bem-sucedido."""

    def __init__(self, usuario):
        """
        Inicializa a tela inicial.
        
        Args:
            usuario: Objeto usuário autenticado
        """
        self.usuario = usuario
        self.repository = CaixaRepository()
        self.root = tk.Tk()
        self.root.title(f"Sistema Financeiro - {usuario.nome}")
        self.root.geometry("1000x700")
        self.root.state("zoomed")  # Maximiza a janela
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self._build_ui()
        self._load_caixa_aberturas()

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
                ("🔒 Fechamento de Caixa", self._fechar_caixa),
            ]
        )
        
        self._create_menu_item(
            scrollable_frame,
            "💳 PAGAMENTOS",
            [
                ("💰 Registrar Pagamento", self._abrir_registrar_pagamento),
            ]
        )
        
        self._create_menu_item(
            scrollable_frame,
            "📄 COMPROVANTES",
            [
                ("🖨️ Emitir Comprovante", self._abrir_emitir_comprovante),
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

        columns = ("id", "dataAbertura", "saldoInicial", "dataFechamento", "saldoFinal", "status")
        self.caixa_tree = ttk.Treeview(caixa_frame, columns=columns, show="headings", height=5, selectmode="browse")
        self.caixa_tree.heading("id", text="ID")
        self.caixa_tree.heading("dataAbertura", text="Data Abertura")
        self.caixa_tree.heading("saldoInicial", text="Saldo Inicial")
        self.caixa_tree.heading("dataFechamento", text="Data Fechamento")
        self.caixa_tree.heading("saldoFinal", text="Saldo Final")
        self.caixa_tree.heading("status", text="Status")
        self.caixa_tree.column("id", width=80, anchor="center")
        self.caixa_tree.column("dataAbertura", width=160)
        self.caixa_tree.column("saldoInicial", width=120, anchor="e")
        self.caixa_tree.column("dataFechamento", width=160)
        self.caixa_tree.column("saldoFinal", width=120, anchor="e")
        self.caixa_tree.column("status", width=120)
        
        scrollbar = ttk.Scrollbar(caixa_frame, orient="vertical", command=self.caixa_tree.yview)
        self.caixa_tree.configure(yscroll=scrollbar.set)
        
        self.caixa_tree.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # placeholder quando não há caixa aberto
        self._set_caixa_placeholder()

    def _abrir_caixa(self) -> None:
        CaixaAberturaView(self)

    def _abrir_registrar_pagamento(self) -> None:
        RegistrarPagamentoView(self)

    def _abrir_emitir_comprovante(self) -> None:
        EmitirComprovanteView(self)

    def _fechar_caixa(self) -> None:
        selected = self.caixa_tree.selection()
        if not selected:
            messagebox.showerror(
                "Fechamento de Caixa",
                "Selecione exatamente um registro para fechamento.",
                parent=self.root,
            )
            return

        if len(selected) > 1:
            messagebox.showerror(
                "Fechamento de Caixa",
                "Selecione apenas um registro para fechamento.",
                parent=self.root,
            )
            return

        item_id = selected[0]
        values = self.caixa_tree.item(item_id, "values")
        caixa_id = values[0] if values else None

        if caixa_id in (None, "—", ""):
            messagebox.showerror(
                "Fechamento de Caixa",
                "Selecione um registro válido para fechamento.",
                parent=self.root,
            )
            return

        status_value = values[5] if len(values) > 5 else None
        if not status_value or str(status_value).strip().upper() != "ABERTO":
            messagebox.showerror(
                "Fechamento de Caixa",
                "Selecione apenas um registro com status ABERTO para fechamento.",
                parent=self.root,
            )
            return

        try:
            caixa_id_int = int(caixa_id)
        except (ValueError, TypeError):
            messagebox.showerror(
                "Fechamento de Caixa",
                "O registro selecionado não possui um ID de caixa válido.",
                parent=self.root,
            )
            return

        CaixaFechamentoView(self, caixa_id_int)

    def _load_caixa_aberturas(self) -> None:
        """Carrega as últimas aberturas de caixa do usuário ao inicializar a tela."""
        try:
            aberturas = self.repository.obter_aberturas_fechamentos(self.usuario.id)
            self.update_caixa_list(aberturas)
        except Exception as error:
            # Se houver erro ao carregar, apenas mostra placeholder
            print(f"Aviso: Erro ao carregar aberturas de caixa: {error}")
            self._set_caixa_placeholder()

    def update_caixa_list(self, aberturas: list) -> None:
        """Atualiza a grid de caixa com a lista de aberturas.

        Args:
            aberturas: Lista de dicionários com dados das aberturas
        """
        for i in self.caixa_tree.get_children():
            self.caixa_tree.delete(i)

        if not aberturas:
            self._set_caixa_placeholder()
            return

        for abertura in aberturas:
            caixa_id = abertura.get("id")
            data_abertura = abertura.get("dataAbertura")
            saldo_inicial = abertura.get("saldoInicial")
            data_fechamento = abertura.get("dataFechamento")
            saldo_final = abertura.get("saldoFinal")
            status = abertura.get("status")

            # Formatar data/hora
            data_abertura_text = self._format_datetime(data_abertura) if data_abertura else "—"
            data_fechamento_text = self._format_datetime(data_fechamento) if data_fechamento else "—"

            # Formatar saldos
            try:
                saldo_inicial_text = self._format_currency(float(saldo_inicial)) if saldo_inicial is not None else "—"
            except (ValueError, TypeError):
                saldo_inicial_text = str(saldo_inicial) if saldo_inicial is not None else "—"

            try:
                saldo_final_text = self._format_currency(float(saldo_final)) if saldo_final is not None else "—"
            except (ValueError, TypeError):
                saldo_final_text = str(saldo_final) if saldo_final is not None else "—"

            self.caixa_tree.insert(
                "",
                "end",
                values=(
                    caixa_id or "—",
                    data_abertura_text,
                    saldo_inicial_text,
                    data_fechamento_text,
                    saldo_final_text,
                    status or "—",
                ),
            )

    def _set_caixa_placeholder(self) -> None:
        # Remove linhas existentes e mostra mensagem de vazio
        for i in self.caixa_tree.get_children():
            self.caixa_tree.delete(i)
        self.caixa_tree.insert("", "end", values=("—", "Nenhuma abertura de caixa", "—", "—", "—", "—"))

    def _format_datetime(self, value: str) -> str:
        if not value:
            return "—"

        try:
            dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                dt = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    dt = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    return value

        return dt.strftime("%d-%m-%Y %H:%M")

    def _format_currency(self, value: float) -> str:
        integer_part, _, decimal_part = f"{value:.2f}".partition(".")
        integer_part_with_sep = "".join(
            [
                integer_part[max(i - 3, 0):i] + ("." if i != len(integer_part) else "")
                for i in range(len(integer_part) % 3 or 3, len(integer_part) + 1, 3)
            ]
        )
        return f"R$ {integer_part_with_sep},{decimal_part}"

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
