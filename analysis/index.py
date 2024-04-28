from app import app
from analysis import layout

app.layout = layout

# main function
if __name__ == '__main__':
    app.run_server(debug=True, port=9000)
