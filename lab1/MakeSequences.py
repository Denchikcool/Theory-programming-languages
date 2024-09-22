import sys
import json
import typing
import tkinter as tk
from dataclasses import dataclass
from TreeCreation import GraphicalTree, Vertex
from graphviz import Digraph


@dataclass(frozen=True)
class Grammar:
    VT: typing.List[str]
    VN: typing.List[str]
    P: typing.Dict[str, typing.List[str]]
    S: str


def generate_sequences(grammar, min_length, max_length):
    stack = [([], grammar.S)]
    was_in_stack = set()
    counter = 1
    ans = []

    try:
        while stack:
            (prev, sequence) = stack.pop()
            prev = prev.copy()
            prev.append(sequence)

            if sequence in was_in_stack:
                continue

            was_in_stack.add(sequence)

            only_term = True

            for i, symbol in enumerate(sequence):
                if symbol in grammar.VN:
                    only_term = False
                    for elem in grammar.P[symbol]:
                        scopy = (sequence[:i] + elem + sequence[i + 1:])
                        if (len(scopy) <= max_length + 3):
                            stack.append((prev, scopy))

            if only_term and min_length <= len(sequence) <= max_length:
                ans.append(prev)
                counter += 1

        return ans
    except KeyError:
        print("Ошибка. Вероятнее всего грамматика задана некорректно!", file=sys.stderr)
        exit(1)


def get_changes(current, next, G):
    if len(next) < len(current):
        return "λ"
    for i, ch in enumerate(current[::-1]):
        i = len(current) - i - 1
        if ch in G.VN:
            return next[i : i + len(next) - len(current) + 1]
    return "λ"


def get_right_vertex(tree, G):
    if not tree.children and tree.data in G.VN:
        return tree
    for vert in tree.children[::-1]:
        v = get_right_vertex(vert, G)
        if v:
            return v


def generate_tree(choiced_ans, G):
    tree = Vertex(choiced_ans[0])
    for curr, next in zip(choiced_ans, choiced_ans[1:]):
        changes = get_changes(curr, next, G)
        v = get_right_vertex(tree, G)
        if v is not None:
            v.children = list(map(Vertex, changes))
    return tree


def generate_all_sequences(grammar_file_var, min_length_entry, max_length_entry, result_text):
    selected_grammar_file = grammar_file_var.get()
    min_length = int(min_length_entry.get())
    max_length = int(max_length_entry.get())

    if min_length < 0:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Минимальная длина не может быть отрицательной")
        return

    try:
        with open(selected_grammar_file, "r") as grammar_file:
            G = Grammar(**json.load(grammar_file))
    except (json.JSONDecodeError, TypeError):
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Файл грамматики некорректен")
        return

    sequences = generate_sequences(G, min_length, max_length)

    result_text.delete("1.0", tk.END)

    for i, sequence in enumerate(sequences, 1):
        result_text.insert(tk.END, f"[{i}] {sequence[-1]}\n")


def generate_and_display_tree(grammar_file_var, min_length_entry, max_length_entry, choise_entry, result_text):
    selected_grammar_file = grammar_file_var.get()
    min_length = int(min_length_entry.get())
    max_length = int(max_length_entry.get())

    try:
        with open(selected_grammar_file, "r") as grammar_file:
            G = Grammar(**json.load(grammar_file))
    except (json.JSONDecodeError, TypeError):
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Файл грамматики некорректен")
        return

    sequences = generate_sequences(G, min_length, max_length)

    choise = int(choise_entry.get())
    if choise < 1 or choise > len(sequences):
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Введите допустимый номер цепочки")
        return

    choiced_ans = sequences[choise - 1]
    tree = generate_tree(choiced_ans, G)

    gt = GraphicalTree(tree)
    gt.start()
