import tkinter as tk
from tkinter import ttk, filedialog

class ReportForm:
    def __init__(self, root, report_controller, on_home):
        self.root = root
        self.report_controller = report_controller

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Reports", font=("Arial", 30, "bold"),
                 bg="#A8A8AD").pack(pady=20)

        tk.Label(frame, text="Select Sample ID:", font=("Arial", 14),
                 bg="#A8A8AD").pack()

        self.sample_combo = ttk.Combobox(frame, width=30)
        self.sample_combo.pack(pady=10)

        # ✅ تحميل sample IDs (مع حل الفراغ)
        try:
            samples = self.report_controller.dao.get_all_results()
            ids = list(set([s["sample_id"] for s in samples]))

            if not ids:
                ids = ["S001"]  # fallback

            self.sample_combo["values"] = ids

        except:
            self.sample_combo["values"] = ["S001"]

        tk.Button(frame, text="View Report", font=("Arial", 14),
                  command=self.view_report).pack(pady=10)

        self.text = tk.Text(frame, height=10, width=70)
        self.text.pack(pady=10)

        tk.Button(frame, text="Export to TXT", font=("Arial", 14),
                  command=self.export).pack(pady=5)

        tk.Button(frame, text="Home", font=("Arial", 16),
                  bg="white",
                  command=on_home).pack(pady=20)

    def view_report(self):
        sample_id = self.sample_combo.get()
        if not sample_id:
            return

        results = self.report_controller.get_results_by_sample(sample_id)

        self.text.delete("1.0", tk.END)

        if not results:
            self.text.insert(tk.END, "No results found")
            return

        for r in results:
            # ✅ استخدم test_id إذا test_name مو موجود
            line = f"{r.get('test_name', r.get('test_id'))}: {r['result_value']}\n"
            self.text.insert(tk.END, line)

    def export(self):
        sample_id = self.sample_combo.get()
        if not sample_id:
            return

        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not path:
            return

        results = self.report_controller.get_results_by_sample(sample_id)

        with open(path, "w") as f:
            if not results:
                f.write("No results found")
            else:
                for r in results:
                    line = f"{r.get('test_name', r.get('test_id'))}: {r['result_value']}\n"
                    f.write(line)