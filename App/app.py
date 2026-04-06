import tkinter as tk
from tkinter import filedialog, messagebox
from transform import process_file

def run_app():
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx")]
    )

    if file_path:
        try:
            output_path = process_file(file_path)
            messagebox.showinfo("Success", f"Output saved to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Real Estate Processor")
app.geometry("300x150")

label = tk.Label(app, text="Upload file and process")
label.pack(pady=10)

button = tk.Button(app, text="Select File & Run", command=run_app)
button.pack(pady=20)

app.mainloop()