import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Function to plot based on user's selection
def plot_graph(df, x_col, y_col, plot_type):
    fig, ax = plt.subplots()
    if plot_type == "Line Plot":
        ax.plot(df[x_col], df[y_col], marker='o')
    elif plot_type == "Bar Plot":
        ax.bar(df[x_col], df[y_col])
    elif plot_type == "Scatter Plot":
        ax.scatter(df[x_col], df[y_col])
    elif plot_type == "Histogram":
        ax.hist(df[y_col], bins=20)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f'{plot_type} of {y_col} vs {x_col}')
    st.pyplot(fig)
    return fig

# Function to convert plot to .png
def download_plot(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

# Streamlit App
st.set_page_config("JalSarthi Report Visualizer")
st.title("JalSarthi Report Visualizer")
st.subheader("Visualize your data with JalSarthi💁")

# Uploading the file
uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Displaying columns to choose from
        columns = df.columns.tolist()
        x_column = st.selectbox("Select the X-axis column", columns)
        y_column = st.selectbox("Select the Y-axis column", columns)

        # Dropdown for plot type
        plot_type = st.selectbox("Select the type of plot", ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram"])

        # Submit button
        if st.button("Generate Plot"):
            fig = plot_graph(df, x_column, y_column, plot_type)

            # Adding a download button for the plot
            buffer = download_plot(fig)
            st.download_button(label="Download Plot as PNG", data=buffer, file_name='plot.png', mime='image/png')
    
    except Exception as e:
        st.error(f"Error: {e}")
