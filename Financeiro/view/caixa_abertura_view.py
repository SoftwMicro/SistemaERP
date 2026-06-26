import tkinter as tk
from tkinter import messagebox, ttk

from ..auth_context import get_current_user
from ..repository.caixa_repository import CaixaRepository


class CaixaAberturaView:
    """Janela de abertura de caixa para informar saldo inicial e chamar a API."""

    def __init__(self, owner):
        # owner is TelaInicial instance; use its root as parent
        self.owner = owner
        parent = getattr(owner, "root", owner)
        self.parent = parent
        self.repository = CaixaRepository()
        self.window = tk.Toplevel(parent)
        self.window.title("Abertura de Caixa")
        self.window.resizable(False, False)
        self.window.grab_set()
        self._build_form()

    def _build_form(self) -> None:
        frame = ttk.Frame(self.window, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Saldo Inicial:").grid(row=0, column=0, sticky="w", pady=4)
        self.saldo_entry = ttk.Entry(frame, width=32)
        self.saldo_entry.grid(row=0, column=1, pady=4)
        self.saldo_entry.bind("<Return>", self._on_saldo_focus_out)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=12)

        self.save_button = ttk.Button(button_frame, text="Salvar", command=self._on_save)
        self.save_button.grid(row=0, column=0, padx=6)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).grid(row=0, column=1, padx=6)

    def _on_save(self) -> None:
        saldo_text = self.saldo_entry.get().strip()
        if not saldo_text:
            messagebox.showerror("Erro", "Informe o saldo inicial.", parent=self.window)
            return

        try:
            saldo = self._parse_currency_value(saldo_text)
        except ValueError:
            messagebox.showerror("Erro", "Saldo inicial deve ser um número válido.", parent=self.window)
            return

        # prevenir duplo clique
        try:
            self.save_button.config(state="disabled")
        except Exception:
            pass

        try:
            response = self._send_open_cash_request(saldo)
            messagebox.showinfo(
                "Sucesso",
                f"Caixa aberto com sucesso.\nID: {response.get('id')}\nStatus: {response.get('status')}",
                parent=self.window,
            )
            # Carrega as últimas aberturas e atualiza a grade na tela principal
            try:
                if hasattr(self.owner, "update_caixa_list"):
                    usuario = get_current_user()
                    if usuario and usuario.id:
                        aberturas = self.repository.obter_aberturas_fechamentos(usuario.id)
                        self.owner.update_caixa_list(aberturas)
            except Exception as error:
                messagebox.showerror("Aviso", f"Caixa aberto, mas erro ao atualizar grade: {error}", parent=self.window)
            
            self.window.destroy()
        except ValueError as error:
            messagebox.showerror("Erro", str(error), parent=self.window)
            try:
                self.save_button.config(state="normal")
            except Exception:
                pass
        except Exception as error:
            messagebox.showerror("Erro", f"Falha ao conectar com a API: {error}", parent=self.window)
            try:
                self.save_button.config(state="normal")
            except Exception:
                pass

    def _send_open_cash_request(self, saldo: float) -> dict:
        usuario = get_current_user()
        if usuario is None or usuario.id is None:
            raise ValueError("Usuário não autenticado. Faça login e tente novamente.")

        return self.repository.abrir_caixa(usuario.id, saldo)

    def _on_saldo_focus_out(self, event: tk.Event) -> None:
        text = self.saldo_entry.get().strip()
        if not text:
            return

        try:
            value = self._parse_currency_value(text)
            self.saldo_entry.delete(0, tk.END)
            self.saldo_entry.insert(0, self._format_currency(value))
        except ValueError:
            # keep the entered text if it's not parseable yet
            pass

    def _parse_currency_value(self, text: str) -> float:
        clean = text.replace("R$", "").replace("r$", "")
        clean = clean.replace(" ", "")
        clean = clean.replace(".", "")
        clean = clean.replace(",", ".")

        if not clean or clean == ".":
            raise ValueError("Valor inválido")

        return float(clean)

    def _format_currency(self, value: float) -> str:
        integer_part, _, decimal_part = f"{value:.2f}".partition(".")
        integer_part_with_sep = "".join(
            [integer_part[max(i - 3, 0):i] + ("." if i != len(integer_part) else "")
             for i in range(len(integer_part) % 3 or 3, len(integer_part) + 1, 3)]
        )
        return f"R$ {integer_part_with_sep},{decimal_part}"
