import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('todo_list.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY, 
              title TEXT NOT NULL, 
              description TEXT, 
              priority INTEGER, 
              due_date TEXT, 
              completed INTEGER)''')
conn.commit()

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x400")

        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.filter_var = tk.StringVar()

        self.create_widgets()
        self.view_tasks()

    def create_widgets(self):
        tk.Label(self.root, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.title_var, width=50).grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(self.root, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.desc_var, width=50).grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(self.root, text="Priority (1-5):").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.priority_var, width=50).grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.due_date_var, width=50).grid(row=3, column=1, padx=10, pady=10, sticky='w')

        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Update Task", command=self.update_task).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=4, column=2, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('ID', 'Title', 'Description', 'Priority', 'Due Date', 'Completed'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Completed', text='Completed')
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.tree.bind('<ButtonRelease-1>', self.select_task)

        tk.Label(self.root, text="Filter by Due Date (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.filter_var, width=50).grid(row=6, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.root, text="Filter Tasks", command=self.filter_tasks).grid(row=6, column=2, padx=10, pady=10)

    def add_task(self):
        title = self.title_var.get()
        description = self.desc_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()

        if not title or not priority or not due_date:
            messagebox.showerror("Error", "Title, Priority, and Due Date are required!")
            return

        try:
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Error", "Priority must be an integer!")
            return

        c.execute("INSERT INTO tasks (title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, 0)",
                  (title, description, priority, due_date))
        conn.commit()
        self.view_tasks()

    def update_task(self):
        selected_item = self.tree.selection()[0]
        task_id = self.tree.item(selected_item)['values'][0]

        title = self.title_var.get()
        description = self.desc_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()

        if not title or not priority or not due_date:
            messagebox.showerror("Error", "Title, Priority, and Due Date are required!")
            return

        try:
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Error", "Priority must be an integer!")
            return

        c.execute("UPDATE tasks SET title = ?, description = ?, priority = ?, due_date = ? WHERE id = ?",
                  (title, description, priority, due_date, task_id))
        conn.commit()
        self.view_tasks()

    def delete_task(self):
        selected_item = self.tree.selection()[0]
        task_id = self.tree.item(selected_item)['values'][0]

        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        self.view_tasks()

    def view_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        c.execute("SELECT * FROM tasks")
        rows = c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def select_task(self, event):
        selected_item = self.tree.selection()[0]
        task = self.tree.item(selected_item)['values']

        self.title_var.set(task[1])
        self.desc_var.set(task[2])
        self.priority_var.set(task[3])
        self.due_date_var.set(task[4])

    def filter_tasks(self):
        filter_date = self.filter_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        c.execute("SELECT * FROM tasks WHERE due_date = ?", (filter_date,))
        rows = c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
    conn.close()
