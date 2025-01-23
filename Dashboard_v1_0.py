import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Map file names to their Dropbox URLs with updated keys
file_paths = {
    "ZWSR_Report_0114": "https://www.dropbox.com/scl/fi/nlx4tcznfmemrr5ehw518/ZWSR_osztalyozas_matrix_0114_riport.xlsx?rlkey=sqc1xavcrv03q4gm6mf3wy3dq&e=1&st=8tltdyks&raw=1",
    "ZWSR_Report_0116": "https://www.dropbox.com/scl/fi/6nr5b9w38uvhaj4qp5l53/ZWSR_osztalyozas_matrix_0116_riport.xlsx?rlkey=ljjlmu0r7vtm47fidh08colq0&st=6ogz28wo&raw=1",
    "ZWSR_Report_0122": "https://www.dropbox.com/scl/fi/sx89joup2q8tcnihkc1ch/ZWSR_osztalyozas_matrix_0122_report.xlsx?rlkey=c1wqtbiq5sg951nv473yv7ru5&st=n9k9ktlo&raw=1",
    "ZWSR_Report_0123": "https://www.dropbox.com/scl/fi/fl0sbhzzbxi2ajqtw8p0w/ZWSR_osztalyozas_matrix_0123_report.xlsx?rlkey=my53vtbee905ckvh8chrme4y4&st=6qodv1kq&raw=1"
}

# Function to load data from a specific file
def load_data(file_path):
    sheet_name = "Red Filled Empty Cell Counts"  # Update the sheet name if necessary
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')  # Specify engine
    return df

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Expose Flask server for deployment

# App Layout
app.layout = html.Div([
    html.H1(
        "Osztályjellemzők hibás rekordjainak száma",
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
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)

