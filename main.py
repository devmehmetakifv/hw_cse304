#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.core.processor import CalculationProcessor
from src.core.file_reader import FileReader

class StatisticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statistical Operations")
        self.root.geometry("600x500")
        
        self.selected_folder = None
        self.calculation_options = {
            "average": tk.BooleanVar(),
            "maximum": tk.BooleanVar(),
            "minimum": tk.BooleanVar(),
            "standard_deviation": tk.BooleanVar(),
            "frequency": tk.BooleanVar(),
            "median": tk.BooleanVar(),
        }
        self.global_var = tk.BooleanVar()
        
        self.init_ui()
    
    def init_ui(self):
        # Folder selection frame
        folder_frame = ttk.LabelFrame(self.root, text="Folder Selection")
        folder_frame.pack(fill="x", padx=10, pady=10)
        
        self.folder_label = ttk.Label(folder_frame, text="No folder selected")
        self.folder_label.pack(side="left", padx=10, pady=10)
        
        select_btn = ttk.Button(folder_frame, text="Select Folder", command=self.select_folder)
        select_btn.pack(side="right", padx=10, pady=10)
        
        # Calculation options frame
        calc_frame = ttk.LabelFrame(self.root, text="Calculation Options")
        calc_frame.pack(fill="x", padx=10, pady=10)
        
        # Add checkboxes for each calculation type
        for i, (option, var) in enumerate(self.calculation_options.items()):
            cb = ttk.Checkbutton(calc_frame, text=option.capitalize(), variable=var)
            cb.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
        
        # Global option
        global_cb = ttk.Checkbutton(calc_frame, text="Global", variable=self.global_var)
        global_cb.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Calculate button
        calc_btn = ttk.Button(self.root, text="Calculate", command=self.calculate)
        calc_btn.pack(padx=10, pady=10)
        
        # Message area
        message_frame = ttk.LabelFrame(self.root, text="Message Content")
        message_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.message_text = tk.Text(message_frame, wrap="word", height=10)
        self.message_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Measurements")
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=folder)
    
    def calculate(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return
        
        # Get selected operations
        selected_operations = [op for op, var in self.calculation_options.items() if var.get()]
        
        if not selected_operations:
            messagebox.showerror("Error", "Please select at least one calculation option.")
            return
        
        try:
            # Read measurement files
            measurement_files = FileReader.scan_directory(self.selected_folder)
            
            # Process calculations
            processor = CalculationProcessor(self.selected_folder)
            result = processor.process_calculations(
                measurement_files, 
                selected_operations,
                self.global_var.get()
            )
            
            # Display result message
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, result["message"])
            
            if result["status"] == "Success":
                messagebox.showinfo("Success", "Calculations completed successfully.")
            else:
                messagebox.showerror("Error", result["message"])
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StatisticsApp(root)
    root.mainloop() 