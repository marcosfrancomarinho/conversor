from tkinter import Listbox, StringVar, Tk, messagebox, ttk
from src.application.dto.converter_input_file import ConverterInputFile
from src.application.dto.selector_output_file import SelectorOutputFile
from src.application.usecase.file_converter_usecase import FileConverterUseCase
from src.application.usecase.file_selector_usecase import FileSelectorUseCase
from src.infrastrucure.tk_file_save_location_selector import TKFileSaveLocationSelector
from src.infrastrucure.tk_file_selector import TkFileSelector
from src.infrastrucure.tk_image_converter import TkImageConverter
from src.infrastrucure.tk_pdf_converter import TkPDFConverter
import tkinter as tk
import os

class ConversorImagensApp:

    def __init__(self, root: Tk, file_selector_usecase:FileSelectorUseCase, file_converter_usecase:FileConverterUseCase):
        self.__root = root
        self.__file_selector_usecase = file_selector_usecase
        self.__file_converter_usecase = file_converter_usecase
        self.__list_file: Listbox
        self.__progress: ttk.Progressbar
        self.__format_var: StringVar = tk.StringVar(value="PNG")
        self.__selected_file:list[SelectorOutputFile] = []
        self.__criar_interface()

    # ================= UI =================
    def __criar_interface(self):
        self.__root.title("Conversor de Imagens")
        self.__root.geometry("520x500")
        self.__root.minsize(520, 500)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("TRadiobutton", font=("Segoe UI", 10))
        style.configure("TLabelFrame", font=("Segoe UI", 10, "bold"))
        style.configure("TProgressbar", thickness=12)
        container = ttk.Frame(self.__root, padding=15)
        container.pack(fill="both", expand=True)

        ttk.Button(
            container,
            text="Selecionar Arquivos",
            command=self.selecionar_arquivos
        ).pack(fill="x", pady=(0, 10))

        frame_lista = ttk.Frame(container)
        frame_lista.pack(fill="both", expand=True)

        self.__list_file = tk.Listbox(
            frame_lista,
            height=10,
            selectmode=tk.EXTENDED,
            exportselection=False
        )
        self.__list_file.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, command=self.__list_file.yview) # type: ignore
        scrollbar.pack(side="right", fill="y")
        self.__list_file.config(yscrollcommand=scrollbar.set)

        frame_formato = ttk.LabelFrame(container, text="Formato de Conversão", padding=10)
        frame_formato.pack(fill="x", pady=10)

        ttk.Radiobutton(frame_formato, text="PNG", variable=self.__format_var, value="PNG").pack(side="left", padx=10)
        ttk.Radiobutton(frame_formato, text="JPEG", variable=self.__format_var, value="JPEG").pack(side="left", padx=10)
        ttk.Radiobutton(frame_formato, text="PDF (único arquivo)", variable=self.__format_var, value="PDF").pack(side="left", padx=10)

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

        self.__progress = ttk.Progressbar(
            container,
            orient="horizontal",
            mode="determinate"
        )
        self.__progress.pack(fill="x", pady=10)

    # ================= Ações =================

    def remover_selecionados(self):
        selecionados= list(self.__list_file.curselection()) # type: ignore
        if not selecionados:
            return
        for index in reversed(selecionados): # type: ignore
            self.__list_file.delete(index) # type: ignore
            del self.__selected_file[index]

    def selecionar_arquivos(self):
        self.__selected_file.extend(self.__file_selector_usecase.select())
        self.__list_file.delete(0, tk.END)
        for file in self.__selected_file:
            self.__list_file.insert(tk.END, os.path.basename(file.path))

    def converter_selecionados(self):
        try:
            format = self.__format_var.get()
            self.__progress["maximum"] = len(self.__selected_file)
            self.__progress["value"] = 0
            if not self.__selected_file:
                messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
                return
            input = ConverterInputFile(format, self.__selected_file, self.__update_progress_bar )
            output = self.__file_converter_usecase.converter(input)   
        except Exception as e:
                messagebox.showerror(title="Aviso", message=f"Error: {e}")
                return
        messagebox.showinfo("Concluído", f"{output.quantity} arquivos processados!")

    def __update_progress_bar(self,course:int)->None:
        self.__progress["value"] =  course
        self.__root.update_idletasks()
           
# ================= EXECUÇÃO =================

if __name__ == "__main__":
    root = tk.Tk()
    file_selector = TkFileSelector()
    image_converter = TkImageConverter()
    pdf_converter = TkPDFConverter()
    file_save_location_selector = TKFileSaveLocationSelector()
    file_selector_usecase = FileSelectorUseCase(file_selector)
    file_converter_usecase = FileConverterUseCase(image_converter, pdf_converter, file_save_location_selector)
    ConversorImagensApp(root, file_selector_usecase, file_converter_usecase)
    root.mainloop()