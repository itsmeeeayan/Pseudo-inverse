import streamlit as st

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def matrix_mult(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]

def determinant(mat):
    if len(mat) == 1:
        return mat[0][0]
    return sum(
        (-1) ** c * mat[0][c] * determinant([row[:c] + row[c+1:] for row in mat[1:]])
        for c in range(len(mat))
    )

def inverse(mat):
    det = determinant(mat)
    if det == 0:
        raise ValueError("Matrix is singular")
    n = len(mat)
    # Build the matrix of cofactors then transpose it to get the adjugate.
    adj = [
        [
            (-1) ** (i + j) * determinant(
                [row[:j] + row[j+1:] for r, row in enumerate(mat) if r != i]
            )
            for i in range(n)
        ]
        for j in range(n)
    ]
    adj = transpose(adj)
    return [[adj[i][j] / det for j in range(n)] for i in range(n)]

def calculate_pseudoinverse(A):
    A_T = transpose(A)
    ATA = matrix_mult(A_T, A)
    ATA_inv = inverse(ATA)
    A_plus = matrix_mult(ATA_inv, A_T)
    return A_plus

def main():
    st.title("Matrix Pseudo-Inverse Calculator")
    st.write("Enter the dimensions and values of the matrix to compute its pseudo-inverse.")

    with st.form(key="matrix_form"):
        # Matrix dimensions input
        m = st.number_input("Rows (m):", min_value=1, step=1, value=2)
        n = st.number_input("Columns (n):", min_value=1, step=1, value=2)
        
        st.write("Enter the matrix entries:")
        matrix = []
        # Create a grid for matrix entries using Streamlit columns
        for i in range(m):
            row = []
            cols = st.columns(n)
            for j in range(n):
                # Each entry is labeled with its row and column number
                entry = cols[j].text_input(f"({i+1},{j+1})", value="0")
                try:
                    row.append(float(entry))
                except ValueError:
                    row.append(0.0)
            matrix.append(row)
        
        submit_button = st.form_submit_button(label="Calculate Pseudo-Inverse")

    if submit_button:
        try:
            pseudo_inv = calculate_pseudoinverse(matrix)
            st.subheader("Pseudo-Inverse:")
            for row in pseudo_inv:
                st.write("  ".join(f"{num:.4f}" for num in row))
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
