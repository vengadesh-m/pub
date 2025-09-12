import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.runner import run_request, run_batch_requests

class APITestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BrunoPy - API Test Client")
        self.build_ui()

    def build_ui(self):
        tab_control = ttk.Notebook(self.root)

        # Single Request Tab
        self.single_tab = ttk.Frame(tab_control)
        tab_control.add(self.single_tab, text='Single Request')
        self.build_single_request_ui(self.single_tab)

        # Batch Request Tab
        self.batch_tab = ttk.Frame(tab_control)
        tab_control.add(self.batch_tab, text='Batch Request')
        self.build_batch_request_ui(self.batch_tab)

        tab_control.pack(expand=1, fill='both')

    # ---------------- Single Request UI ----------------
    def build_single_request_ui(self, parent):
        ttk.Label(parent, text="URL:").grid(row=0, column=0, sticky="w")
        self.url_entry = ttk.Entry(parent, width=60)
        self.url_entry.grid(row=0, column=1)

        ttk.Label(parent, text="Method:").grid(row=1, column=0, sticky="w")
        self.method_var = tk.StringVar(value="GET")
        ttk.Combobox(parent, textvariable=self.method_var, values=["GET", "POST", "PUT", "DELETE"]).grid(row=1, column=1)

        ttk.Label(parent, text="Headers (JSON):").grid(row=2, column=0, sticky="nw")
        self.headers_text = tk.Text(parent, height=5, width=60)
        self.headers_text.grid(row=2, column=1)

        ttk.Label(parent, text="Body (JSON):").grid(row=3, column=0, sticky="nw")
        self.body_text = tk.Text(parent, height=5, width=60)
        self.body_text.grid(row=3, column=1)

        ttk.Button(parent, text="Send Request", command=self.send_single_request).grid(row=4, column=1, sticky="e")

        ttk.Label(parent, text="Response:").grid(row=5, column=0, sticky="nw")
        self.response_text = tk.Text(parent, height=10, width=60)
        self.response_text.grid(row=5, column=1)

    def send_single_request(self):
        url = self.url_entry.get()
        method = self.method_var.get()
        headers = self.headers_text.get("1.0", tk.END).strip()
        body = self.body_text.get("1.0", tk.END).strip()

        try:
            response = run_request(method, url, headers, body)
            self.response_text.delete("1.0", tk.END)

            # Try to pretty-print JSON
            try:
                parsed = response.json()
                pretty = json.dumps(parsed, indent=2)
            except Exception:
                pretty = response.text  # fallback to raw text

            self.response_text.insert(tk.END, f"Status: {response.status_code}\n\n{pretty}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- Batch Request UI ----------------
    def build_batch_request_ui(self, parent):
        ttk.Label(parent, text="URL:").grid(row=0, column=0, sticky="w")
        self.batch_url_entry = ttk.Entry(parent, width=60)
        self.batch_url_entry.grid(row=0, column=1)

        ttk.Label(parent, text="Method:").grid(row=1, column=0, sticky="w")
        self.batch_method_var = tk.StringVar(value="POST")
        ttk.Combobox(parent, textvariable=self.batch_method_var, values=["POST", "PUT", "DELETE"]).grid(row=1, column=1)

        ttk.Label(parent, text="Headers (JSON):").grid(row=2, column=0, sticky="nw")
        self.batch_headers_text = tk.Text(parent, height=5, width=60)
        self.batch_headers_text.grid(row=2, column=1)

        ttk.Label(parent, text="Body Template (JSON with {{variables}}):").grid(row=3, column=0, sticky="nw")
        self.batch_body_text = tk.Text(parent, height=5, width=60)
        self.batch_body_text.grid(row=3, column=1)

        ttk.Label(parent, text="CSV File:").grid(row=4, column=0, sticky="w")
        self.csv_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.csv_path_var, width=50).grid(row=4, column=1, sticky="w")
        ttk.Button(parent, text="Browse", command=self.browse_csv).grid(row=4, column=1, sticky="e")

        ttk.Button(parent, text="Run Batch", command=self.run_batch).grid(row=5, column=1, sticky="e")

        ttk.Label(parent, text="Batch Output:").grid(row=6, column=0, sticky="nw")
        self.batch_output_text = tk.Text(parent, height=10, width=60)
        self.batch_output_text.grid(row=6, column=1)

        ttk.Label(parent, text="CSV File:").grid(row=4, column=0, sticky="w")
        self.csv_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.csv_path_var, width=50).grid(row=4, column=1, sticky="w")
        ttk.Button(parent, text="Browse", command=self.browse_csv).grid(row=4, column=1, sticky="e")

        ttk.Button(parent, text="Run Batch", command=self.run_batch).grid(row=5, column=1, sticky="e")

        ttk.Label(parent, text="Batch Output:").grid(row=6, column=0, sticky="nw")
        self.batch_output_text = tk.Text(parent, height=10, width=60)
        self.batch_output_text.grid(row=6, column=1)

    def browse_template(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.template_path_var.set(path)

    def browse_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.csv_path_var.set(path)

    def run_batch(self):
        url = self.batch_url_entry.get()
        method = self.batch_method_var.get()
        headers = self.batch_headers_text.get("1.0", tk.END).strip()
        body_template = self.batch_body_text.get("1.0", tk.END).strip()
        csv_path = self.csv_path_var.get()

        try:
            results = run_batch_requests(method, url, headers, body_template, csv_path)
            self.batch_output_text.delete("1.0", tk.END)
            for i, result in enumerate(results, start=1):
                self.batch_output_text.insert(tk.END, f"\nRequest {i}:\n{result}\n")
        except Exception as e:
            messagebox.showerror("Batch Error", str(e))