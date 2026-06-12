import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from ..controller.pagamento_controller import PagamentoController


class RegistrarPagamentoView:
    def __init__(self, owner):
        self.owner = owner
        parent = getattr(owner, "root", owner)
        self.controller = PagamentoController()
        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Pagamento")
        self.window.geometry("900x650")
        self.window.minsize(900, 650)
        self.window.resizable(True, True)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grab_set()
        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.window, padding=12)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        search_frame = ttk.LabelFrame(main_frame, text="Pesquisa de Pedido", padding=10)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="ID do Pedido:").grid(row=0, column=0, sticky="w", pady=4)
        self.id_entry = ttk.Entry(search_frame, width=24)
        self.id_entry.grid(row=0, column=1, sticky="w", pady=4)
        self.id_entry.focus()

        ttk.Button(search_frame, text="Pesquisar", command=self._on_search).grid(
            row=0, column=2, padx=8, pady=4
        )

        self.info_frame = ttk.LabelFrame(main_frame, text="Dados do Pedido", padding=10)
        self.info_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.info_frame.grid_columnconfigure(1, weight=1)

        labels = [
            ("Número:", "numero"),
            ("Data de criação:", "data_criacao"),
            ("Cliente:", "cliente"),
            ("Status:", "status"),
            ("Valor total:", "valor_total"),
            ("Observações:", "observacoes"),
        ]

        self.info_labels = {}
        for index, (text, key) in enumerate(labels):
            ttk.Label(self.info_frame, text=text).grid(row=index, column=0, sticky="nw", pady=4)
            label = ttk.Label(self.info_frame, text="—", wraplength=620, justify="left")
            label.grid(row=index, column=1, sticky="w", pady=4)
            self.info_labels[key] = label

        items_frame = ttk.LabelFrame(main_frame, text="Itens do Pedido", padding=10)
        items_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        items_frame.grid_rowconfigure(0, weight=1)
        items_frame.grid_columnconfigure(0, weight=1)

        columns = ("produto", "quantidade", "preco_unitario", "subtotal")
        self.items_tree = ttk.Treeview(
            items_frame,
            columns=columns,
            show="headings",
            height=6,
            selectmode="none",
        )
        self.items_tree.heading("produto", text="Produto")
        self.items_tree.heading("quantidade", text="Quantidade")
        self.items_tree.heading("preco_unitario", text="Preço Unitário")
        self.items_tree.heading("subtotal", text="Subtotal")

        self.items_tree.column("produto", width=320)
        self.items_tree.column("quantidade", width=100, anchor="center")
        self.items_tree.column("preco_unitario", width=140, anchor="e")
        self.items_tree.column("subtotal", width=140, anchor="e")

        item_scroll = ttk.Scrollbar(items_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscroll=item_scroll.set)
        self.items_tree.grid(row=0, column=0, sticky="nsew")
        item_scroll.grid(row=0, column=1, sticky="ns")

        history_frame = ttk.LabelFrame(main_frame, text="Histórico de Status", padding=10)
        history_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        history_frame.grid_rowconfigure(0, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)

        history_cols = ("data_hora", "status_anterior", "novo_status", "usuario", "observacoes")
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=history_cols,
            show="headings",
            height=6,
            selectmode="none",
        )
        self.history_tree.heading("data_hora", text="Data/Hora")
        self.history_tree.heading("status_anterior", text="Status Anterior")
        self.history_tree.heading("novo_status", text="Novo Status")
        self.history_tree.heading("usuario", text="Usuário")
        self.history_tree.heading("observacoes", text="Observações")

        self.history_tree.column("data_hora", width=160)
        self.history_tree.column("status_anterior", width=140)
        self.history_tree.column("novo_status", width=140)
        self.history_tree.column("usuario", width=120)
        self.history_tree.column("observacoes", width=260)

        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscroll=history_scroll.set)
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        history_scroll.grid(row=0, column=1, sticky="ns")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=12, sticky="e")
        ttk.Button(button_frame, text="Fechar", command=self.window.destroy).grid(row=0, column=0, padx=6)

    def _on_search(self) -> None:
        pedido_id_text = self.id_entry.get().strip()
        if not pedido_id_text:
            messagebox.showwarning("Aviso", "Informe o ID do pedido.", parent=self.window)
            return

        try:
            pedido_id = int(pedido_id_text)
        except ValueError:
            messagebox.showwarning("Aviso", "ID do pedido deve ser um número inteiro.", parent=self.window)
            return

        self._clear_order_display()

        try:
            pedido = self.controller.obter_pedido_por_id(pedido_id)
            self._fill_order_data(pedido)
        except ValueError as error:
            messagebox.showerror("Erro", str(error), parent=self.window)
        except Exception as error:
            messagebox.showerror("Erro", f"Falha ao consultar a API: {error}", parent=self.window)

    def _fill_order_data(self, pedido: dict) -> None:
        self.info_labels["numero"].configure(text=str(pedido.get("numero", "—")))
        self.info_labels["data_criacao"].configure(text=self._format_datetime(pedido.get("data_criacao")))
        self.info_labels["cliente"].configure(text=str(pedido.get("cliente", "—")))
        self.info_labels["status"].configure(text=str(pedido.get("status", "—")))
        self.info_labels["valor_total"].configure(text=self._format_currency(pedido.get("valor_total")))
        self.info_labels["observacoes"].configure(text=str(pedido.get("observacoes", "—")))

        itens = pedido.get("itens") or []
        for item in itens:
            produto = item.get("produto", "—")
            quantidade = item.get("quantidade", "—")
            preco_unitario = self._format_currency(item.get("preco_unitario"))
            subtotal = self._format_currency(item.get("subtotal"))
            self.items_tree.insert("", "end", values=(produto, quantidade, preco_unitario, subtotal))

        historico = pedido.get("historico_status") or []
        for registro in historico:
            data_hora = self._format_datetime(registro.get("data_hora"))
            status_anterior = registro.get("status_anterior", "—")
            novo_status = registro.get("novo_status", "—")
            usuario = registro.get("usuario", "—")
            observacoes = registro.get("observacoes", "—")
            self.history_tree.insert(
                "",
                "end",
                values=(data_hora, status_anterior, novo_status, usuario, observacoes),
            )

    def _clear_order_display(self) -> None:
        for label in self.info_labels.values():
            label.configure(text="—")
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

    def _format_datetime(self, value) -> str:
        if not value:
            return "—"

        if isinstance(value, datetime.datetime):
            dt = value
        else:
            text = str(value)
            try:
                dt = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
            except ValueError:
                try:
                    dt = datetime.datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        dt = datetime.datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        return text
        return dt.strftime("%d-%m-%Y %H:%M")

    def _format_currency(self, value) -> str:
        if value in (None, "", "—"):
            return "R$ 0,00"

        try:
            amount = float(str(value).replace("R$", "").replace("r$", "").replace(" ", "").replace(",", "."))
        except (TypeError, ValueError):
            return str(value)

        integer_part, _, decimal_part = f"{amount:.2f}".partition(".")
        integer_part_with_sep = "".join(
            [
                integer_part[max(i - 3, 0):i] + ("." if i != len(integer_part) else "")
                for i in range(len(integer_part) % 3 or 3, len(integer_part) + 1, 3)
            ]
        )
        return f"R$ {integer_part_with_sep},{decimal_part}"
