import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from pymongo import MongoClient

class SistemaOcorrencias:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['ouvidoria']
        self.collection = self.db['ocorrencias']

    def exibir_ocorrencias(self):
        ocorrencias = self.collection.find()
        return [{"nome": o["nome"], "tipo": o["tipo"], "descricao": o["descricao"]} for o in ocorrencias]

    def adicionar_ocorrencia(self, nome, tipo, descricao):
        ocorrencia = {"nome": nome, "tipo": tipo, "descricao": descricao}
        self.collection.insert_one(ocorrencia)

    def exibir_ocorrencias_por_tipo(self, tipo):
        ocorrencias = self.collection.find({"tipo": tipo})
        return [{"nome": o["nome"], "tipo": o["tipo"], "descricao": o["descricao"]} for o in ocorrencias]

    def excluir_todas_ocorrencias(self):
        self.collection.delete_many({})

    def excluir_ocorrencia_por_nome(self, nome):
        self.collection.delete_one({"nome": nome})

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.nome = None
        self.descricao = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Digite seu nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = ttk.Entry(master)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
        self.descricao_entry = ttk.Entry(master)
        self.descricao_entry.grid(row=1, column=1, padx=5, pady=5)
        return self.nome_entry  # initial focus

    def apply(self):
        self.nome = self.nome_entry.get()
        self.descricao = self.descricao_entry.get()

    def get_values(self):
        return self.nome, self.descricao

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
        self.logo_img = self.logo_img.resize((100, 100), Image.ANTIALIAS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = ttk.Label(self.header_frame, image=self.logo_photo, style="Header.TLabel")
        self.logo_label.pack()

        self.university_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        self.university_frame.pack()

        self.uni_label = ttk.Label(self.university_frame, text="UNIFACISA", font=("Helvetica", 16), foreground="white", style="Header.TLabel")
        self.uni_label.pack(side="left")

        self.title_label = ttk.Label(self.header_frame, text="SISTEMA DE OUVIDORIA", font=("Helvetica", 14), foreground="white", style="Header.TLabel")
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

        self.elogio_img = Image.open("images/elogio.png").resize((50, 50), Image.ANTIALIAS)
        self.elogio_photo = ImageTk.PhotoImage(self.elogio_img)
        self.critica_img = Image.open("images/critica.png").resize((50, 50), Image.ANTIALIAS)
        self.critica_photo = ImageTk.PhotoImage(self.critica_img)
        self.sugestao_img = Image.open("images/sugestao.png").resize((50, 50), Image.ANTIALIAS)
        self.sugestao_photo = ImageTk.PhotoImage(self.sugestao_img)

        self.elogio_btn = ttk.Button(self.button_frame, text="ELOGIO", image=self.elogio_photo, compound="top", command=lambda: self.adicionar_ocorrencia("ELOGIO"), style="TButton")
        self.elogio_btn.grid(row=0, column=0, padx=10, pady=10)

        self.critica_btn = ttk.Button(self.button_frame, text="CRÍTICA", image=self.critica_photo, compound="top", command=lambda: self.adicionar_ocorrencia("CRÍTICA"), style="TButton")
        self.critica_btn.grid(row=0, column=1, padx=10, pady=10)

        self.sugestao_btn = ttk.Button(self.button_frame, text="SUGESTÃO", image=self.sugestao_photo, compound="top", command=lambda: self.adicionar_ocorrencia("SUGESTÃO"), style="TButton")
        self.sugestao_btn.grid(row=0, column=2, padx=10, pady=10)

        self.listar_btn = ttk.Button(self.button_frame, text="Listar todas as ocorrências", command=self.listar_ocorrencias, style="TButton")
        self.listar_btn.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.exibir_usuario_btn = ttk.Button(self.button_frame, text="Exibir ocorrências de um usuário", command=self.exibir_por_usuario, style="TButton")
        self.exibir_usuario_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Frame para o botão de sair no canto inferior direito
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
        nome, descricao = dialog.get_values()

        if nome and descricao:
            self.sistema.adicionar_ocorrencia(nome, tipo, descricao)
            messagebox.showinfo("Sucesso", f"{tipo} adicionada com sucesso.")

    def exibir_por_usuario(self):
        tipo = self.input_dialog("Exibir Ocorrências de um Usuário", "Digite o tipo (crítica, elogio ou sugestão):")
        if tipo:
            ocorrencias = self.sistema.exibir_ocorrencias_por_tipo(tipo)
            self.mostrar_ocorrencias(ocorrencias)

    def excluir_todas(self):
        self.sistema.excluir_todas_ocorrencias()
        messagebox.showinfo("Sucesso", "Todas as ocorrências foram excluídas.")

    def excluir_por_nome(self):
        nome = self.input_dialog("Excluir Ocorrência", "Digite o nome da ocorrência a ser excluída:")
        if nome:
            self.sistema.excluir_ocorrencia_por_nome(nome)
            messagebox.showinfo("Sucesso", f"Ocorrência '{nome}' foi excluída.")

    def input_dialog(self, title, prompt):
        input_value = simpledialog.askstring(title, prompt)
        return input_value

    def mostrar_ocorrencias(self, ocorrencias):
        ocorrencias_text = "\n".join([f"Nome: {o['nome']}, Tipo: {o['tipo']}, Descrição: {o['descricao']}" for o in ocorrencias])
        ocorrencias_lista = "\n".join([f"{o['nome']} - {o['tipo']} - {o['descricao']}" for o in ocorrencias])
        ocorrencias_janelas = ocorrencias_lista.split('\n')
        ocorrencias_columns = [ocorrencias_janelas[i:i+3] for i in range(0, len(ocorrencias_janelas), 3)]
        
        ocorrencias_text = "\n\n".join(["\n".join(column) for column in ocorrencias_columns])
        messagebox.showinfo("Ocorrências", ocorrencias_text if ocorrencias_text else "Nenhuma ocorrência encontrada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OuvidoriaApp(root)
    root.mainloop()
