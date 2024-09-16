from flask import Flask, render_template, jsonify, request
from api.sockg import SOCKG

# Need to be replaced with environment variable
SPARQL_ENDPOINT = "https://frink.apps.renci.org/sockg/sparql"
app = Flask(__name__)
sockg = SOCKG(SPARQL_ENDPOINT)

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
    attributes = sockg.get_data_property(node_id)
    return (attributes)

@app.route('/get_node_instances/<node_type>', methods=['GET'])
def get_node_instance_route(node_type):
    sockg = SOCKG(SPARQL_ENDPOINT)
    instances = sockg.get_node_instance(node_type)
    return (instances)


# start of REST API endpoints
# Route to get all classes
@app.route('/get_all_classes', methods=['GET'])
def get_all_classes():
    classes = sockg.get_all_classes()
    return jsonify(classes)

# Route to get all edges
@app.route('/get_all_edges', methods=['GET'])
def get_all_edges():
    edges = sockg.get_all_edges()
    return jsonify(edges)

# Route to get instance count for a given class type
@app.route('/get_instance_count', methods=['GET'])
def get_instance_count():
    class_type = request.args.get('class_type')
    result = sockg.get_instance_count(class_type)
    return jsonify(result)

# Route to get data properties from a class type
@app.route('/get_data_properties_from_class', methods=['GET'])
def get_data_properties_from_class():
    class_type = request.args.get('class_type')
    print(class_type)
    result = sockg.get_data_properties_from_class(class_type)
    return jsonify(result)

# Route to get node instances from a class with pagination (limit and offset)
@app.route('/get_node_instance_from_class', methods=['GET'])
def get_node_instance_from_class():
    class_type = request.args.get('class_type')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    result = sockg.get_node_instance_from_class(class_type, limit, offset)
    return jsonify(result)

# Route to get data properties for a node instance
@app.route('/get_data_property_from_instance', methods=['GET'])
def get_data_property_from_instance():
    node_uri = request.args.get('node_uri')
    result = sockg.get_data_property_from_instance(node_uri)
    return jsonify(result)

# Route to get object properties for a node instance
@app.route('/get_object_property_from_instance', methods=['GET'])
def get_object_property_from_instance():
    node_uri = request.args.get('node_uri')
    result = sockg.get_object_property_from_instance(node_uri)
    return jsonify(result)

# Route to get class type from a node instance
@app.route('/get_class_type_from_instance', methods=['GET'])
def get_class_type_from_instance():
    node_uri = request.args.get('node_uri')
    result = sockg.get_class_type_from_instance(node_uri)
    return jsonify(result)

# Route to get all experimental units for a field
@app.route('/get_all_experimentalUnit_for_field', methods=['GET'])
def get_all_experimentalUnit_for_field():
    field_instance = request.args.get('field_instance')
    result = sockg.get_all_experimentalUnit_for_field(field_instance)
    return jsonify(result)

# Route to get all soil physical samples for an experimental unit
@app.route('/get_all_soilPhysicalSample_for_expUnit', methods=['GET'])
def get_all_soilPhysicalSample_for_expUnit():
    expUnit_instance = request.args.get('expUnit_instance')
    result = sockg.get_all_soilPhysicalSample_for_expUnit(expUnit_instance)
    return jsonify(result)

# Route to get all soil chemical samples for an experimental unit
@app.route('/get_all_soilChemicalSample_for_expUnit', methods=['GET'])
def get_all_soilChemicalSample_for_expUnit():
    expUnit_instance = request.args.get('expUnit_instance')
    result = sockg.get_all_soilChemicalSample_for_expUnit(expUnit_instance)
    return jsonify(result)

# Route to get all soil biological samples for an experimental unit
@app.route('/get_all_soilBiologicalSample_for_expUnit', methods=['GET'])
def get_all_soilBiologicalSample_for_expUnit():
    expUnit_instance = request.args.get('expUnit_instance')
    result = sockg.get_all_soilBiologicalSample_for_expUnit(expUnit_instance)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
