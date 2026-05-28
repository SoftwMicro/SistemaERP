import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import json
from styles.theme import AppTheme

API_BASE = "http://localhost:8000/api/v1"

class OrderListForm(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = AppTheme(self)
        self.parent = parent
        if parent is None:
            self.pack(fill=tk.BOTH, expand=True)
            self.master.title("Gerenciar Pedidos")
            self.master.geometry("1200x600")
            self.master.resizable(True, True)
           

        self.create_widgets()
        self.carregar_pedidos()

    def create_widgets(self):
        # Grid de pedidos
        columns = ("numero", "data_criacao", "cliente", "status", "valor_total", "observacoes")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        col_titles = ["Número", "Data Criação", "Cliente", "Status", "Valor Total", "Observações"]
        for col, title in zip(columns, col_titles):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=150)
        self.tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=4, sticky="ns")

        # Botões de ação
        self.btn_confirmar = ttk.Button(self, text="Confirmar Pedido", command=lambda: self.alterar_status("CONFIRMADO"), style="Confirmar.TButton")
        self.btn_confirmar.grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.btn_separado = ttk.Button(self, text="Separa Pedido", command=lambda: self.alterar_status("SEPARADO"))
        self.btn_separado.grid(row=1, column=1, padx=5, pady=10, sticky="e")
        self.btn_enviado = ttk.Button(self, text="Enviar Pedido", command=lambda: self.alterar_status("ENVIADO"))
        self.btn_enviado.grid(row=1, column=2, padx=5, pady=10, sticky="e")
        self.btn_entregar = ttk.Button(self, text="Entregar Pedido", command=lambda: self.alterar_status("ENTREGUE"), style="Entregue.TButton")
        self.btn_entregar.grid(row=1, column=3, padx=5, pady=10, sticky="e")
        
        self.btn_cancelar = ttk.Button(self, text="Cancelar Pedido", command=lambda: self.alterar_status("CANCELADO"), style="Cancelar.TButton")
        self.btn_cancelar.grid(row=1, column=4, padx=5, pady=10, sticky="e")
        self.btn_deletar = ttk.Button(self, text="Deletar Pedido", command=self.deletar_pedido)
        self.btn_deletar.grid(row=1, column=5, padx=5, pady=10, sticky="e")
       


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def carregar_pedidos(self):
        self.tree.delete(*self.tree.get_children())
        try:
            resp = requests.get(f"{API_BASE}/orders")
            if resp.status_code == 200:
                pedidos = resp.json()
                for pedido in pedidos:
                    data_criacao = pedido.get("data_criacao")
                    if data_criacao:
                        try:
                            # Tenta converter do formato ISO para dd/MM/yyyy
                            data_criacao = datetime.fromisoformat(data_criacao).strftime("%d/%m/%Y")
                        except Exception:
                            pass
                    valor_total = pedido.get("valor_total")
                    # Formatar como moeda Real
                    if valor_total is not None:
                        try:
                            valor_total = float(valor_total)
                            valor_total = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        except Exception:
                            valor_total = pedido.get("valor_total")
                    self.tree.insert("", "end", values=(
                        pedido.get("numero"),
                        data_criacao,
                        pedido.get("cliente"),
                        pedido.get("status"),
                        valor_total,
                        pedido.get("observacoes", "")
                    ))
            else:
                messagebox.showerror("Erro", f"Erro ao carregar pedidos: {resp.status_code}\n{resp.text}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")

    def get_pedido_selecionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um pedido na lista.")
            return None
        values = self.tree.item(selected[0])['values']
        return values[0]  # numero do pedido

    def alterar_status(self, novo_status):
        numero = self.get_pedido_selecionado()
        if not numero:
            return
        
        # Criamos textos dinâmicos para a mensagem dependendo do status
        acao = novo_status.lower() # "confirmado", "entregue", "cancelado"
        
        if not messagebox.askyesno("Confirmação", f"Deseja alterar o status do pedido {numero} para {novo_status}?"):
            return
            
        payload = {
            "status": novo_status,
            "usuario": "sistema",
            "observacoes": f"Atualizado para {acao} via interface"
        }
        
        try:
            resp = requests.patch(f"{API_BASE}/orders/{numero}/status", json=payload)
            if resp.status_code in (200, 201, 204): # Adicionado 204 que também é comum em PATCH
                messagebox.showinfo("Sucesso", f"Pedido {numero} atualizado para {novo_status}!")
                self.carregar_pedidos()
            else:
                messagebox.showerror("Erro", f"Erro ao atualizar pedido: {resp.status_code}\n{resp.text}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")

    def deletar_pedido(self):
        numero = self.get_pedido_selecionado()
        if not numero:
            return
        if not messagebox.askyesno("Confirmação", f"Deseja deletar o pedido {numero}?"):
            return
        try:
            resp = requests.delete(f"{API_BASE}/orders/{numero}")
            if resp.status_code in (200, 204):
                messagebox.showinfo("Sucesso", f"Pedido {numero} deletado!")
                self.carregar_pedidos()
            else:
                messagebox.showerror("Erro", f"Erro ao deletar pedido: {resp.status_code}\n{resp.text}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderListForm(root)
    root.mainloop()
