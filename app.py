from flask import Flask, render_template
from api.sockg import SOCKG

# Need to be replaced with environment variable
SPARQL_ENDPOINT = "https://frink.apps.renci.org/sockg/sparql"

app = Flask(__name__)

@app.route('/')
def home():
    
    # Initialize the SOCKG class
    sockg = SOCKG(SPARQL_ENDPOINT)
    
    # Get VisJS graph format
    visjs_graph = sockg.getVisJsGraph()
    return render_template('home.html', node_list = visjs_graph['nodes'], edge_list = visjs_graph['edges'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/get_node_attributes/<node_id>', methods=['GET'])
def get_node_attributes_route(node_id):
    sockg = SOCKG(SPARQL_ENDPOINT)
    attributes = sockg.get_node_attributes(node_id)
    return (attributes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
