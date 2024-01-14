import tkinter as tk
from tkinter import filedialog

class myGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mesclador Excel RWI")
        self.root.geometry("800x500")

        self.label_coords = tk.Label(self.root, text="Arquivo com coordenadas:")
        self.label_cep = tk.Label(self.root, text="Arquivo com CEPs:")

        self.btn_coords = tk.Button(self.root, text="Selecionar Arquivo com coordenadas", command=self.select_coords_file)
        self.btn_cep = tk.Button(self.root, text="Selecionar Arquivo com CEPs", command=self.select_cep_file)
        self.btn_merge = tk.Button(self.root, text="Mesclar", command=self.merge_files)

    def run(self):
        self.widgets_config()
        self.root.mainloop()

    def select_coords_file(self):
        coords_file = filedialog.askopenfilename(title="Selecione o arquivo com as coordenadas", filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
        if coords_file:
            self.coords_file.config(text=coords_file)

    def select_cep_file(self):
        cep_file = filedialog.askopenfilename(title="Selecione o arquivo com os CEPs", filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
        if cep_file:
            self.cep_file.config(text=cep_file)

    def merge_files(self):
        print("merge")
        pass

    def widgets_config(self):
        self.label_coords.pack(pady=10)
        self.label_cep.pack(pady=10)

        self.label_cep.pack(pady=10)
        self.btn_cep.pack(pady=10)

        self.btn_merge.pack(pady=10)