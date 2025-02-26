import numpy as np
import streamlit as st

def main():
    st.title("Matrix Pseudo-Inverse Calculator")
    st.write("Enter the dimensions and values of your matrix. The pseudo-inverse is computed using a robust SVD method, so singular matrices are handled gracefully.")

    with st.form(key="matrix_form"):
        # Matrix dimensions input
        m = st.number_input("Rows (m):", min_value=1, value=2, step=1)
        n = st.number_input("Columns (n):", min_value=1, value=2, step=1)
        
        st.write("Enter the matrix entries:")
        matrix_entries = []
        # Create a grid for matrix entries using Streamlit columns
        for i in range(m):
            row_entries = []
            cols = st.columns(n)
            for j in range(n):
                entry = cols[j].text_input(label=f"Entry ({i+1},{j+1})", value="0", key=f"{i}_{j}")
                row_entries.append(entry)
            matrix_entries.append(row_entries)
        
        submit_button = st.form_submit_button(label="Calculate Pseudo-Inverse")

    if submit_button:
        try:
            # Convert entries to a NumPy array of floats
            A = np.array([[float(item) for item in row] for row in matrix_entries])
        except ValueError:
            st.error("Please ensure all matrix entries are valid numbers.")
            return
        
        try:
            # Use NumPy's pinv function to compute the pseudo-inverse robustly
            A_plus = np.linalg.pinv(A)
            st.subheader("Pseudo-Inverse:")
            for row in A_plus:
                st.write("  ".join(f"{num:.4f}" for num in row))
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
