import random
import tkinter
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SpanTree:
    def __init__(self, value):
        self.value = value
        self.children = []

    def expand(self, new_states):
        self.children = new_states

class Square:
    def __init__(self, A, E, I, O):
        self.A = A
        self.E = E
        self.I = I
        self.O = O

class LogicSquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Square")
        self.root.geometry("1600x1200")  # Zwiększ rozmiar okna (dwukrotnie większa wysokość i długość)

        self.LP = 1
        self.squares = []
        self.buttons = []
        self.entries = []
        self.expands = []
        self.create_widgets()
        self.add_extract_button(5)
        self.add_restart_button(7)  # Add Restart button

        instructions_text1 = "User Instructions:"
        instructions_text2 = (
            "1. Enter values for the A, E, I, O categories in the respective fields.\n"
            "2. Click the (+) button next to the corresponding category to add a new logic square.\n"
            "3. Repeat steps 1-2 for each category as needed.\n"
            "4. Click the 'Confirm' button to confirm the user-entered data.\n"
            "5. Graphs will be automatically generated based on the entered data."
        )

        instructions_label = tk.Label(self.root, text=instructions_text1, justify='center', font=('Arial', 12, 'bold'))
        instructions_label.grid(row=1, column=3, rowspan=1, padx=150, pady=20)
        new_label = tk.Label(self.root, text=instructions_text2, justify='left', font=('Arial', 11))
        new_label.grid(row=2, column=3, rowspan=2, padx=150, pady=0)

    def create_widgets(self, row_index=2):
        # Create a style for ttk widgets
        style = ttk.Style()
        style.configure("TLabel", padding=10)

        # Create labels and entries
        ttk.Label(self.root, text=f"Logic Square {self.LP}").grid(row=row_index - 1, column=1)

        entry1 = ttk.Entry(self.root)
        entry1.grid(row=row_index, column=0, padx=10, pady=10)
        label = ttk.Label(self.root, text=" <--> ")
        label.grid(row=row_index, column=1)
        entry2 = ttk.Entry(self.root)
        entry2.grid(row=row_index, column=2, padx=10, pady=10)

        ttk.Label(self.root, text="").grid(row=row_index + 1, column=2)

        entry3 = ttk.Entry(self.root)
        entry3.grid(row=row_index + 4, column=0, padx=10, pady=10)

        button1 = ttk.Button(self.root, text="+",
                             command=lambda i=row_index + 10: self.add_logic_square(i, entry1, entry2, entry3, entry4,
                                                                                    1))
        button1.grid(row=row_index, column=0, rowspan=5)
        self.buttons.append(button1)  # Add reference to the button in the list
        self.entries.extend([entry1, entry2])  # Add references to the entry widgets in the list

        button2 = ttk.Button(self.root, text="+",
                             command=lambda i=row_index + 10: self.add_logic_square(i, entry1, entry2, entry3, entry4,
                                                                                    2))
        button2.grid(row=row_index, column=2, rowspan=5)
        self.buttons.append(button2)  # Add reference to the button in the list

        entry4 = ttk.Entry(self.root)
        entry4.grid(row=row_index + 4, column=2, padx=10, pady=10)
        self.entries.extend([entry3, entry4])  # Add references to the entry widgets in the list

        button3 = ttk.Button(self.root, text="+",
                             command=lambda i=row_index + 10: self.add_logic_square(i, entry1, entry2, entry3, entry4,
                                                                                    3))
        button3.grid(row=row_index + 2, column=1, rowspan=5)
        self.buttons.append(button3)  # Add reference to the button in the list

        return row_index + 7

    def add_extract_button(self, row_index):
        extract_button = ttk.Button(self.root, text="Confirm", command=self.confirm)
        extract_button.grid(row=row_index + 1, column=3, pady=10, padx=20)  # Increase padx to make it wider
        extract_button.config(width=30)  # Increase the width of the button
        self.buttons.append(extract_button)

    def add_restart_button(self, row_index):
        restart_button = ttk.Button(self.root, text="Restart", command=self.restart_program)
        restart_button.grid(row=row_index, column=3, pady=10, padx=20)
        restart_button.config(width=30)
        self.buttons.append(restart_button)

    def restart_program(self):
        # Add any logic needed to restart the program here
        print("Restarting the program...")
        self.root.destroy()  # Close the current Tkinter window
        new_root = tk.Tk()  # Create a new Tkinter window
        app = LogicSquareApp(new_root)  # Create a new instance of the application
        new_root.mainloop()  # Start the main loop for the new window

    def add_logic_square(self, row_index, entry1, entry2, entry3, entry4, buttonID):
        self.LP += 1  # Increment the logic square count
        new_row_index = self.create_widgets(row_index)

        # Copy values from the source entries to the new entries
        if buttonID == 1:
            self.entries[-4].delete(0, tk.END)
            self.entries[-4].insert(0, entry1.get())
            self.entries[-2].delete(0, tk.END)
            self.entries[-2].insert(0, entry3.get())
            self.expands.append([entry1.get(), entry3.get()])
        elif buttonID == 2:
            self.entries[-3].delete(0, tk.END)
            self.entries[-3].insert(0, entry2.get())
            self.entries[-1].delete(0, tk.END)
            self.entries[-1].insert(0, entry4.get())
            self.expands.append([entry2.get(), entry4.get()])
        else:
            self.entries[-2].delete(0, tk.END)
            self.entries[-2].insert(0, entry3.get())
            self.entries[-1].delete(0, tk.END)
            self.entries[-1].insert(0, entry4.get())
            self.expands.append([entry3.get(), entry4.get()])

        # Create a Square instance and add it to the list
        square_instance = Square(entry1.get(), entry2.get(), entry3.get(), entry4.get())
        self.squares.append(square_instance)

        # Print information about the squares in the console
        self.print_squares_info()
    def print_squares_info(self):
        print("Squares Information:")
        for i, square in enumerate(self.squares, start=1):
            print(f"Square {i}: A={square.A}, E={square.E}, I={square.I}, O={square.O}")

    def select_leaf_to_expand(self, span_tree):
        if span_tree.children:
            for e in span_tree.children:
                if e.value == self.expands[0]:
                    self.expands.pop(0)
                    return e
        else:
            return span_tree

    def confirm(self):
        current_square = Square(self.entries[-4].get(), self.entries[-3].get(), self.entries[-2].get(), self.entries[-1].get())
        self.squares.append(current_square)
        self.print_squares_info()
        self.extract_and_expand()

    def extract_and_expand(self):
        span_tree = SpanTree("0")
        leaf = span_tree

        for s in self.squares:
            leaf = self.select_leaf_to_expand(leaf)
            print(str(leaf.value))
            A = s.A
            E = s.E
            O = s.O
            I = s.I

            newStates = [SpanTree([A, I]), SpanTree([E, O]), SpanTree([I, O])]
            leaf.expand(newStates)
        self.draw_tree(span_tree)

        directed_graph = self.span_tree_to_directed_graph(span_tree)


    def span_tree_to_directed_graph(self, span_tree):
        directed_graph = nx.DiGraph()
        self.collect_leaf_nodes(span_tree, directed_graph)
        self.add_user_transitions(directed_graph)
        return directed_graph

    def collect_leaf_nodes(self, node, graph):
        if not node.children:
            graph.add_node(str(node.value))

        for child in node.children:
            self.collect_leaf_nodes(child, graph)

    def add_user_transitions(self, directed_graph):
        all_nodes = list(directed_graph.nodes)
        dialog_window = tk.Toplevel(self.root)
        dialog_window.title("Enter Transitions")


        # Utwórz ramkę dla obszaru przewijania
        frame = ttk.Frame(dialog_window)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Utwórz płótno do przechowywania ramki
        canvas = tk.Canvas(frame, width=1200, height=800)  # Dostosuj szerokość i wysokość według potrzeb
        canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Utwórz pasek przewijania dla płótna
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Konfiguruj płótno i pasek przewijania
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        # Utwórz ramkę do przechowywania widżetów wewnątrz płótna
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw", width=1600,
                             height=2400)  # Dostosuj szerokość i wysokość według potrzeb

        # Utwórz przejścia za pomocą inner_frame
        transitions = {}
        for source in all_nodes:
            for target in all_nodes:
                if source != target:
                    label_text = f"Enter transition from {source} to {target}:"
                    label = ttk.Label(inner_frame, text=label_text)

                    entry_var = tk.StringVar()
                    entry = ttk.Entry(inner_frame, textvariable=entry_var)

                    label.grid(row=len(transitions), column=0, padx=5, pady=5, sticky="e")
                    entry.grid(row=len(transitions), column=1, padx=5, pady=5, sticky="w")

                    transitions[(source, target)] = entry_var

        def ok_button_callback():
            for (source, target), entry_var in transitions.items():
                transition = entry_var.get()
                print(f"Transition from {source} to {target}: {transition}")

                if transition:
                    directed_graph.add_edge(source, target, label=transition)

            dialog_window.destroy()
            self.draw_directed_graph(directed_graph)

        ok_button = ttk.Button(inner_frame, text="OK", command=ok_button_callback)
        ok_button.grid(row=len(transitions), column=0, columnspan=2, pady=10)

        # Połącz przewijanie płótna z kółkiem myszy
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def draw_directed_graph(self, directed_graph):
        pos = nx.spring_layout(directed_graph)
        edge_labels = nx.get_edge_attributes(directed_graph, 'Transitions')
        nx.draw(directed_graph, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=8,
                font_color='black', font_weight='bold', arrowsize=15)
        nx.draw_networkx_edge_labels(directed_graph, pos, edge_labels=edge_labels)
        plt.show()

    def draw_tree(self, span_tree):
        graph = nx.Graph()
        graph.add_node(str(span_tree.value))

        queue = deque([(span_tree, None, None, 0)])

        vert_gap = 0.2
        width = 1.0

        while queue:
            node, parent_name, parent_xcenter, level = queue.popleft()

            xcenter = parent_xcenter + width / 2 if parent_xcenter is not None else 0.5
            ycenter = -level * vert_gap
            graph.add_node(str(node.value), pos=(xcenter, ycenter))
            if parent_name is not None:
                graph.add_edge(parent_name, str(node.value))

            for i, child in enumerate(node.children):
                queue.append((child, str(node.value), xcenter + i - len(node.children) / 2, level + 1))

        pos = nx.get_node_attributes(graph, 'pos')

        self.draw_graph_in_tkinter(graph, pos)

    def draw_graph_in_tkinter(self, graph, pos):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Span Tree")

        canvas = FigureCanvasTkAgg(plt.figure(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        nx.draw(graph, pos=pos, with_labels=True, node_size=700, node_color='skyblue', font_size=8, font_color='black',
                font_weight='bold', ax=canvas.figure.gca())
        plt.close()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = LogicSquareApp(root)
    root.mainloop()
