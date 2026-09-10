import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path as SystemPath
from tkinter import StringVar, Tk, messagebox, ttk

from src.application.dto.converter_input_file import ConverterInputFile
from src.application.dto.selector_output_file import SelectorOutputFile
from src.application.usecase.file_converter_usecase import FileConverterUseCase
from src.application.usecase.file_selector_usecase import FileSelectorUseCase
from src.domain.gateway.file_save_location_selector import FileSaveLocationSelector
from src.domain.valuesobject.type import Type
from src.presentation.theme import configure_theme


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
        self.__summary_var = StringVar(value="Nenhum arquivo selecionado")
        self.__status_var = StringVar(value="Adicione imagens ou PDFs para começar.")
        self.__destination_customized = False
        self.__is_converting = False
        self.__last_output_path: str | None = None

        self.__file_table: ttk.Treeview
        self.__progress: ttk.Progressbar
        self.__add_button: ttk.Button
        self.__remove_button: ttk.Button
        self.__clear_button: ttk.Button
        self.__up_button: ttk.Button
        self.__down_button: ttk.Button
        self.__change_destination_button: ttk.Button
        self.__reset_destination_button: ttk.Button
        self.__open_destination_button: ttk.Button
        self.__open_result_button: ttk.Button
        self.__convert_button: ttk.Button

        self.__create_interface()
        self.__bind_shortcuts()
        self.__update_controls()

    def __create_interface(self) -> None:
        self.__root.title("Conversor PDF & Imagens")
        self.__root.geometry("860x700")
        self.__root.minsize(760, 620)

        style = ttk.Style(self.__root)
        configure_theme(style)

        root_frame = ttk.Frame(self.__root, style="App.TFrame", padding=(22, 18))
        root_frame.pack(fill="both", expand=True)

        self.__build_header(root_frame)
        self.__build_file_section(root_frame)
        self.__build_options_section(root_frame)
        self.__build_footer(root_frame)

    def __build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))

        title_group = ttk.Frame(header, style="App.TFrame")
        title_group.pack(side="left", fill="x", expand=True)

        ttk.Label(
            title_group,
            text="Conversor PDF & Imagens",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            title_group,
            text=(
                "Junte PDFs e imagens em um único arquivo ou converta imagens "
                "para PNG/JPEG."
            ),
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        self.__add_button = ttk.Button(
            header,
            text="＋ Adicionar arquivos",
            style="Primary.TButton",
            command=self.select_files,
        )
        self.__add_button.pack(side="right", padx=(12, 0))

    def __build_file_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Arquivos e ordem das páginas", padding=12)
        section.pack(fill="both", expand=True)

        section_header = ttk.Frame(section)
        section_header.pack(fill="x", pady=(0, 8))

        ttk.Label(
            section_header,
            textvariable=self.__summary_var,
            style="Muted.TLabel",
        ).pack(side="left")

        ttk.Label(
            section_header,
            text="A ordem abaixo será mantida no PDF final.",
            style="Muted.TLabel",
        ).pack(side="right")

        table_frame = ttk.Frame(section)
        table_frame.pack(fill="both", expand=True)

        self.__file_table = ttk.Treeview(
            table_frame,
            columns=("order", "name", "type", "size"),
            show="headings",
            selectmode="extended",
        )
        self.__file_table.heading("order", text="#")
        self.__file_table.heading("name", text="Arquivo")
        self.__file_table.heading("type", text="Tipo")
        self.__file_table.heading("size", text="Tamanho")

        self.__file_table.column("order", width=48, minwidth=48, anchor="center", stretch=False)
        self.__file_table.column("name", width=480, minwidth=250, anchor="w")
        self.__file_table.column("type", width=90, minwidth=80, anchor="center", stretch=False)
        self.__file_table.column("size", width=100, minwidth=90, anchor="e", stretch=False)

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.__file_table.yview,
        )
        self.__file_table.configure(yscrollcommand=y_scroll.set)

        self.__file_table.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")

        actions = ttk.Frame(section)
        actions.pack(fill="x", pady=(10, 0))

        self.__up_button = ttk.Button(
            actions,
            text="↑ Subir",
            style="Compact.TButton",
            command=self.move_up,
        )
        self.__up_button.pack(side="left")

        self.__down_button = ttk.Button(
            actions,
            text="↓ Descer",
            style="Compact.TButton",
            command=self.move_down,
        )
        self.__down_button.pack(side="left", padx=(6, 0))

        self.__remove_button = ttk.Button(
            actions,
            text="Remover",
            style="Compact.TButton",
            command=self.remove_selected,
        )
        self.__remove_button.pack(side="left", padx=(12, 0))

        self.__clear_button = ttk.Button(
            actions,
            text="Limpar lista",
            style="Compact.TButton",
            command=self.clear_files,
        )
        self.__clear_button.pack(side="left", padx=(6, 0))

        ttk.Label(
            actions,
            text="Atalhos: Ctrl+O adicionar · Delete remover · Ctrl+↑/↓ ordenar",
            style="Muted.TLabel",
        ).pack(side="right")

        self.__file_table.bind("<<TreeviewSelect>>", lambda _event: self.__update_controls())

    def __build_options_section(self, parent: ttk.Frame) -> None:
        options = ttk.Frame(parent, style="App.TFrame")
        options.pack(fill="x", pady=(14, 0))

        format_frame = ttk.LabelFrame(options, text="Formato de saída", padding=12)
        format_frame.pack(side="left", fill="both", expand=True, padx=(0, 7))

        radios = ttk.Frame(format_frame)
        radios.pack(fill="x")

        for text, value in (
            ("PDF único", "PDF"),
            ("PNG", "PNG"),
            ("JPEG", "JPEG"),
        ):
            ttk.Radiobutton(
                radios,
                text=text,
                variable=self.__format_var,
                value=value,
                command=self.__on_format_change,
            ).pack(side="left", padx=(0, 18))

        ttk.Label(
            format_frame,
            text="PDF aceita imagens + PDFs. PNG/JPEG aceitam somente imagens.",
            style="Muted.TLabel",
            wraplength=330,
        ).pack(anchor="w", pady=(8, 0))

        destination_frame = ttk.LabelFrame(options, text="Destino", padding=12)
        destination_frame.pack(side="left", fill="both", expand=True, padx=(7, 0))

        destination_entry = ttk.Entry(
            destination_frame,
            textvariable=self.__destination_var,
            state="readonly",
        )
        destination_entry.pack(fill="x")

        destination_actions = ttk.Frame(destination_frame)
        destination_actions.pack(fill="x", pady=(8, 0))

        self.__change_destination_button = ttk.Button(
            destination_actions,
            text="Alterar...",
            style="Compact.TButton",
            command=self.change_destination,
        )
        self.__change_destination_button.pack(side="left")

        self.__reset_destination_button = ttk.Button(
            destination_actions,
            text="Usar automático",
            style="Compact.TButton",
            command=self.reset_destination,
        )
        self.__reset_destination_button.pack(side="left", padx=(6, 0))

        self.__open_destination_button = ttk.Button(
            destination_actions,
            text="Abrir pasta",
            style="Compact.TButton",
            command=self.open_destination,
        )
        self.__open_destination_button.pack(side="right")

    def __build_footer(self, parent: ttk.Frame) -> None:
        footer = ttk.Frame(parent, style="App.TFrame")
        footer.pack(fill="x", pady=(14, 0))

        progress_group = ttk.Frame(footer, style="App.TFrame")
        progress_group.pack(side="left", fill="x", expand=True, padx=(0, 14))

        status_row = ttk.Frame(progress_group, style="App.TFrame")
        status_row.pack(fill="x", pady=(0, 5))

        ttk.Label(
            status_row,
            textvariable=self.__status_var,
            style="Status.TLabel",
        ).pack(side="left")

        self.__progress = ttk.Progressbar(
            progress_group,
            orient="horizontal",
            mode="determinate",
        )
        self.__progress.pack(fill="x")

        self.__open_result_button = ttk.Button(
            footer,
            text="Abrir resultado",
            command=self.open_result,
        )
        self.__open_result_button.pack(side="right")

        self.__convert_button = ttk.Button(
            footer,
            text="Converter",
            style="Primary.TButton",
            command=self.convert_selected,
        )
        self.__convert_button.pack(side="right", padx=(0, 8))

    def __bind_shortcuts(self) -> None:
        self.__root.bind("<Control-o>", lambda _event: self.select_files())
        self.__root.bind("<Control-O>", lambda _event: self.select_files())
        self.__root.bind("<Delete>", lambda _event: self.remove_selected())
        self.__root.bind("<Control-Return>", lambda _event: self.convert_selected())
        self.__root.bind("<Control-Up>", lambda _event: self.move_up())
        self.__root.bind("<Control-Down>", lambda _event: self.move_down())

    def select_files(self) -> None:
        if self.__is_converting:
            return

        selected = self.__file_selector_usecase.select()
        if not selected:
            return

        existing_paths = {
            os.path.normcase(os.path.abspath(file.path))
            for file in self.__selected_files
        }

        added = 0
        ignored = 0

        for file in selected:
            normalized = os.path.normcase(os.path.abspath(file.path))
            if normalized in existing_paths:
                ignored += 1
                continue

            self.__selected_files.append(file)
            existing_paths.add(normalized)
            added += 1

        self.__destination_customized = False
        self.__last_output_path = None
        self.__refresh_file_table()
        self.__update_default_destination()

        if ignored:
            self.__status_var.set(
                f"{added} arquivo(s) adicionado(s). {ignored} duplicado(s) ignorado(s)."
            )
        else:
            self.__status_var.set(f"{added} arquivo(s) adicionado(s).")

        self.__update_controls()

    def remove_selected(self) -> None:
        if self.__is_converting:
            return

        indexes = self.__selected_indexes()
        if not indexes:
            return

        for index in reversed(indexes):
            del self.__selected_files[index]

        self.__destination_customized = False
        self.__last_output_path = None
        self.__refresh_file_table()
        self.__update_default_destination()
        self.__status_var.set("Arquivo(s) removido(s) da lista.")
        self.__update_controls()

    def clear_files(self) -> None:
        if self.__is_converting or not self.__selected_files:
            return

        self.__selected_files.clear()
        self.__destination_customized = False
        self.__last_output_path = None
        self.__refresh_file_table()
        self.__update_default_destination()
        self.__progress["value"] = 0
        self.__status_var.set("Lista limpa. Adicione arquivos para começar.")
        self.__update_controls()

    def move_up(self) -> None:
        if self.__is_converting:
            return

        indexes = self.__selected_indexes()
        if not indexes or indexes[0] == 0:
            return

        for index in indexes:
            self.__selected_files[index - 1], self.__selected_files[index] = (
                self.__selected_files[index],
                self.__selected_files[index - 1],
            )

        new_indexes = [index - 1 for index in indexes]
        self.__refresh_file_table(new_indexes)
        self.__status_var.set("Ordem atualizada.")
        self.__update_controls()

    def move_down(self) -> None:
        if self.__is_converting:
            return

        indexes = self.__selected_indexes()
        if not indexes or indexes[-1] == len(self.__selected_files) - 1:
            return

        for index in reversed(indexes):
            self.__selected_files[index + 1], self.__selected_files[index] = (
                self.__selected_files[index],
                self.__selected_files[index + 1],
            )

        new_indexes = [index + 1 for index in indexes]
        self.__refresh_file_table(new_indexes)
        self.__status_var.set("Ordem atualizada.")
        self.__update_controls()

    def change_destination(self) -> None:
        if not self.__selected_files or self.__is_converting:
            return

        suggested = self.__get_destination()
        selected = self.__save_location_selector.select(
            Type(self.__format_var.get()),
            suggested,
        )

        if selected:
            self.__destination_var.set(selected)
            self.__destination_customized = True
            self.__last_output_path = None
            self.__status_var.set("Destino personalizado definido.")
            self.__update_controls()

    def reset_destination(self) -> None:
        if not self.__selected_files or self.__is_converting:
            return

        self.__destination_customized = False
        self.__last_output_path = None
        self.__update_default_destination()
        self.__status_var.set("Destino automático restaurado.")
        self.__update_controls()

    def convert_selected(self) -> None:
        if self.__is_converting:
            return

        validation_error = self.__conversion_validation_error()
        if validation_error:
            messagebox.showwarning("Não é possível converter", validation_error)
            return

        output_path = self.__resolve_output_path_for_conversion()
        if output_path is None:
            return

        self.__progress["maximum"] = len(self.__selected_files)
        self.__progress["value"] = 0
        self.__is_converting = True
        self.__last_output_path = None
        self.__status_var.set(
            f"Convertendo 0 de {len(self.__selected_files)} arquivo(s)..."
        )
        self.__update_controls()
        self.__root.update_idletasks()

        try:
            input_data = ConverterInputFile(
                output_type=self.__format_var.get(),
                files_input=self.__selected_files,
                output_path=output_path,
                progress=self.__update_progress_bar,
            )
            output = self.__file_converter_usecase.converter(input_data)
        except Exception as error:
            self.__status_var.set("A conversão não foi concluída.")
            messagebox.showerror("Erro na conversão", str(error))
            return
        finally:
            self.__is_converting = False
            self.__update_controls()

        self.__last_output_path = output.output_path
        self.__status_var.set(
            f"Concluído: {output.quantity} arquivo(s) processado(s)."
        )
        self.__update_controls()

        if self.__format_var.get() == "PDF":
            message = (
                f"PDF criado com sucesso a partir de {output.quantity} arquivo(s).\n\n"
                f"Salvo em:\n{output.output_path}"
            )
        else:
            message = (
                f"{output.quantity} arquivo(s) convertido(s) com sucesso.\n\n"
                f"Salvos em:\n{output.output_path}"
            )

        messagebox.showinfo("Conversão concluída", message)

    def open_destination(self) -> None:
        if not self.__selected_files:
            return

        destination = self.__destination_var.get()
        target = (
            os.path.dirname(destination)
            if self.__format_var.get() == "PDF"
            else destination
        )

        if not target:
            return

        os.makedirs(target, exist_ok=True)
        self.__open_path(target)

    def open_result(self) -> None:
        if not self.__last_output_path:
            return

        target = self.__last_output_path

        if not os.path.exists(target):
            messagebox.showwarning(
                "Resultado não encontrado",
                "O resultado não está mais disponível no caminho informado.",
            )
            self.__last_output_path = None
            self.__update_controls()
            return

        self.__open_path(target)

    def __on_format_change(self) -> None:
        self.__destination_customized = False
        self.__last_output_path = None
        self.__progress["value"] = 0
        self.__update_default_destination()

        validation_error = self.__conversion_validation_error()
        if validation_error:
            self.__status_var.set(validation_error)
        elif self.__selected_files:
            self.__status_var.set(
                f"Saída alterada para {self.__format_var.get()}."
            )

        self.__update_controls()

    def __refresh_file_table(self, selected_indexes: list[int] | None = None) -> None:
        for item in self.__file_table.get_children():
            self.__file_table.delete(item)

        pdf_count = 0
        image_count = 0

        for index, file in enumerate(self.__selected_files, start=1):
            extension = SystemPath(file.path).suffix.lower()
            if extension == ".pdf":
                pdf_count += 1
                file_type = "PDF"
            else:
                image_count += 1
                file_type = extension.removeprefix(".").upper() or "ARQUIVO"

            self.__file_table.insert(
                "",
                "end",
                iid=str(index - 1),
                values=(
                    index,
                    os.path.basename(file.path),
                    file_type,
                    self.__format_size(file.path),
                ),
            )

        total = len(self.__selected_files)
        if total == 0:
            self.__summary_var.set("Nenhum arquivo selecionado")
        else:
            parts = [f"{total} arquivo" + ("" if total == 1 else "s")]
            if pdf_count:
                parts.append(f"{pdf_count} PDF" + ("" if pdf_count == 1 else "s"))
            if image_count:
                parts.append(f"{image_count} imagem" + ("" if image_count == 1 else "ns"))
            self.__summary_var.set(" · ".join(parts))

        if selected_indexes:
            for index in selected_indexes:
                item_id = str(index)
                if self.__file_table.exists(item_id):
                    self.__file_table.selection_add(item_id)
            first = str(selected_indexes[0])
            if self.__file_table.exists(first):
                self.__file_table.focus(first)
                self.__file_table.see(first)

    def __selected_indexes(self) -> list[int]:
        return sorted(int(item_id) for item_id in self.__file_table.selection())

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

    def __get_destination(self) -> str:
        if not self.__selected_files:
            raise ValueError("Nenhum arquivo selecionado.")

        if not self.__destination_customized:
            self.__update_default_destination()

        return self.__destination_var.get()

    def __resolve_output_path_for_conversion(self) -> str | None:
        if not self.__selected_files:
            return None

        if self.__format_var.get() != "PDF":
            return self.__destination_var.get()

        if not self.__destination_customized:
            first_file = SystemPath(self.__selected_files[0].path)
            candidate = first_file.parent / f"{first_file.stem}_convertido.pdf"
            destination = self.__next_available_pdf_path(candidate)
            self.__destination_var.set(str(destination))
            return str(destination)

        destination = self.__destination_var.get()
        normalized_destination = os.path.normcase(os.path.abspath(destination))
        input_paths = {
            os.path.normcase(os.path.abspath(file.path))
            for file in self.__selected_files
        }

        if normalized_destination in input_paths:
            messagebox.showwarning(
                "Destino inválido",
                "O PDF de saída não pode substituir um dos arquivos de entrada. "
                "Escolha outro nome ou outro local.",
            )
            return None

        if os.path.exists(destination):
            overwrite = messagebox.askyesno(
                "Substituir arquivo?",
                f"Já existe um arquivo neste destino:\n\n{destination}\n\n"
                "Deseja substituí-lo?",
            )
            if not overwrite:
                return None

        return destination

    def __conversion_validation_error(self) -> str | None:
        if not self.__selected_files:
            return "Selecione pelo menos um arquivo."

        if self.__format_var.get() != "PDF" and self.__has_pdf_input():
            return (
                "Há PDF na lista. Para misturar PDFs e imagens, escolha “PDF único”. "
                "PNG/JPEG aceitam somente imagens."
            )

        missing = [
            file.path
            for file in self.__selected_files
            if not os.path.isfile(file.path)
        ]
        if missing:
            return (
                "Um ou mais arquivos não existem mais no local original. "
                "Remova-os e selecione novamente."
            )

        return None

    def __has_pdf_input(self) -> bool:
        return any(
            SystemPath(file.path).suffix.lower() == ".pdf"
            for file in self.__selected_files
        )

    def __update_controls(self) -> None:
        has_files = bool(self.__selected_files)
        indexes = self.__selected_indexes()
        has_selection = bool(indexes)
        can_move_up = has_selection and indexes[0] > 0
        can_move_down = (
            has_selection
            and indexes[-1] < len(self.__selected_files) - 1
        )

        disabled = self.__is_converting

        self.__set_button_state(self.__add_button, not disabled)
        self.__set_button_state(self.__remove_button, has_selection and not disabled)
        self.__set_button_state(self.__clear_button, has_files and not disabled)
        self.__set_button_state(self.__up_button, can_move_up and not disabled)
        self.__set_button_state(self.__down_button, can_move_down and not disabled)
        self.__set_button_state(
            self.__change_destination_button,
            has_files and not disabled,
        )
        self.__set_button_state(
            self.__reset_destination_button,
            has_files and self.__destination_customized and not disabled,
        )
        self.__set_button_state(
            self.__open_destination_button,
            has_files and not disabled,
        )
        self.__set_button_state(
            self.__open_result_button,
            bool(self.__last_output_path) and not disabled,
        )

        can_convert = (
            has_files
            and self.__conversion_validation_error() is None
            and not disabled
        )
        self.__set_button_state(self.__convert_button, can_convert)

        if self.__is_converting:
            self.__convert_button.configure(text="Convertendo...")
        else:
            self.__convert_button.configure(text="Converter")

    @staticmethod
    def __set_button_state(button: ttk.Button, enabled: bool) -> None:
        if enabled:
            button.state(["!disabled"])
        else:
            button.state(["disabled"])

    def __update_progress_bar(self, progress: int) -> None:
        self.__progress["value"] = progress
        total = len(self.__selected_files)
        self.__status_var.set(f"Convertendo {progress} de {total} arquivo(s)...")
        self.__root.update_idletasks()

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

    @staticmethod
    def __format_size(path: str) -> str:
        try:
            size = os.path.getsize(path)
        except OSError:
            return "—"

        units = ("B", "KB", "MB", "GB")
        value = float(size)
        unit = units[0]

        for unit in units:
            if value < 1024 or unit == units[-1]:
                break
            value /= 1024

        if unit == "B":
            return f"{int(value)} {unit}"
        return f"{value:.1f} {unit}"

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
                f"Não foi possível abrir:\n{error}",
            )
