from api.sockg import SOCKG

sockg = SOCKG("https://frink.apps.renci.org/sockg/sparql")

print(f"Classes: {sockg.get_all_classes()}")

print(f"Relations: {sockg.get_all_edges()}")

print(f"Instances count of 'WeatherObservation': {sockg.get_instance_count('WeatherObservation')}")

print(f"Data properties of 'WeatherObservation': {sockg.get_data_properties_from_class('WeatherObservation')}")

print(f"Object properties of 'WeatherObservation': {sockg.get_object_properties_from_class('WeatherObservation')}")