# Camins Calldetenes

Camins Calldetenes permet trobar el camí més curt entre dos punts de
Calldetenes, un municipi de la comarca d'Osona, Catalunya. També és possible
visualitzar els algorismes mentre estan buscant el camí més curt.

Els algorismes implementats són:
- Algorisme de Dijkstra
- Algorisme de cerca A*
- Algorisme de Dijkstra bidireccional
- Algorisme de cerca A* bidireccional

Aquest projecte ha estat desenvolupat per Marçal Comajoan Cara com a part del
treball de recerca de batxillerat.

El treball de recerca elaborat ha estat guardonat en diversos premis:
els [Premis Pepi Balmaña de l'Institut Jaume Callís](https://agora.xtec.cat/iesjaumecallis/general/lliurament-del-premis-pepi-balmana-a-lexcellencia-en-els-treballs-de-recerca/),
els [Premis Ramon Llull](https://www.url.edu/ca/sala-de-premsa/noticies/institucional/2020/es-donen-coneixer-els-guanyadors-de-la-19a-edicio-dels-premis-ramon-llull-treballs-de-recerca-de-batxillerat),
el [Premi Poincaré de la Facultat de Matemàtiques i Estadística de la UPC](https://fme.upc.edu/ca/premi-poincare/edicions-anteriors/Premi-poincare-2020/veredicte-resultats-fotos),
el [Premi de l'Escola de Camins (UPC) i el Col·legi de Camins, Canals i Ports de Barcelona](https://actualitat.camins.upc.edu/ca/node/7695),
els [Premis UB-Santander](https://youtu.be/o4UfOZX11Nw) i el [Premi Plana de Vic Jove](https://patronatestudisosonencs.cat/ca/noticia/Lliurament-Premi-Plana-de-Vic-Jove-2020).

## Instal·lació

1. Instal·la [Python 3](https://www.python.org/downloads/) i
[Git](https://git-scm.com/download/).

2. Obre el terminal i executa les següents comandes:

##### GNU/Linux o macOS
    git clone https://github.com/salcc/CaminsCalldetenes.git
    cd CaminsCalldetenes
    python3 -m venv venv
    . venv/bin/activate
    python generar_graf.py
    pip install Flask
    flask run
    
##### Windows
    git clone https://github.com/salcc/CaminsCalldetenes.git
    cd CaminsCalldetenes
    py -3 -m venv venv
    venv\Scripts\activate
    python generar_graf.py
    pip install Flask
    flask run

3. Obre http://127.0.0.1:5000/ en un navegador web.

## Llicència i atribucions

Copyright &copy; 2019 Marçal Comajoan Cara

Aquest projecte està disponible sota la llicència de programari lliure
GNU General Public License, versió 3. Consulteu el fitxer
[LICENSE.md](LICENSE.md) per obtenir més informació.

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
[mcomajoancara@gmail.com](mailto:mcomajoancara@gmail.com)

