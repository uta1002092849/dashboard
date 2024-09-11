from SPARQLWrapper import SPARQLWrapper, JSON
import collections

# SOCKG knowledge graph class
class SOCKG:
    def __init__(self, sparql_endpoint):
        
        # Initialize the SPARQLWrapper with the endpoint URL
        self.sparql = SPARQLWrapper(sparql_endpoint)
        self.sparql.setReturnFormat(JSON)
        self.adjacency_list = collections.defaultdict(list)
        self.nodes_reference_links = {}
        
        # For pyvis graph, initialize to None if get_pyvis_graph is not called
        self.pyvis_knowledge_graph = None
        
        # Get the ontology graph
        self.get_ontology_graph()
        
    
    # Get the ontology graph
    def get_ontology_graph(self):
        # Define the SPARQL query to get all classes/or nodes types
        
        get_ontology_query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX type: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT DISTINCT
                (STRAFTER(STR(?start), "/soil-carbon-ontology/") AS ?startNodeType)
                (STRAFTER(STR(?rel), "/soil-carbon-ontology/") AS ?relationType)
                (STRAFTER(STR(?end), "/soil-carbon-ontology/") AS ?endNodeType)
                ?start_reference_link
                ?end_reference_link
            WHERE {
                
                # bind default reference to "Reference not available"
                BIND("Reference not available" AS ?default_reference_link)
                
                ?rel rdf:type owl:ObjectProperty .
                ?rel rdfs:domain ?start.
                ?rel rdfs:range ?end.
                ?start rdf:type owl:Class .
                ?end rdf:type owl:Class .
                
                OPTIONAL { ?start rdfs:seeAlso ?start_link . }
                OPTIONAL { ?end rdfs:seeAlso ?end_link . }
                
                bind(coalesce(?start_link, ?default_reference_link) as ?start_reference_link)
                bind(coalesce(?end_link, ?default_reference_link) as ?end_reference_link)
            }
        """
        
        # Run the query
        try:
            self.sparql.setQuery(get_ontology_query)
            results = self.sparql.queryAndConvert()
            for result in results["results"]["bindings"]:
                start_node_type = result["startNodeType"]["value"]
                relation = result["relationType"]["value"]
                end_node_type = result["endNodeType"]["value"]
                self.adjacency_list[start_node_type].append((relation, end_node_type))
                self.nodes_reference_links[start_node_type] = result["start_reference_link"]["value"]
                self.nodes_reference_links[end_node_type] = result["end_reference_link"]["value"]
        except Exception as e:
            print(f"Error retrieving knownledge graph schema: {e}")

    # Get a list of all nodes in the ontology graph
    def get_nodes(self):
        return list(self.adjacency_list.keys())

    # Get a list of all edges in the ontology graph
    def get_edges(self):
        return self.adjacency_list.get_edges()
    
    # Get a list of attributes for a given node
    def get_node_attributes(self, node):
        
        attributes = []
        if node not in self.get_nodes():
            print("Node type (Class) not found in the ontology graph")
        else:
            node_uri = "http://www.semanticweb.org/zzy/ontologies/2024/0/soil-carbon-ontology/" + node
            
            get_attributes_query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX type: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>

                SELECT DISTINCT
                (STRAFTER(STR(?node), "/soil-carbon-ontology/") AS ?nodeType)
                (STRAFTER(STR(?attri), "/soil-carbon-ontology/") AS ?attribute)
                (STRAFTER(STR(?datatype), "/XMLSchema#") AS ?dataType)
                ?reference_link
                WHERE {{
                    ?attri rdf:type owl:DatatypeProperty .
                    ?attri rdfs:domain <{node_uri}> .
                    ?attri rdfs:range ?datatype.
                    ?attri rdfs:seeAlso ?reference_link
                }}
            """.format(node_uri=node_uri)

            # Run the query
            try:
                self.sparql.setQuery(get_attributes_query)
                results = self.sparql.queryAndConvert()
                
                # A list of tuples containing the attribute name, data type, and reference link
                for result in results["results"]["bindings"]:
                    attribute = result["attribute"]["value"]
                    data_type = result["dataType"]["value"]
                    reference_link = result["reference_link"]["value"]
                    # format each row as a dictionary
                    row = {"name": attribute, "data_type": data_type, "reference_link": reference_link}
                    attributes.append(row)
                
            except Exception as e:
                print(f"Error retrieving attributes for node {node}: {e}")
        return attributes

    # Return visJs compatible format graph
    def getVisJsGraph(self):
        
        nodes, edges = [], []
        seen_nodes = set()
        
        for start_node in self.adjacency_list:
            for relation, end_node in self.adjacency_list[start_node]:
                if start_node not in seen_nodes:
                    nodes.append({"id": start_node, "label": start_node, "group": start_node})
                    seen_nodes.add(start_node)
                if end_node not in seen_nodes:
                    nodes.append({"id": end_node, "label": end_node, "group": end_node})
                    seen_nodes.add(end_node)
                edges.append({"from": start_node, "to": end_node, "title": relation, "arrows": "to"})
        return {"nodes": nodes, "edges": edges}
    
    # Given a node type, return all node instance belong to that type
    def get_node_instance(self, node_type):
        
        instances_uri = []
        if node_type not in self.get_nodes():
            print("Node type (Class) not found in the ontology graph")
        else:
            
            get_attributes_query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX onto: <http://www.semanticweb.org/zzy/ontologies/2024/0/soil-carbon-ontology/>

                SELECT ?instance_uri
                WHERE {{
                ?instance_uri rdf:type onto:{node_type} .
                }}
            """.format(node_type=node_type)

            # Run the query
            try:
                self.sparql.setQuery(get_attributes_query)
                results = self.sparql.queryAndConvert()
                
                # A list of tuples containing the attribute name, data type, and reference link
                for result in results["results"]["bindings"]:
                    uri = result["instance_uri"]["value"]
                    instances_uri.append(uri)
            except Exception as e:
                print(f"Error retrieving attributes for node {node_type}: {e}")
        return instances_uri




    
        
        