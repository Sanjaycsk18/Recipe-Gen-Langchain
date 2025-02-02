from dash import Dash, html, dcc, Input, Output, State
import base64
from ai import generate_recipe

app = Dash(__name__)

def serve_layout():
    return html.Div([
        html.H1("Recipe from Image"),
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
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-image-upload'),
        html.H2("Recipe"),
        html.Div(id='recipe-output')
    ])

app.layout = serve_layout

@app.callback(
    Output('output-image-upload', 'children'),
    Input('upload-image', 'contents')
)
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = [
            html.Img(src=list_of_contents)
        ]
        return children
    return None

@app.callback(
    Output('recipe-output', 'children'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('upload-image', 'last_modified')
)
def display_recipe(contents,filename,date):
    
    if contents is not None:
        
        image_data = contents.split(',')[1]
        image_path = "img/" + filename + str(date)
        
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        
        recipe=generate_recipe(image_path)
        print(recipe)


        return [
            html.H3(recipe['name']),
            html.P(recipe['description']),
            html.H4("Ingredients"),
            html.Ol([html.Li(i) for i in recipe['ingredients']]),

            html.H4("Instructions"),
            html.Ol([html.Li(i) for i in recipe['instructions']])
        ]
    

if __name__ == '__main__':
    app.run_server(debug=False, host='localhost')