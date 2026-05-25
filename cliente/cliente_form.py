import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_BASE = "http://localhost:8000/api/v1"

# --- Model ---
class ClienteModel:
    def __init__(self, nome, cpf_cnpj, email, telefone, endereco, ativo=True):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.ativo = ativo

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf_cnpj": self.cpf_cnpj,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "ativo": self.ativo
        }

# --- Controller ---
class ClienteController:
    @staticmethod
    def cadastrar_cliente(cliente: ClienteModel):
        resp = requests.post(f"{API_BASE}/customers", json=cliente.to_dict())
        return resp

    @staticmethod
    def listar_clientes():
        resp = requests.get(f"{API_BASE}/customers")
        if resp.status_code == 200:
            return resp.json()
        return []

# --- View ---
class ClienteForm(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        if parent is None:
            self.pack(fill=tk.BOTH, expand=True)
            self.master.title("Cadastro de Cliente")
            self.master.geometry("900x400")
            self.master.resizable(False, False)
        self.create_widgets()
        self.atualizar_grid()

    def create_widgets(self):
        # Labels e Entrys
        ttk.Label(self, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = ttk.Entry(self, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Cpf/Cnpj:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cpf_cnpj_entry = ttk.Entry(self, width=20)
        self.cpf_cnpj_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Telefone:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.telefone_entry = ttk.Entry(self, width=20)
        self.telefone_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(self, text="Endereço:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.endereco_entry = ttk.Entry(self, width=50)
        self.endereco_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        self.ativo_var = tk.BooleanVar(value=True)
        self.ativo_check = ttk.Checkbutton(self, text="Ativo", variable=self.ativo_var)
        self.ativo_check.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botão Salvar
        self.save_btn = ttk.Button(self, text="Salvar", command=self.on_save)
        self.save_btn.grid(row=3, column=3, padx=5, pady=5, sticky="e")

        # Grid de clientes
        columns = ("id", "nome", "cpf_cnpj", "email", "telefone", "endereco", "ativo")
        col_titles = ["ID", "Nome", "Cpf/Cnpj", "Email", "Telefone", "Endereço", "Ativo"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col, title in zip(columns, col_titles):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=120)
        self.tree.grid(row=4, column=0, columnspan=4, padx=5, pady=10, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def on_save(self):
        self.save_btn.config(state=tk.DISABLED, text="Salvando...")
        self.update_idletasks()
        # Validação
        nome = self.nome_entry.get().strip()
        cpf_cnpj = self.cpf_cnpj_entry.get().strip()
        email = self.email_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        endereco = self.endereco_entry.get().strip()
        ativo = self.ativo_var.get()
        if not nome or not cpf_cnpj or not email or not telefone or not endereco:
            messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos.")
            self.save_btn.config(state=tk.NORMAL, text="Salvar")
            return
        cliente = ClienteModel(nome, cpf_cnpj, email, telefone, endereco, ativo)
        try:
            resp = ClienteController.cadastrar_cliente(cliente)
            if resp.status_code in (200, 201):
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                self.atualizar_grid()
                self.limpar_form()
            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar cliente.\nStatus: {resp.status_code}\nResposta: {resp.text}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")
        self.save_btn.config(state=tk.NORMAL, text="Salvar")

    def atualizar_grid(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            clientes = ClienteController.listar_clientes()
            for cli in clientes:
                self.tree.insert("", "end", values=(cli.get("id", ""), cli.get("nome", ""), cli.get("cpf_cnpj", ""), cli.get("email", ""), cli.get("telefone", ""), cli.get("endereco", ""), "Sim" if cli.get("ativo", True) else "Não"))
        except Exception as e:
            messagebox.showerror("Erro ao carregar clientes", str(e))

    def limpar_form(self):
        self.nome_entry.delete(0, tk.END)
        self.cpf_cnpj_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)
        self.ativo_var.set(True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteForm(root)
    root.mainloop()
