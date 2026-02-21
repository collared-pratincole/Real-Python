import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import subprocess
import sys
import os

def snake_to_python(code):
    replacements = {
        "🐍🐍🐍🐍🐍": "def",
        "🐍👑": "return",
        "🐍🐍🐍": "if",
        "🐍🐍🐍🐍": "else",
        "🐍🐍🐍🐍🐍🐍": "for",
        "🐍": "print",
        "🐍👑🐍👑🐍👑": "=",
        "🐍🐍🐍👑": "+",
        "🐍🐍🐍👑🐍": "-",
        "🐍🐍🐍👑🐍👑": "*",
        "🐍🐍🐍👑🐍👑🐍": "/",
        "🐍🐍👑🐍👑": "==",
        "🐍🐍👑🐍👑🐍": "!=",
        "🐍🐍👑🐍👑🐍👑": ">",
        "🐍🐍👑🐍👑🐍👑🐍": "<",
        "🐍🐍👑": "True",
        "🐍🐍👑🐍": "False",
        "🐍非": "not",
        "🐍且": "and",
        "🐍或": "or",
    }
    for snake, py in replacements.items():
        code = code.replace(snake, py)
    return code

class SnakeIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 蛇语 IDE")
        self.root.geometry("900x600")

        # 菜单栏
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="新建", command=self.new_file)
        filemenu.add_command(label="打开", command=self.open_file)
        filemenu.add_command(label="保存", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)

        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="运行蛇语代码", command=self.run_snake_code)
        menubar.add_cascade(label="运行", menu=runmenu)

        root.config(menu=menubar)

        # IDE
        self.editor_frame = tk.Frame(root)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        self.editor_label = tk.Label(self.editor_frame, text="🐍 蛇语代码编辑器")
        self.editor_label.pack(anchor="w", padx=5, pady=2)

        self.text_area = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 运行button
        self.run_btn = tk.Button(
            root,
            text="▶️ 运行蛇语代码",
            command=self.run_snake_code,
            bg="#4CAF50",
            fg="white",
            font=("黑体", 12, "bold")
        )
        self.run_btn.pack(pady=5)

        # 输出
        self.output_frame = tk.Frame(root)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_label = tk.Label(self.output_frame, text="📝 运行输出")
        self.output_label.pack(anchor="w", padx=5, pady=2)

        self.output_area = scrolledtext.ScrolledText(
            self.output_frame,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=("Consolas", 10),
            state="disabled"
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.current_file = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("🐍 蛇语 IDE - 未命名")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".rpy",
            filetypes=[("蛇语文件", "*.rpy"), ("所有文件", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, content)
            self.current_file = file_path
            self.root.title(f"🐍 蛇语 IDE - {os.path.basename(file_path)}")

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("保存成功", f"已保存到: {self.current_file}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".snake",
            filetypes=[("蛇语文件", "*.rpy"), ("所有文件", "*.*")]
        )
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.current_file = file_path
            self.root.title(f"🐍 蛇语 IDE - {os.path.basename(file_path)}")
            messagebox.showinfo("保存成功", f"已保存到: {file_path}")

    def run_snake_code(self):
        snake_code = self.text_area.get(1.0, tk.END)
        if not snake_code.strip():
            messagebox.showwarning("警告", "请先编写蛇语代码！")
            return

        try:
            python_code = snake_to_python(snake_code)
            temp_file = "__rpy_temp__.py"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(python_code)

            # 运行+输出
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

            self.output_area.config(state="normal")
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, "=== 翻译后的 Python 代码 ===\n")
            self.output_area.insert(tk.END, python_code + "\n\n")
            self.output_area.insert(tk.END, "=== 运行结果 ===\n")
            if result.stdout:
                self.output_area.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_area.insert(tk.END, "错误:\n" + result.stderr, "error")
            self.output_area.config(state="disabled")

            os.remove(temp_file)

        except Exception as e:
            self.output_area.config(state="normal")
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"运行出错: {str(e)}")
            self.output_area.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeIDE(root)
    root.mainloop()