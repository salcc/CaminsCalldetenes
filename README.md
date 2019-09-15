# Camins Calldetenes

Camins Calldetenes permet trobar el camí més curt entre dos punts de
Calldetenes, un municipi de la comarca d'Osona, Catalunya. També és possible
visualitzar els algorismes mentre estan buscant el camí més curt. Disponible a https://caminscalldetenes.cat.

Aquest projecte ha estat desenvolupat per Marçal Comajoan Cara com a part del
treball de recerca de batxillerat.

## Instal·lació

1. Instal·la [Python 3](https://www.python.org/downloads/) i
[Git](https://git-scm.com/download/).

2. Obre el terminal i executa les següents comandes:

##### GNU/Linux o macOS
    git clone https://github.com/salcc/CaminsCalldetenes.git
    cd CaminsCalldetenes
    python3 -m venv venv
    . venv/bin/activate
    python processament/descarregar_osm.py 
    python processament/processar_osm.py 
    pip install Flask
    flask run
    
##### Windows
    git clone https://github.com/salcc/CaminsCalldetenes.git
    cd CaminsCalldetenes
    py -3 -m venv venv
    venv\Scripts\activate
    python processament/descarregar_osm.py 
    python processament/processar_osm.py 
    pip install Flask
    flask run

3. Obre http://127.0.0.1:5000/ en un navegador web.

## Llicència i atribucions

Copyright &copy; 2019 Marçal Comajoan Cara

Aquest projecte està disponible sota la llicència de programari lliure
GNU General Public License, versió 3. Consulteu el fitxer [LICENSE.md](LICENSE.md) per
obtenir més informació.

Les dades mostrades en la capa topogràfica i utilitzades per a què el programa
que he escrit pugui computar el camí més curt han estat proporcionades per
[OpenStreetMap](https://www.openstreetmap.org/) i els seus col·laboradors.
OpenStreetMap és un projecte col·laboratiu per crear un mapa gratuït i
editable de tot el món. Les dades proporcionades estan disponibles sota la
llicència Open Data Commons Open Database License. Més informació a
[openstreetmap.org/copyright](https://www.openstreetmap.org/copyright).

Per mostrar el mapa en aquesta pàgina i poder dibuixar els camins, Camins
Calldetenes utilitza [Leaflet](https://leafletjs.com/), una llibreria de
JavaScript de codi obert per crear mapes interactius.

El projecte també utilitza el micro web framework de codi obert
[Flask](https://palletsprojects.com/p/flask/) que serveix perquè el codi de
la pàgina web es pugui comunicar amb el programa emmagatzemat al servidor web
que computa el camí més ràpid.

Les imatges de la capa ortofoto han estat proporcionades per l'[Institut
Cartogràfic i Geològic de Catalunya](http://www.icgc.cat/ca/).

## Contacte

Marçal Comajoan Cara:
[marcal.comajoan@callisvic.cat](mailto:marcal.comajoan@callisvic.cat)

