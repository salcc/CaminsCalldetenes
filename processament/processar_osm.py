# Copyright (C) 2019 Marçal Comajoan Cara
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pickle
import xml.etree.ElementTree as xml
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import distancia
from graf import GrafDirigit


element_tree = xml.parse("processament/mapa.osm").getroot()
dicc_vertexs = {}
vies = []

for i in element_tree:
  if i.tag == "node":
    dicc_vertexs[int(i.attrib["id"])] = [
      float(i.attrib["lat"]), float(i.attrib["lon"])]
  elif i.tag == "way":
    via = []
    unidireccional = False
    insertar = False
    for j in i:
      if j.tag == "nd":
        via.append(int(j.attrib["ref"]))
      elif j.tag == "tag":
        if (j.attrib["k"] == "oneway" and j.attrib["v"] == "yes") or (
            j.attrib["k"] == "junction" and (
            j.attrib["v"] in ["roundabout", "circular"])):
          unidireccional = True
        elif j.attrib["k"] == "highway" and j.attrib["v"] in ["motorway",
                                                              "motorway_link",
                                                              "trunk",
                                                              "trunk_link",
                                                              "primary",
                                                              "primary_link",
                                                              "secondary",
                                                              "secondary_link",
                                                              "tertiary",
                                                              "tertiary_link",
                                                              "unclassified",
                                                              "residential",
                                                              "service",
                                                              "living_street",
                                                              "track"]:
          insertar = True

    if insertar:
      vies.append(via)
      if not unidireccional:
        vies.append(list(reversed(via)))

graf = GrafDirigit()

for id, coordenades in dicc_vertexs.items():
  for via in vies:
    if id in via:
      dicc_vertexs[id] = graf.ordre()
      graf.afegir_vertex(id=id, coordenades=coordenades)
      break

for via in vies:
  for i, id in enumerate(via):
    via[i] = dicc_vertexs[id]
  for i in range(len(via) - 1):
    graf.afegir_aresta((via[i], via[i + 1]))

for e in graf.arestes():
  graf.assignar_atributs(e, llargada=distancia(
    graf.llegir_atributs(e[0])["coordenades"],
    graf.llegir_atributs(e[1])["coordenades"]))

f = open("graf.pickle", "wb")
pickle.dump(graf, f)
f.close()
