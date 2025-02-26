import tkinter as tk
from tkinter import ttk

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def matrix_mult(a, b):
    return [[sum(a_row[k] * b[k][col] for col in range(len(b[0]))] 
            for a_row in a for k in range(len(b)))]

def determinant(mat):
    if len(mat) == 1:
        return mat[0][0]
    return sum((-1)**c * mat[0][c] * determinant([row[:c]+row[c+1:] for row in mat[1:]]) 
              for c in range(len(mat)))

def inverse(mat):
    det = determinant(mat)
    if det == 0:
        raise ValueError("Matrix is singular")
    n = len(mat)
    adj = [[(-1)**(i+j) * determinant([row[:j]+row[j+1:] for r, row in enumerate(mat) if r != i])
            for i in range(n)] for j in range(n)]
    adj = transpose(adj)
    return [[adj[i][j]/det for j in range(n)] for i in range(n)]

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Pseudo-Inverse Calculator")
        
        # Matrix dimension inputs
        ttk.Label(root, text="Rows (m):").grid(row=0, column=0)
        self.m_entry = ttk.Entry(root)
        self.m_entry.grid(row=0, column=1)
        
        ttk.Label(root, text="Columns (n):").grid(row=1, column=0)
        self.n_entry = ttk.Entry(root)
        self.n_entry.grid(row=1, column=1)
        
        # Matrix input frame
        self.input_frame = ttk.Frame(root)
        self.input_frame.grid(row=2, column=0, columnspan=2)
        
        # Result display
        self.result_label = ttk.Label(root, text="Pseudo-Inverse:")
        self.result_text = tk.Text(root, height=5, width=40)
        
        # Buttons
        ttk.Button(root, text="Create Matrix", command=self.create_matrix_input).grid(row=3, column=0, columnspan=2)
        ttk.Button(root, text="Calculate", command=self.calculate_pseudo_inverse).grid(row=4, column=0, columnspan=2)

    def create_matrix_input(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
        try:
            self.m = int(self.m_entry.get())
            self.n = int(self.n_entry.get())
        except:
            return
            
        self.matrix_entries = []
        for i in range(self.m):
            row_entries = []
            for j in range(self.n):
                entry = ttk.Entry(self.input_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def get_matrix(self):
        matrix = []
        for row_entries in self.matrix_entries:
            row = []
            for entry in row_entries:
                try:
                    row.append(float(entry.get()))
                except:
                    row.append(0.0)
            matrix.append(row)
        return matrix

    def calculate_pseudo_inverse(self):
        try:
            A = self.get_matrix()
            A_T = transpose(A)
            ATA = matrix_mult(A_T, A)
            ATA_inv = inverse(ATA)
            A_plus = matrix_mult(ATA_inv, A_T)
            
            # Display results
            self.result_label.grid(row=5, column=0, columnspan=2)
            self.result_text.grid(row=6, column=0, columnspan=2)
            self.result_text.delete(1.0, tk.END)
            for row in A_plus:
                self.result_text.insert(tk.END, "  ".join(f"{num:.4f}" for num in row) + "\n")
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()
