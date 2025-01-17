import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# Folder path
folder_path = r"C:\Users\DanGulyas\OneDrive - MOLGROUP\Work\Cikkszám osztályozás riportok\Dashboard\ZWSR"


# Function to get all Excel files from the folder
def get_excel_files(folder_path):
    files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(".xlsx")
    ]
    return files


# Function to load data from a specific file
def load_data(file_path):
    sheet_name = "Red Filled Empty Cell Counts"  # Update the sheet name if necessary
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df


# Map file names to their paths dynamically
excel_files = get_excel_files(folder_path)
file_paths = {
    os.path.basename(file).replace(".xlsx", ""): file for file in excel_files
}

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Red Filled Empty Cells Count Dashboard",
        style={"textAlign": "center"}  # Center-align the title
    ),
    html.Label("Select File:", style={"font-weight": "bold", "margin-top": "20px"}),
    dcc.Dropdown(
        id="file-dropdown",
        options=[{"label": key, "value": key} for key in file_paths.keys()],
        value=list(file_paths.keys())[0],  # Default to the first file
        style={"width": "50%", "margin": "auto"}  # Center-align the dropdown
    ),
    dcc.Graph(id="bar-chart")
])


# Callback to update the bar chart based on selected file
@app.callback(
    Output("bar-chart", "figure"),
    [Input("file-dropdown", "value")]
)
def update_chart(selected_file):
    # Load the selected file's data
    file_path = file_paths[selected_file]
    df = load_data(file_path)

    # Create bar chart with conditional coloring
    fig = px.bar(
        df,
        x="Column",
        y="Red Filled Empty Cells Count",
        color="Red Filled Empty Cells Count",  # Use value for coloring
        color_continuous_scale=px.colors.sequential.Blues,  # Use a blue gradient
        title=f"Red Filled Empty Cells Count ({selected_file})",
        labels={"Red Filled Empty Cells Count": "Empty Cells Count"}
    )
    fig.update_layout(
        xaxis_tickangle=-45,  # Rotate x-axis labels for readability
        title={"text": f"Red Filled Empty Cells Count ({selected_file})", "x": 0.5},  # Center the chart title
        coloraxis_colorbar={"title": "Empty Cells Count"},  # Add colorbar title
    )
    # Adjust color scale to avoid overly white bars for small values
    fig.update_traces(marker=dict(cmin=0, cmax=df["Red Filled Empty Cells Count"].max() * 0.9))  # Limit deviation

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
