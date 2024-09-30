from math import trunc
import tkinter as tk
from tkinter import filedialog, ttk
from MakeSequences import generate_all_sequences, generate_and_display_tree
from CreateGrammar import GrammarEditor

def open_grammar_editor():
    root_editor = tk.Tk()
    editor = GrammarEditor(root_editor)

def create_gui(root):
    # Настройки стиля
    style = ttk.Style()
    style.configure("TLabelframe", background="#E6E6FA", padding=10)
    style.configure("TButton", background="#e0e0e0", foreground="#000000", padding=10, borderwidth=0, relief="flat")
    style.configure("TEntry", fieldbackground="#f0f0f0", foreground="#000", padding=5, relief="flat")

    root.configure(background="#f8f8f8")

    # Область для работы с грамматикой
    grammar_frame = ttk.Labelframe(root, text="Грамматика")
    grammar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
    grammar_frame.configure(labelanchor="n")

    grammar_file_var = tk.StringVar()
    grammar_file_label = ttk.Label(grammar_frame, text="Файл:")
    grammar_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    grammar_file_entry = ttk.Entry(grammar_frame, textvariable=grammar_file_var, width=40, state="readonly")
    grammar_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    browse_button = ttk.Button(grammar_frame, text="Открыть проводник", command=lambda: grammar_file_var.set(filedialog.askopenfilename()))
    browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    open_editor_button = ttk.Button(grammar_frame, text="Открыть редактор", command=open_grammar_editor)
    open_editor_button.grid(row=1, column=0, columnspan=3, pady=5)

    length_frame = ttk.Labelframe(root, text="Длина цепочек")
    length_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
    length_frame.configure(labelanchor="n")

    min_length_label = ttk.Label(length_frame, text="Минимальная:")
    min_length_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Ползунок для минимальной длины
    min_length_var = tk.IntVar(value=1)
    min_length_scale = ttk.Scale(length_frame, from_=1, to=20, orient="horizontal", command=lambda value: min_length_var.set(int(round(float(value)))))
    min_length_scale.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Иллюстрация значения для минимальной длины
    min_length_value_label = ttk.Label(length_frame, textvariable=min_length_var)
    min_length_value_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    max_length_label = ttk.Label(length_frame, text="Максимальная:")
    max_length_label.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    # Ползунок для максимальной длины
    max_length_var = tk.IntVar(value=10)
    max_length_scale = ttk.Scale(length_frame, from_=3, to=20, orient="horizontal", command=lambda value: max_length_var.set(int(round(float(value)))))
    max_length_scale.grid(row=0, column=6, padx=5, pady=5, sticky="w")

    # Иллюстрация значения для максимальной длины
    max_length_value_label = ttk.Label(length_frame, textvariable=max_length_var)
    max_length_value_label.grid(row=0, column=7, padx=5, pady=5, sticky="w")

    # Кнопка "Сгенерировать"
    generate_length_button = ttk.Button(length_frame, text="Сгенерировать",command=lambda: generate_all_sequences(grammar_file_var, min_length_var.get(),max_length_var.get(),result_text))
    generate_length_button.grid(row=1, column=0, columnspan=4, pady=5)

    # Область для вывода результата
    result_frame = ttk.Labelframe(root, text="Результат")
    result_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
    result_frame.configure(labelanchor="n")

    # Настройка растяжения labelframe
    result_frame.rowconfigure(0, weight=1)
    result_frame.columnconfigure(0, weight=1)

    result_text = tk.Text(result_frame, wrap=tk.WORD, width=40, height=10)
    result_text.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(result_frame)
    scrollbar.grid(row=0, column=1, sticky="ns")

    result_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_text.yview)

    # Настройка растяжения основного окна
    root.columnconfigure(0, weight=1)
    root.rowconfigure(3, weight=1)

    # Область для выбора цепочки для построения дерева
    choice_frame = ttk.Labelframe(root, text="Выбор цепочки")
    choice_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
    choice_frame.configure(labelanchor="n")

    choise_label = ttk.Label(choice_frame, text="Номер:")
    choise_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    choise_var = tk.StringVar()
    choise_entry = ttk.Entry(choice_frame, textvariable=choise_var, width=50)
    choise_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    generate_button = ttk.Button(choice_frame, text="Изображение дерева", command=lambda: generate_and_display_tree(
        grammar_file_var, min_length_var, max_length_var, choise_entry, result_text))
    generate_button.grid(row=1, column=1, columnspan=2, pady=5)