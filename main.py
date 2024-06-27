from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

class SistemaOcorrencias:
    def __init__(self):
        self.ocorrencias = []

    def adicionar_ocorrencia(self, cpf, tipo, descricao):
        self.ocorrencias.append({'cpf': cpf, 'tipo': tipo, 'descricao': descricao})

    def exibir_ocorrencias(self):
        return self.ocorrencias

    def exibir_ocorrencias_por_cpf(self, cpf):
        return [o for o in self.ocorrencias if o['cpf'] == cpf]

    def excluir_ocorrencia_por_cpf(self, cpf):
        self.ocorrencias = [o for o in self.ocorrencias if o['cpf'] != cpf]

    def excluir_todas_ocorrencias(self):
        self.ocorrencias = []

    def atualizar_ocorrencia(self, cpf, tipo, descricao):
        for o in self.ocorrencias:
            if o['cpf'] == cpf:
                o['tipo'] = tipo
                o['descricao'] = descricao
                return

    def exibir_ocorrencias_por_tipo(self, tipo):
        return [o for o in self.ocorrencias if o['tipo'] == tipo]

class OuvidoriaApp:
    def __init__(self, root):
        self.sistema = SistemaOcorrencias()
        self.root = root
        self.root.title("UNIFACISA")

        # Definindo o ícone da aplicação na barra de tarefas
        self.root.iconbitmap('images/facisaicon.ico')

        # Configurar fundo sólido azul escuro
        self.root.configure(bg='dark blue')

        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = ttk.Frame(self.root, style="Header.TFrame")
        self.header_frame.pack(pady=10)

        # Logotipo da FACISA
        self.logo_img = Image.open("images/Facisa.png")
        self.logo_img = self.logo_img.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = ttk.Label(self.header_frame, image=self.logo_photo, style="Header.TLabel")
        self.logo_label.pack()

        self.university_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        self.university_frame.pack()

        self.uni_label = ttk.Label(self.university_frame, text="FACISA", font=("Helvetica", 16), foreground="white", style="Header.TLabel")
        self.uni_label.pack(side="left")

        self.title_label = ttk.Label(self.header_frame, text="Sistema de Ouvidoria", font=("Helvetica", 14), foreground="white", style="Header.TLabel")
        self.title_label.pack()

        # Botões do MENU - configuração
        self.button_frame = ttk.Frame(self.root, style="Menu.TFrame")
        self.button_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton",
                        font=("Helvetica", 12),
                        padding=10)

        style.configure("Header.TFrame", background="dark blue")
        style.configure("Header.TLabel", background="dark blue", foreground="white")
        style.configure("Menu.TFrame", background="dark blue")

        style.map("TButton",
                  background=[('active', '#0052cc'), ('!active', 'white')],
                  foreground=[('active', 'white'), ('!active', 'black')])

        # Ícones dos botões

        self.elogio_img = Image.open("images/elogio.png").resize((50, 50), Image.LANCZOS)
        self.elogio_photo = ImageTk.PhotoImage(self.elogio_img)

        self.critica_img = Image.open("images/critica.png").resize((50, 50), Image.LANCZOS)
        self.critica_photo = ImageTk.PhotoImage(self.critica_img)

        self.sugestao_img = Image.open("images/sugestao.png").resize((50, 50), Image.LANCZOS)
        self.sugestao_photo = ImageTk.PhotoImage(self.sugestao_img)

        self.exibir_usuario_img = Image.open("images/listauser.png").resize((50, 50), Image.LANCZOS)
        self.exibir_usuario_photo = ImageTk.PhotoImage(self.exibir_usuario_img)

        self.excluir_todas_img = Image.open("images/deletarTODOSS.png").resize((50, 50), Image.LANCZOS)
        self.excluir_todas_photo = ImageTk.PhotoImage(self.excluir_todas_img)

        self.excluir_por_cpf_img = Image.open("images/deletarCPF.png").resize((50, 50), Image.LANCZOS)
        self.excluir_por_cpf_photo = ImageTk.PhotoImage(self.excluir_por_cpf_img)

        self.atualizar_img = Image.open("images/atualizar.png").resize((50, 50), Image.LANCZOS)
        self.atualizar_photo = ImageTk.PhotoImage(self.atualizar_img)

        self.exibir_tipo_img = Image.open("images/exibirPORtipo.png").resize((50, 50), Image.LANCZOS)
        self.exibir_tipo_photo = ImageTk.PhotoImage(self.exibir_tipo_img)

        self.listar_img = Image.open("images/listaTODOS.png").resize((50, 50), Image.LANCZOS)
        self.listar_photo = ImageTk.PhotoImage(self.listar_img)

        #Botões

        botoes = [
            ("Elogio", self.elogio_photo, lambda: self.adicionar_ocorrencia("ELOGIO")),
            ("Crítica", self.critica_photo, lambda: self.adicionar_ocorrencia("CRÍTICA")),
            ("Sugestão", self.sugestao_photo, lambda: self.adicionar_ocorrencia("SUGESTÃO")),
            ("Listar", self.listar_photo, self.listar_ocorrencias),
            ("Exibir por CPF", self.exibir_usuario_photo, self.exibir_por_cpf),
            ("Excluir Todas", self.excluir_todas_photo, self.excluir_todas),
            ("Excluir por CPF", self.excluir_por_cpf_photo, self.excluir_por_cpf),
            ("Atualizar", self.atualizar_photo, self.atualizar_ocorrencia),
            ("Exibir por Tipo", self.exibir_tipo_photo, self.exibir_por_tipo)
        ]

        #Organizacao da grade!
        for i, (text, image, command) in enumerate(botoes):
            row = i // 3
            col = i % 3
            button = ttk.Button(self.button_frame, text=text, image=image, compound="top", command=command, style="TButton")
            button.grid(row=row, column=col, padx=10, pady=10)

        # Botão de SAIR do programa!
        self.exit_frame = ttk.Frame(self.root, style="Menu.TFrame")
        self.exit_frame.pack(side="bottom", anchor="e", padx=10, pady=10)

        self.sair_btn = ttk.Button(self.exit_frame, text="Sair", command=self.root.quit, style="TButton")
        self.sair_btn.pack()

        # Adicionar eventos de mudança de cor nos botões
        for btn in self.button_frame.winfo_children():
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        e.widget.config(background='#0052cc', foreground='white')

    def on_leave(self, e):
        e.widget.config(background='white', foreground='black')

    def listar_ocorrencias(self):
        ocorrencias = self.sistema.exibir_ocorrencias()
        self.mostrar_ocorrencias(ocorrencias)

    def adicionar_ocorrencia(self, tipo):
        dialog = CustomDialog(self.root, f"Adicionar {tipo}")
        cpf, descricao = dialog.get_values()

        if cpf and descricao:
            try:
                self.sistema.adicionar_ocorrencia(cpf, tipo, descricao)
                messagebox.showinfo("Sucesso", f"{tipo} adicionada com sucesso.")
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def exibir_por_cpf(self):
        cpf = self.input_dialog("Exibir Ocorrências por CPF", "Digite um CPF:")
        if cpf:
            ocorrencias = self.sistema.exibir_ocorrencias_por_cpf(cpf)
            self.mostrar_ocorrencias(ocorrencias)

    def excluir_todas(self):
        self.sistema.excluir_todas_ocorrencias()
        messagebox.showinfo("Sucesso", "Todas as ocorrências foram excluídas.")

    def excluir_por_cpf(self):
        cpf = self.input_dialog("Excluir Ocorrência", "Digite o CPF da ocorrência a ser excluída:")
        if cpf:
            self.sistema.excluir_ocorrencia_por_cpf(cpf)
            messagebox.showinfo("Sucesso", f"Ocorrência do CPF {cpf} foi excluída.")

    def atualizar_ocorrencia(self):
        cpf = self.input_dialog("Atualizar Ocorrência", "Digite o CPF da ocorrência a ser atualizada:")
        if cpf:
            dialog = CustomDialog(self.root, "Atualizar Ocorrência")
            _, descricao = dialog.get_values()

            if descricao:
                self.sistema.atualizar_ocorrencia(cpf, descricao)
                messagebox.showinfo("Sucesso", f"Ocorrência do CPF {cpf} foi atualizada.")

    def exibir_por_tipo(self):
        tipo = self.input_dialog("Exibir Ocorrências por Tipo", "Digite o tipo de ocorrência a ser exibida:")
        if tipo:
            ocorrencias = self.sistema.exibir_ocorrencias_por_tipo(tipo)
            self.mostrar_ocorrencias(ocorrencias)

    def input_dialog(self, title, prompt):
        input_value = simpledialog.askstring(title, prompt)
        return input_value

    def mostrar_ocorrencias(self, ocorrencias):
        if ocorrencias:
            ocorrencias_text = "\n\n".join([f"CPF: {o['cpf']}, Tipo: {o['tipo']}, Descrição: {o['descricao']}" for o in ocorrencias])
        else:
            ocorrencias_text = "Nenhuma ocorrência encontrada."
        messagebox.showinfo("Ocorrências", ocorrencias_text)


class CustomDialog:
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.dialog = Toplevel(parent)
        self.dialog.title(title)

        self.create_widgets()

    def create_widgets(self):
        self.cpf_label = Label(self.dialog, text="CPF:")
        self.cpf_label.grid(row=0, column=0, padx=10, pady=10)
        self.cpf_entry = Entry(self.dialog)
        self.cpf_entry.grid(row=0, column=1, padx=10, pady=10)

        self.descricao_label = Label(self.dialog, text="Descrição:")
        self.descricao_label.grid(row=1, column=0, padx=10, pady=10)
        self.descricao_entry = Entry(self.dialog)
        self.descricao_entry.grid(row=1, column=1, padx=10, pady=10)

        self.confirm_button = Button(self.dialog, text="Confirmar", command=self.dialog_ok)
        self.confirm_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def dialog_ok(self):
        self.dialog.destroy()

    def get_values(self):
        self.parent.wait_window(self.dialog)
        return self.cpf_entry.get(), self.descricao_entry.get()


if __name__ == "__main__":
    root = Tk()
    app = OuvidoriaApp(root)
    root.mainloop()