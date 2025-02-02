import dash
from dash import dcc, html, Output, Input, State
import os
import base64
import ai

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file(contents, filename):
    """Save uploaded file to the uploads folder."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(decoded)
    return file_path


app = dash.Dash(__name__)

def serve_layout():
    return html.Div([
        html.H1("Recipe from Image", style={'textAlign': 'center'}),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='image-preview'),
        html.H2("Recipe"),
        html.Div(id='recipeName'),
    
    ])

app.layout = serve_layout

@app.callback(
    Output('image-preview', 'children'),
    Input('upload-image', 'contents'),
)
def update_output(contents):
    if contents is not None:
        children = [
            html.Img(src=contents)
        ]
        return children
    return None

@app.callback(
    Output('recipeName', 'children'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('upload-image', 'last_modified')
)   


def display_recipe(contents, filename, date):
    if contents is not None:
        image_data = contents.split(',')[1]
        image_path = "img/" + filename + str(date)
        
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        recipe = ai.generate_recipe(image_path)


        if not all(key in recipe for key in ('name', 'ingredients', 'instructions')):
            return html.Div("Error: Recipe data is incomplete or invalid.")
        print(recipe)

        # Display the uploaded image
        

        return [
            html.H3(recipe['name']),
            html.H4("Ingredients"),
            html.Ol([html.Li(f'{i["name"]} - {i["quantity"]}') for i in recipe['ingredients']]),

            html.H4("Instructions"),
            html.Ol([html.Li(i) for i in recipe['instructions']])
        ]

   
if __name__ == '__main__':
    app.run_server(debug=True)
