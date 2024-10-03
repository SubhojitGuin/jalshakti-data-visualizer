import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Function to plot based on user's selection
def plot_graph(df, x_col, y_col, plot_type):
    fig, ax = plt.subplots()
    try:
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
        plt.xticks(rotation=90)
        st.pyplot(fig)
        return fig
    except KeyError as e:
        st.error(f"Error: Column not found - {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to convert plot to .png
def download_plot(fig):
    buffer = BytesIO()
    try:
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error saving plot: {e}")

# Streamlit App
st.title("Plot Generator from CSV/XLSX")

# Uploading the file
uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        # Handling file upload and checking format
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or XLSX file.")
            st.stop()

        # Check if the file is empty
        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid file.")
            st.stop()

        # Displaying columns to choose from
        columns = df.columns.tolist()
        if not columns:
            st.error("No columns found in the uploaded file.")
            st.stop()

        x_column = st.selectbox("Select the X-axis column", columns)
        y_column = st.selectbox("Select the Y-axis column", columns)

        # Dropdown for plot type
        plot_type = st.selectbox("Select the type of plot", ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram"])

        # Submit button
        if st.button("Generate Plot"):
            if x_column and y_column:
                fig = plot_graph(df, x_column, y_column, plot_type)

                if fig:
                    # Adding a download button for the plot
                    buffer = download_plot(fig)
                    if buffer:
                        st.download_button(label="Download Plot as PNG", data=buffer, file_name='plot.png', mime='image/png')
            else:
                st.error("Please select valid columns for X and Y axes.")

    except pd.errors.EmptyDataError:
        st.error("The file is empty or improperly formatted.")
    except pd.errors.ParserError:
        st.error("Error parsing file. Please ensure the file is a valid CSV or XLSX format.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
