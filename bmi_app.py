import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def get_bmi_category(bmi):
    """Return BMI category and color for visualization."""
    if bmi < 18.5:
        return "Underweight", "skyblue"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight", "lightgreen"
    elif 25 <= bmi < 29.9:
        return "Overweight", "orange"
    else:
        return "Obese", "red"

def calculate_bmi():
    try:
        username = entry_name.get().strip()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if not username:
            messagebox.showwarning("Input Error", "Please enter a username")
            return

        bmi = round(weight / ((height / 100) ** 2), 2)
        category, color = get_bmi_category(bmi)
        label_result.config(text=f"{username}'s BMI: {bmi} ({category})", bg=color)

        # Save record
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO bmi_records (username, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
            (username, weight, height, bmi, category, date)
        )
        conn.commit()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

def view_history():
    username = entry_name.get().strip()
    if not username:
        messagebox.showwarning("Input Error", "Please enter a username")
        return

    cursor.execute(
        "SELECT date, weight, height, bmi, category FROM bmi_records WHERE username=? ORDER BY date",
        (username,)
    )
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Data", f"No records found for {username}")
        return

    history_window = tk.Toplevel(root)
    history_window.title(f"{username}'s BMI History")
    history_window.geometry("500x300")

    tree = ttk.Treeview(history_window, columns=("Date", "Weight", "Height", "BMI", "Category"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height", text="Height (cm)")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")

    for rec in records:
        tree.insert("", tk.END, values=rec)

    tree.pack(expand=True, fill="both")

def show_trend():
    username = entry_name.get().strip()
    if not username:
        messagebox.showwarning("Input Error", "Please enter a username")
        return

    cursor.execute(
        "SELECT date, bmi FROM bmi_records WHERE username=? ORDER BY date",
        (username,)
    )
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Data", f"No records found for {username}")
        return

    dates = [r[0] for r in records]
    bmis = [r[1] for r in records]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, bmis, marker="o", linestyle="-", color="purple", label="BMI")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI Trend for {username}")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ---------------- TOOLTIP FUNCTION ----------------
class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="lightyellow", relief='solid', borderwidth=1,
                         font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Interactive BMI Calculator")
root.geometry("500x450")
root.resizable(False, False)
root.configure(bg="#f0f2f5")

# Title
title = tk.Label(root, text="BMI Calculator with History & Trends", font=("Helvetica", 16, "bold"), bg="#f0f2f5")
title.pack(pady=10)

# Input frame
frame_input = tk.LabelFrame(root, text="User Details", padx=20, pady=20, bg="#f0f2f5")
frame_input.pack(padx=10, pady=10, fill="x")

tk.Label(frame_input, text="Username:", bg="#f0f2f5").grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(frame_input, width=35)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame_input, text="Weight (kg):", bg="#f0f2f5").grid(row=1, column=0, sticky="w", pady=5)
entry_weight = tk.Entry(frame_input, width=35)
entry_weight.grid(row=1, column=1, pady=5)

tk.Label(frame_input, text="Height (cm):", bg="#f0f2f5").grid(row=2, column=0, sticky="w", pady=5)
entry_height = tk.Entry(frame_input, width=35)
entry_height.grid(row=2, column=1, pady=5)

# Buttons
frame_buttons = tk.Frame(root, bg="#f0f2f5")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Calculate BMI", width=18, command=calculate_bmi, bg="#4caf50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="View History", width=18, command=view_history, bg="#2196f3", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Show Trend", width=18, command=show_trend, bg="#ff9800", fg="white").grid(row=0, column=2, padx=5)

# Result label
label_result = tk.Label(root, text="BMI: --", font=("Helvetica", 14, "bold"), bg="#f0f2f5", width=50)
label_result.pack(pady=20)

# BMI Category Guide
guide_frame = tk.LabelFrame(root, text="BMI Categories Guide", padx=10, pady=10, bg="#f0f2f5")
guide_frame.pack(padx=10, pady=10, fill="x")

categories = [("Underweight", "skyblue"), ("Normal weight", "lightgreen"), ("Overweight", "orange"), ("Obese", "red")]
for idx, (cat, color) in enumerate(categories):
    lbl = tk.Label(guide_frame, text=cat, bg=color, width=15)
    lbl.grid(row=0, column=idx, padx=5, pady=5)
    ToolTip(lbl, f"{cat} BMI range")

root.mainloop()
