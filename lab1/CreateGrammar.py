import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog


class GrammarEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Создание новой грамматики")

        self.grammar = {"VT": [], "VN": [], "P": {}, "S": "S"}

        self.step = 1

        self.create_step_widgets()

    def create_step_widgets(self):
        if self.step == 1:
            self.create_alphabet_step()
        elif self.step == 2:
            self.create_non_terminals_step()
        elif self.step == 3:
            self.create_rules_step()
        else:
            self.save_grammar_and_exit()

    def create_alphabet_step(self):
        self.step_label = ttk.Label(self.root)
        self.step_label.pack(padx=10, pady=10)

        self.alphabet_label = ttk.Label(self.root, text="Введите алфавит (VT):")
        self.alphabet_label.pack(padx=10, pady=5)

        self.alphabet_entry = ttk.Entry(self.root, width=30)
        self.alphabet_entry.pack(padx=10, pady=5)

        self.next_button = ttk.Button(self.root, text="Продолжить", command=self.handle_alphabet_next)
        self.next_button.pack(padx=10, pady=10)

    def handle_alphabet_next(self):
        alphabet = self.alphabet_entry.get().split(",")
        if all(map(lambda x: len(x) == 1, alphabet)):
            self.grammar["VT"] = alphabet
            self.step += 1
            self.clear_previous_widgets()
            self.create_step_widgets()
        else:
            messagebox.showerror("Ошибка", "Алфавит должен состоять из одиночных символов. Перечислять символы через запятую, без пробелов.")

    def create_non_terminals_step(self):
        self.step_label = ttk.Label(self.root)
        self.step_label.pack(padx=10, pady=10)

        self.non_terminals_label = ttk.Label(self.root, text="Введите правила (VN):")
        self.non_terminals_label.pack(padx=10, pady=5)

        self.non_terminals_entry = ttk.Entry(self.root, width=30)
        self.non_terminals_entry.pack(padx=10, pady=5)

        self.next_button = ttk.Button(self.root, text="Продолжить", command=self.handle_non_terminals_next)
        self.next_button.pack(padx=10, pady=10)

    def handle_non_terminals_next(self):
        non_terminals = self.non_terminals_entry.get().split(",")
        non_terminals = [x.strip() for x in non_terminals]
        if all(map(lambda x: len(x) == 1 and x.isupper(), non_terminals)):
            if "S" not in non_terminals:
                non_terminals.append("S")
            self.grammar["VN"] = non_terminals
            self.step += 1
            self.clear_previous_widgets()
            self.create_step_widgets()
        else:
            messagebox.showerror("Ошибка", "Нетерминальные символы должны состоять из одной заглавной буквы. Перечислять символы через запятую, без пробелов.")

    def create_rules_step(self):
        self.step_label = ttk.Label(self.root)
        self.step_label.pack(padx=10, pady=10)

        self.rules_label = ttk.Label(self.root, text="Правила создания грамматики (точка входа P):")
        self.rules_label.pack(padx=10, pady=5)

        self.rules_text = tk.Text(self.root, width=40, height=10)
        self.rules_text.pack(padx=10, pady=5)

        self.next_button = ttk.Button(self.root, text="Продолжить", command=self.handle_rules_next)
        self.next_button.pack(padx=10, pady=10)

    def handle_rules_next(self):
        rules_text = self.rules_text.get("1.0", tk.END).strip()
        rules = {}
        for line in rules_text.split("\n"):
            if line:
                parts = line.split("->")
                if len(parts) == 2:
                    non_terminal = parts[0].strip()
                    productions = parts[1].strip().split("|")
                    productions = [p.replace("lambda", "") for p in productions]
                    rules[non_terminal] = productions
                else:
                    messagebox.showerror("Ошибка", f"Некорректное правило: {line}. Пример правила: S -> 0|1|lambda")
                    return
        self.grammar["P"] = rules
        self.step += 1
        self.clear_previous_widgets()
        self.create_step_widgets()

    def save_grammar_and_exit(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Сохранить как JSON")

        if file_path:
            with open(file_path, "w") as json_file:
                json.dump(self.grammar, json_file, indent=4)

        self.root.destroy()

    def clear_previous_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
