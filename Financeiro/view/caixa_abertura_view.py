import json
import os
import urllib.error
import urllib.parse
import urllib.request
import tkinter as tk
from tkinter import messagebox, ttk

from ..auth_context import get_current_user


class CaixaAberturaView:
    """Janela de abertura de caixa para informar saldo inicial e chamar a API."""

    API_URL = os.getenv("FINANCEIRO_API_URL", "http://localhost:8080/caixa/abrir")

    def __init__(self, owner):
        # owner is TelaInicial instance; use its root as parent
        self.owner = owner
        parent = getattr(owner, "root", owner)
        self.parent = parent
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
            saldo = float(saldo_text.replace(",", "."))
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
            # atualiza a grade na tela principal
            try:
                if hasattr(self.owner, "update_caixa"):
                    self.owner.update_caixa(response)
            except Exception:
                pass
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

        form = {
            "usuarioId": str(usuario.id),
            "saldoInicial": str(saldo),
        }
        data = urllib.parse.urlencode(form).encode("utf-8")
        request = urllib.request.Request(
            self.API_URL,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="ignore").strip()
            details = error_body or str(error.reason) or "Sem corpo de erro"
            raise ValueError(
                f"API retornou erro {error.code} {error.reason}: {details}"
            ) from error
        except urllib.error.URLError as error:
            raise ConnectionError(f"Não foi possível acessar a API: {error.reason}") from error
        except json.JSONDecodeError as error:
            raise ValueError(f"Resposta da API inválida: {body}") from error
