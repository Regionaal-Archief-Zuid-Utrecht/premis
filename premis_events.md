# PREMIS events bij de ingest

Tijdens het ingest-proces wordt er een SIP (submission information package) gemaakt aan de hand van de aangeleverde bronbestanden. De bronbestanden doorlopen allerlei stappen gericht op het opbouwen van het SIP. Daarbij worden er ook nieuwe bestanden aangemaakt, de metadata-bestanden. Deze stappen worden vastgelegd in een PREMIS-eventlog in RDF. 

Dit document beschrijft hoe de stappen van het ingest-proces vastgelegd worden in een PREMIS-eventlog. We baseren ons hierbij op https://www.loc.gov/standards/premis/ontology/pdf/premis3-owl-guidelines-20180924.pdf en hebben ons daarbij laten inspireren door https://developer.meemoo.be/docs/metadata/knowledge-graph/0.0.1/events/en/

## URIs voor events

Er wordt per toegang / archief / dataset één eventlog gemaakt die als één bestand in RDF wordt weggeschreven. Een voorbeeld van een URI van zo'n bestand is	https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500.eventlog.json . Hierbij is 'K50907905' de code van de archiefvormer (NB: in onderkast gebruikt in de domeinnaam van de S3 bucket / CDN) en '500' de code van de dataset (toegang / archief).

De events zelf hebben URIs als https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e2421.  Het laatste deel van de URI eindigt op het teken 'e' gevolgd door een oplopend nummer.

## Afkadering objecten

De eventlog heeft betrekking op bestanden. Omdat we RDF hanteren worden bestanden geidenticeerd op basis van de URI's. De URI van een bestand in de URL van het bestand waarmee het uit het e-depot opvraagbaar is. Een voorbeeld van zo'n URI is https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf of https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.meta.json.

Deze URIs hebben óók betrekking op het bestand zoals ontvangen van de archiefvormer, ook als de bestandsnaam of locatie dan nog anders is dan de definitieve bestandsnaam en locatie. De URI is dus niet direct gerelateerd aan de originele naam van het bronbestand. Een afgeleid bestand, bijvoorbeeld een bestand in een andere bestandsformaat dat gemaakt wordt bij een preserveringsacties, is een ander object, en krijgt dus een nieuwe URI. Bronbestanden zelf worden nooit bewerkt.

Een metadata-bestand (dat geen bronbestand is), krijgt geen andere URI als de inhoud verandert, maar een dergelijke wijzinging van de inhoud wordt wel vastgelegd in de eventlog.


## De ingest in hoofdlijnen

Binnen het ingest-proces zijn een paar stappen te onderscheiden.

 1. Viruscheck en quarantaine
 De ontvangen bestanden worden in een afgeschermde omgeving ontvangen. Hierin worden de bestanden gecontroleerd op virusen. Het proces wordt alleen voortgezet als er binnen een vastgestelde quarantaine-periode geen virusen zijn gevonden.

 2. Bestandtype-identificatie
 Het (PRONOM) formaat van de bestanden wordt geidentificeerd, bijvoorbeeld met DROID.

 3. Opbouw SIP
 De SIP wordt opgebouwd. Hierbij worden de bronbestanden hernoemt, wordt een URI bepaald en worden de metadata-bestanden aangemaakt. In deze fase wordt de eventlog opgebouwd, waarbij ook de uitkomst van stappen 1. en 2. met de nu beschikbare URI's beschreven wordt. De SIP bevat naar bronbestanden, metadata-bestanden en een eventlog ook een manifest, dat aangeeft welke bestanden in de SIP te vinden moeten zijn.

Als de SIP afgerond is en gevalideerd dan kan deze naar de storage en backups opgebracht worden. De metadata kan geëxporteerd worden naar de triplestore en een Elastic Search zoekindex kan opgebouwd worden.


## Eventtypes

RAZU hanteert de PREMIS eventtypes http://id.loc.gov/vocabulary/preservation/eventType .

### Event voor bronbestanden

Voor ieder bronbestand zullen deze events vastgelegd worden:
- Een 'ins', ofwel ingest-start event (betreft stap 1)
- Een 'vir', ofwel viruscheck-event (betreft stap 1)
- Een 'for', ofwel bestandsidentificatie-event (betreft stap 2)
- Een 'mes', ofwel een event waarin een checksum vastgelegd (betreft stap 2)
- Een 'fil'-event, waarin de naam wordt genormaliseerd (deel stap 3)
- Een 'fix-event, waarin de checksum gevalideerd wordt (deel stap 3)
- Een 'ine'-event, waarmee de ingest beindigd wordt (einde stap 3)

### Events voor metadata-bestanden

De metadata-bestanden die deel uitmaken van het SIP worden aangemaakt in stap 3. Voor ieder metadata-bestand zullen de volgende events worden vastgelegd:

- Een 'mem'-event als het aangemaakt wordt
- Een 'ine'-event als de ingest beindigd wordt.


## Voorbeeld van events in RDF

### Prefixes

De volgende prefixes worden gebruikt:

    @prefix ns3: <http://id.loc.gov/vocabulary/preservation/eventRelatedObjectRole/> .
    @prefix ns1: <http://www.loc.gov/premis/rdf/v3/> .
    @prefix ns2: <http://id.loc.gov/vocabulary/preservation/eventRelatedAgentRole/> .
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

### 'ins'-event voor een bronbestand

Het Ingestion Start event biedt een lijst van alle bronbestanden van archiefvormer.

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e2421> a ns1:Event ;
                                                                                    # applicatie: niet expliciet opgenomen
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;   # door: RAZU
        ns2:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;   # door: RAZU
        ns3:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-0.xlsx>,  # subject, alle bronbestanden in 1 event
            # etc:
            <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf>.
        ns1:eventType <http://id.loc.gov/vocabulary/preservation/eventType/ins> ;    # type event
        ns1:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;   # succesvol?
        prov:endedAtTime "2025-01-13T10:23:28.758690+00:00"^^xsd:dateTime .          # tijd, hier alleen endedAtTime

### 'vir'-event voor een bronbestand

Het Ingestion Start event biedt een lijst van alle bronbestanden van archiefvormer.
Als een viruscheck een besmetting geeft in de ingest-fase dan wordt de ingest afgebroken.

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e2422> a ns3:Event ;
        ns2:exe <https://data.razu.nl/id/applicatie/09f90b15b53f77637ec94b12857f4e67> ; # applicatie: clamav
        ns2:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-0.xlsx>,     # subject, alle bronbestanden in 1 event
            # etc:
            <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.meta.json> ,
            <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;
        ns2:eventType <http://id.loc.gov/vocabulary/preservation/eventType/vir> ;       # type event
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;      # succesvol?
        ns1:outcomeNote "" ;
        prov:endedAtTime "2025-01-13T10:27:29.011168+00:00"^^xsd:dateTime ;
        prov:startedAtTime "2025-01-13T10:23:28.758690+00:00"^^xsd:dateTime .

### 'fil'-event voor een bronbestand

In de outcomeNote wordt de originele bestandsnaam gegeven, als relatief pad.

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e2315> a ns2:Event ;
                                                                                                # applicatie: niet expliciet opgenomen
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;              # door: RAZU
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;           # subject 
        ns2:eventType <http://id.loc.gov/vocabulary/preservation/eventType/fil> ;               # type event
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;              # succesvol?
        ns2:outcomeNote "renamed 20230405_Bestuursvergadering/Bijlage_0_2_Beleidsplan_Vriendenstichting_2022.pdf to NL-WbDRAZU-K50907905-500-1095.pdf" ; # resultaat
        prov:endedAtTime "2025-01-21T08:33:40.235675+00:00"^^xsd:dateTime .                     # tijdstip, hier alleen endedAtTime

### 'mes'-event voor een bronbestand

Hierbij wordt de checksum bepaald. Wordt vroeg in het proces, in stap 2, vastgelegd.

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e999> a ns2:Event ;
        ns3:exe <https://data.razu.nl/id/applicatie/1d7104dc068ca27a7f85d4eb18414097> ;         # applicatie:DROID
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;              # door: RAZU
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;           # subject
        ns2:eventType <http://id.loc.gov/vocabulary/preservation/eventType/mes> ;               # type event
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;              # succesvol?
        ns2:outcomeNote "md5sum: 473965f0819db1a6724d9d63fa30a433" ;                            # resultaat, prefix "md5sum: "
        prov:endedAtTime "2025-01-13T10:28:59.004406+00:00"^^xsd:dateTime ;                     # tijdstip, hier startedAtTime & endedAtTime
        prov:startedAtTime "2025-01-13T10:28:40.468897+00:00"^^xsd:dateTime .

### 'for'-event voor een bronbestand

De output van DROID bestandsidentificatie, wordt ook in de metadata-bestanden vastgelegd

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e1000> a ns2:Event ;
        ns3:exe <https://data.razu.nl/id/applicatie/1d7104dc068ca27a7f85d4eb18414097> ; # applicatie:DROID
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;      # door: RAZU
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;   # subject
        ns2:eventType <http://id.loc.gov/vocabulary/preservation/eventType/for> ;       # type event
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;      # succesvol?
        ns2:outcomeNote "fmt/276" ;                                                     # resultaat
        prov:endedAtTime "2025-01-13T10:28:59.004406+00:00"^^xsd:dateTime ;             # tijdstip, hier startedAtTime & endedAtTime
        prov:startedAtTime "2025-01-13T10:28:40.468897+00:00"^^xsd:dateTime .

### 'fix'-event voor een bronbestand

Tijdens het ingest-proces wordt regelmatig de checksum van de bestanden gecontroleerd. Het resultaat hiervan wordt alleen aan het einde van de ingest vastgelegd.
Tijdens het ingest-proces is een afwijkende checksum niet acceptabel en dan wordt de ingest afgebroken totdat de oorzaak ontdenkt en verholpen is.

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e5006> a ns2:Event ;
                                                                                        # applicatie niet expliciet opgenomen
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;      # door: RAZU
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;   # subject
        ns2:eventType <http://id.loc.gov/vocabulary/preservation/eventType/fix> ;       # type event
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;      # succesvol?
        ns2:outcomeNote "fmt/276" ;                                                     # resultaat
        prov:endedAtTime "2025-01-21T08:39:50.267943+00:00"^^xsd:dateTime .             # tijdstip, hier alleen endedAtTime

### 'ine'-event

Het Ingestion End event biedt een lijst van alle bron- en metadatabestanden van het Sip.
Een SIP waarin dit event voorkomt in de eventlog mag niet meer bewerkt worden.

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e5561> a ns2:Event ;
                                                                                            # applicatie niet expliciet opgenomen
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;           # door: RAZU
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-0.meta.json>,     # subject, dit zijn alle files in de sip uitgez. eventlog en manifest 
            <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-0.xlsx>,
            # etc
            <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.meta.json> ,
            <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;          # succesvol?
        prov:endedAtTime "2025-01-21T08:40:02.835275+00:00"^^xsd:dateTime .

### 'mem'-event voor een metadata-object, gegenereerd voor een bronbestand 

Dit event wordt gebruik bij zowel de creatie van een metadata-bestand als ook bij het bewerken van een metadata-bestand.

#### Creatie metadata-bestand

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e1664> a ns2:Event ;
                                                                                                    # applicatie niet expliciet opgenomen 
        ns3:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;                  # door RAZU
        ns1:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.pdf> ;               # subject / bron
        ns2:eventType <http://id.loc.gov/vocabulary/preservation/eventType/mem> ;                   # type event
        ns2:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;
        prov:endedAtTime "2025-01-23T12:38:27.980927+00:00"^^xsd:dateTime ;
        prov:generated <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.meta.json> .  # gegenereerd bestand, anders dan bron dus nieuw bestand

#### Bewerking metadata-bestand

    <https://data.razu.nl/id/event/NL-WbDRAZU-K50907905-500-e3670> a ns1:Event ;
                                                                                                    # applicatie niet expliciet opgenomen
        ns2:imp <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;                  # door: RAZU
        ns3:sou <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.meta.json> ;         # subject, het bewerkte bestand
        ns1:eventType <http://id.loc.gov/vocabulary/preservation/eventType/mem> ;                   # type event
        ns1:outcome <http://id.loc.gov/vocabulary/preservation/eventOutcome/suc> ;                  # succesvol?    
        prov:endedAtTime "2025-01-23T12:45:08.373527+00:00"^^xsd:dateTime ;
        prov:generated <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.meta.json> .  # gegenereerd bestand zelfde als bron, dus bewerking






