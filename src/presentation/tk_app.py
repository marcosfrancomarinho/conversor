import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path as SystemPath
from tkinter import Listbox, StringVar, Tk, messagebox, ttk

from src.application.dto.converter_input_file import ConverterInputFile
from src.application.dto.selector_output_file import SelectorOutputFile
from src.application.usecase.file_converter_usecase import FileConverterUseCase
from src.application.usecase.file_selector_usecase import FileSelectorUseCase
from src.domain.gateway.file_save_location_selector import FileSaveLocationSelector
from src.domain.valuesobject.type import Type


class ConverterApp:
    def __init__(
        self,
        root: Tk,
        file_selector_usecase: FileSelectorUseCase,
        file_converter_usecase: FileConverterUseCase,
        save_location_selector: FileSaveLocationSelector,
    ) -> None:
        self.__root = root
        self.__file_selector_usecase = file_selector_usecase
        self.__file_converter_usecase = file_converter_usecase
        self.__save_location_selector = save_location_selector

        self.__selected_files: list[SelectorOutputFile] = []
        self.__format_var = StringVar(value="PDF")
        self.__destination_var = StringVar(value="Selecione arquivos para definir o destino.")
        self.__count_var = StringVar(value="0 arquivos selecionados")
        self.__destination_customized = False

        self.__list_file: Listbox
        self.__progress: ttk.Progressbar

        self.__create_interface()

    def __create_interface(self) -> None:
        self.__root.title("Conversor de Arquivos")
        self.__root.geometry("700x610")
        self.__root.minsize(620, 560)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=7, font=("Segoe UI", 10))
        style.configure("TRadiobutton", font=("Segoe UI", 10))
        style.configure("TLabelFrame", font=("Segoe UI", 10, "bold"))
        style.configure("TProgressbar", thickness=12)

        container = ttk.Frame(self.__root, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Button(
            container,
            text="Selecionar arquivos",
            command=self.select_files,
        ).pack(fill="x", pady=(0, 8))

        ttk.Label(container, textvariable=self.__count_var).pack(anchor="w", pady=(0, 5))

        list_container = ttk.Frame(container)
        list_container.pack(fill="both", expand=True)

        self.__list_file = tk.Listbox(
            list_container,
            height=12,
            selectmode=tk.EXTENDED,
            exportselection=False,
        )
        self.__list_file.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_container, command=self.__list_file.yview)
        scrollbar.pack(side="left", fill="y")
        self.__list_file.config(yscrollcommand=scrollbar.set)

        order_buttons = ttk.Frame(list_container)
        order_buttons.pack(side="left", fill="y", padx=(8, 0))

        ttk.Button(order_buttons, text="↑", width=4, command=self.move_up).pack(pady=(0, 5))
        ttk.Button(order_buttons, text="↓", width=4, command=self.move_down).pack(pady=(0, 5))
        ttk.Button(order_buttons, text="Remover", command=self.remove_selected).pack(pady=(10, 5))
        ttk.Button(order_buttons, text="Limpar", command=self.clear_files).pack()

        frame_format = ttk.LabelFrame(container, text="Formato de saída", padding=10)
        frame_format.pack(fill="x", pady=10)

        for text, value in (
            ("PNG", "PNG"),
            ("JPEG", "JPEG"),
            ("PDF único", "PDF"),
        ):
            ttk.Radiobutton(
                frame_format,
                text=text,
                variable=self.__format_var,
                value=value,
                command=self.__on_format_change,
            ).pack(side="left", padx=10)

        destination_frame = ttk.LabelFrame(container, text="Destino", padding=10)
        destination_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            destination_frame,
            textvariable=self.__destination_var,
            wraplength=550,
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            destination_frame,
            text="Alterar...",
            command=self.change_destination,
        ).pack(side="right", padx=(10, 0))

        ttk.Label(
            container,
            text=(
                "O destino acima é usado automaticamente. "
                "Só clique em “Alterar...” se quiser salvar em outro local."
            ),
        ).pack(anchor="w", pady=(0, 8))

        frame_buttons = ttk.Frame(container)
        frame_buttons.pack(fill="x", pady=5)

        ttk.Button(
            frame_buttons,
            text="Converter",
            command=self.convert_selected,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            frame_buttons,
            text="Abrir destino",
            command=self.open_destination,
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.__progress = ttk.Progressbar(
            container,
            orient="horizontal",
            mode="determinate",
        )
        self.__progress.pack(fill="x", pady=(10, 0))

    def select_files(self) -> None:
        selected = self.__file_selector_usecase.select()
        if not selected:
            return

        existing_paths = {file.path for file in self.__selected_files}
        for file in selected:
            if file.path not in existing_paths:
                self.__selected_files.append(file)
                existing_paths.add(file.path)

        self.__destination_customized = False
        self.__refresh_file_list()
        self.__update_default_destination()

    def remove_selected(self) -> None:
        selected_indexes = list(self.__list_file.curselection())
        if not selected_indexes:
            return

        for index in reversed(selected_indexes):
            del self.__selected_files[index]

        self.__destination_customized = False
        self.__refresh_file_list()
        self.__update_default_destination()

    def clear_files(self) -> None:
        self.__selected_files.clear()
        self.__destination_customized = False
        self.__refresh_file_list()
        self.__update_default_destination()

    def move_up(self) -> None:
        indexes = list(self.__list_file.curselection())
        if not indexes or indexes[0] == 0:
            return

        for index in indexes:
            self.__selected_files[index - 1], self.__selected_files[index] = (
                self.__selected_files[index],
                self.__selected_files[index - 1],
            )

        self.__refresh_file_list()
        for index in indexes:
            self.__list_file.selection_set(index - 1)

    def move_down(self) -> None:
        indexes = list(self.__list_file.curselection())
        if not indexes or indexes[-1] == len(self.__selected_files) - 1:
            return

        for index in reversed(indexes):
            self.__selected_files[index + 1], self.__selected_files[index] = (
                self.__selected_files[index],
                self.__selected_files[index + 1],
            )

        self.__refresh_file_list()
        for index in indexes:
            self.__list_file.selection_set(index + 1)

    def change_destination(self) -> None:
        if not self.__selected_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo primeiro.")
            return

        suggested = self.__get_destination()
        selected = self.__save_location_selector.select(
            Type(self.__format_var.get()),
            suggested,
        )

        if selected:
            self.__destination_var.set(selected)
            self.__destination_customized = True

    def convert_selected(self) -> None:
        if not self.__selected_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return

        output_path = self.__get_destination()
        self.__progress["maximum"] = len(self.__selected_files)
        self.__progress["value"] = 0

        try:
            input_data = ConverterInputFile(
                output_type=self.__format_var.get(),
                files_input=self.__selected_files,
                output_path=output_path,
                progress=self.__update_progress_bar,
            )
            output = self.__file_converter_usecase.converter(input_data)
        except Exception as error:
            messagebox.showerror("Erro", str(error))
            return

        if self.__format_var.get() == "PDF":
            message = (
                f"PDF criado com {output.quantity} arquivo(s) de entrada.\n\n"
                f"Salvo em:\n{output.output_path}"
            )
        else:
            message = (
                f"{output.quantity} arquivo(s) convertido(s).\n\n"
                f"Salvos em:\n{output.output_path}"
            )

        messagebox.showinfo("Concluído", message)

    def open_destination(self) -> None:
        if not self.__selected_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo primeiro.")
            return

        destination = self.__get_destination()
        target = destination

        if self.__format_var.get() == "PDF":
            target = os.path.dirname(destination)

        if not target:
            return

        os.makedirs(target, exist_ok=True)
        self.__open_path(target)

    def __on_format_change(self) -> None:
        self.__destination_customized = False
        self.__update_default_destination()

    def __refresh_file_list(self) -> None:
        self.__list_file.delete(0, tk.END)
        for file in self.__selected_files:
            self.__list_file.insert(tk.END, os.path.basename(file.path))

        quantity = len(self.__selected_files)
        suffix = "arquivo selecionado" if quantity == 1 else "arquivos selecionados"
        self.__count_var.set(f"{quantity} {suffix}")

    def __update_default_destination(self) -> None:
        if self.__destination_customized:
            return

        if not self.__selected_files:
            self.__destination_var.set("Selecione arquivos para definir o destino.")
            return

        first_file = SystemPath(self.__selected_files[0].path)
        if self.__format_var.get() == "PDF":
            candidate = first_file.parent / f"{first_file.stem}_convertido.pdf"
            destination = self.__next_available_pdf_path(candidate)
        else:
            destination = first_file.parent / "convertidos"

        self.__destination_var.set(str(destination))

    @staticmethod
    def __next_available_pdf_path(candidate: SystemPath) -> SystemPath:
        if not candidate.exists():
            return candidate

        index = 2
        while True:
            alternative = candidate.with_name(
                f"{candidate.stem}_{index}{candidate.suffix}"
            )
            if not alternative.exists():
                return alternative
            index += 1

    def __get_destination(self) -> str:
        if not self.__selected_files:
            raise ValueError("Nenhum arquivo selecionado.")

        if not self.__destination_customized:
            self.__update_default_destination()

        return self.__destination_var.get()

    def __update_progress_bar(self, progress: int) -> None:
        self.__progress["value"] = progress
        self.__root.update_idletasks()

    @staticmethod
    def __open_path(path: str) -> None:
        try:
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as error:
            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir o destino:\n{error}",
            )
