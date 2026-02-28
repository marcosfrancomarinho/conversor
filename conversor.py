import tkinter as tk
from tkinter import Listbox, StringVar, Tk, filedialog, messagebox, ttk
from PIL import Image, UnidentifiedImageError
import os


class ConversorImagensApp:

    def __init__(self, root: Tk):
        self.root = root
        self.lista_arquivos: Listbox
        self.progresso: ttk.Progressbar
        self.formato_var: StringVar = tk.StringVar(value="PNG")
        self.arquivos_selecionados = []

        self.root.title("Conversor de Imagens")
        self.root.geometry("520x500")
        self.root.minsize(520, 500)

        self._criar_interface()

    # ================= UI =================

    def _criar_interface(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("TRadiobutton", font=("Segoe UI", 10))
        style.configure("TLabelFrame", font=("Segoe UI", 10, "bold"))
        style.configure("TProgressbar", thickness=12)

        container = ttk.Frame(self.root, padding=15)
        container.pack(fill="both", expand=True)

        ttk.Button(
            container,
            text="Selecionar Arquivos",
            command=self.selecionar_arquivos
        ).pack(fill="x", pady=(0, 10))

        frame_lista = ttk.Frame(container)
        frame_lista.pack(fill="both", expand=True)

        self.lista_arquivos = tk.Listbox(
            frame_lista,
            height=10,
            selectmode=tk.EXTENDED,
            exportselection=False
        )
        self.lista_arquivos.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, command=self.lista_arquivos.yview) # type: ignore
        scrollbar.pack(side="right", fill="y")
        self.lista_arquivos.config(yscrollcommand=scrollbar.set)

        frame_formato = ttk.LabelFrame(container, text="Formato de Conversão", padding=10)
        frame_formato.pack(fill="x", pady=10)

        ttk.Radiobutton(frame_formato, text="PNG", variable=self.formato_var, value="PNG").pack(side="left", padx=10)
        ttk.Radiobutton(frame_formato, text="JPEG", variable=self.formato_var, value="JPEG").pack(side="left", padx=10)
        ttk.Radiobutton(frame_formato, text="PDF (único arquivo)", variable=self.formato_var, value="PDF").pack(side="left", padx=10)

        frame_botoes = ttk.Frame(container)
        frame_botoes.pack(fill="x", pady=5)

        ttk.Button(
            frame_botoes,
            text="Converter",
            command=self.converter_selecionados
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            frame_botoes,
            text="Remover Selecionado",
            command=self.remover_selecionados
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.progresso = ttk.Progressbar(
            container,
            orient="horizontal",
            mode="determinate"
        )
        self.progresso.pack(fill="x", pady=10)

    # ================= Ações =================

    def remover_selecionados(self):
        selecionados= list(self.lista_arquivos.curselection()) # type: ignore
        if not selecionados:
            return

        for index in reversed(selecionados): # type: ignore
            self.lista_arquivos.delete(index) # type: ignore
            del self.arquivos_selecionados[index]

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos",
            filetypes=[("Todos os arquivos", "*")]
        )

        self.arquivos_selecionados = list(arquivos)
        self.lista_arquivos.delete(0, tk.END)

        for file in self.arquivos_selecionados:
            self.lista_arquivos.insert(tk.END, os.path.basename(file))

    def escolher_pasta_saida(self):
        if self.formato_var.get() == "PDF":
            return filedialog.asksaveasfilename(
            title="Salvar PDF como",
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf")],
        )
        return filedialog.askdirectory(title="Escolha a pasta de destino")

    def converter_selecionados(self):
        formato = self.formato_var.get()
        
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
    
        pasta_saida = self.escolher_pasta_saida()
            
        if not pasta_saida:
            return


        self.progresso["maximum"] = len(self.arquivos_selecionados)
        self.progresso["value"] = 0

        imagens_pdf: list[Image.Image] = []
        convertidos = 0

        for i, caminho in enumerate(self.arquivos_selecionados):
            try:
                with Image.open(caminho) as img:
                    img.load()

                    nome_base = os.path.splitext(os.path.basename(caminho))[0]
                    if not nome_base:
                        nome_base = f"arquivo_{i+1}"

                    if formato == "PNG":
                        destino = os.path.join(pasta_saida, f"{nome_base}_{i+1}" + ".png")
                        img.convert("RGBA").save(destino, format="PNG")
                        convertidos += 1

                    elif formato == "JPEG":
                        destino = os.path.join(pasta_saida, f"{nome_base}_{i+1}" + ".jpg")
                        img.convert("RGB").save(destino, format="JPEG")
                        convertidos += 1

                    elif formato == "PDF":
                        imagens_pdf.append(img.convert("RGB").copy())

            except UnidentifiedImageError:
                messagebox.showerror(title="Aviso", message=f"Ignorado (não é imagem válida): {caminho}")
                return
            except Exception as e:
                messagebox.showerror(title="Aviso", message=f"Erro em {caminho}: {e}")
                return

            self.progresso["value"] = i + 1
            self.root.update_idletasks()

        if formato == "PDF" and imagens_pdf:
            self._salvar_pdf(imagens_pdf, pasta_saida)
            convertidos = len(imagens_pdf)

        messagebox.showinfo("Concluído", f"{convertidos} arquivos processados!")

    def _salvar_pdf(self, imagens: list[Image.Image], pasta_saida: str):
        imagens[0].save(
            pasta_saida,
            save_all=True,
            append_images=imagens[1:]
        )


# ================= EXECUÇÃO =================

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorImagensApp(root)
    root.mainloop()