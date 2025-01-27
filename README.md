# PREMIS Events 

Deze repository bevat beschrijft hoe in het RAZU e-depot PREMIS events in RDF worden vastgelegd. Het biedt SHACL shapes ter validatie van die events, een python script om de SHACL toe te passen en een PyTest script om de SHACL te controleren.

Deze documentatie heeft in deze fase alleen nog betrekking op de ingest-fase.

## Structuur

De repository bestaat uit de volgende mappen en bestanden:

- [premis_events](premis_events.md): de beschrijving van de PREMIS events die in het RAZU e-depot gebruikt worden.
- [shacl](shacl/premis-shacl.ttl): SHACL shapes ter validatie van PREMIS events.
- [validator](scripts/validate.py): een python script om de SHACL te gebruiken om PREMIS events te valideren.
- [tests](tests/): PyTest tests om de SHACL te controleren.


