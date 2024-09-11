from api.sockg import SOCKG

sockg = SOCKG("https://frink.apps.renci.org/sockg/sparql")

node_types = sockg.get_nodes()