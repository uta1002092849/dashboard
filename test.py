from api.sockg import SOCKG

sockg = SOCKG("https://frink.apps.renci.org/sockg/sparql")

print(sockg.get_data_properties_from_class("WeatherObservation"))