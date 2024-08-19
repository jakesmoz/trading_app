import tkinter as tk
from tkinter import scrolledtext, ttk

def setup_ui(master, trigger_function):
    master.title("Trading Application")
    master.geometry("600x400")

    label = tk.Label(master, text="Zak maak my Bra")
    label.pack(pady=10)

    trading_style_var = tk.StringVar(value='day')
    trading_style_options = ['day', 'swing', 'long-term']
    trading_style_menu = ttk.OptionMenu(master, trading_style_var, trading_style_options[0], *trading_style_options)
    trading_style_menu.pack(pady=10)

    recommend_button = tk.Button(master, text="Get Recommendations", command=lambda: trigger_function(trading_style_var.get()))
    recommend_button.pack(pady=20)

    global recommendation_text
    recommendation_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=10, font=("Helvetica", 12))
    recommendation_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    recommendation_text.config(state=tk.DISABLED)

def update_recommendations(text):
    recommendation_text.config(state=tk.NORMAL)
    recommendation_text.delete('1.0', tk.END)
    recommendation_text.insert(tk.END, text)
    recommendation_text.config(state=tk.DISABLED)
