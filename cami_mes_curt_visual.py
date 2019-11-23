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


# L'explicació detallada dels algorismes que hi ha a continuació es troben
# dins del text del treball de recerca.

from math import inf
from queue import PriorityQueue

from utils import distancia
from cami_mes_curt import reconstruir_cami


def dijkstra_visual(G, i, f, nom_atribut_pes):
  distancies = [inf] * G.ordre()
  distancies[i] = 0

  predecessors = [None] * G.ordre()

  PQ = PriorityQueue()
  PQ.put((distancies[i], i))

  visualitzacio = []

  while not PQ.empty():
    u = PQ.get()[1]

    if predecessors[u] is not None:
      visualitzacio.append([[G.llegir_atributs(predecessors[u])["coords"], G.llegir_atributs(u)["coords"]], True])

    if u == f:
      return reconstruir_cami(predecessors, f), visualitzacio

    for v in G.llista_adjacencia[u]:
      g = distancies[u] + G.llegir_atributs((u, v))[nom_atribut_pes]

      if g < distancies[v]:
        predecessors[v] = u
        distancies[v] = g
        PQ.put((distancies[v], v))

        visualitzacio.append([[G.llegir_atributs(u)["coords"], G.llegir_atributs(v)["coords"]], False])

  return None, visualitzacio


def heuristica(G, v, f):
  return distancia(G.llegir_atributs(v)["coords"], G.llegir_atributs(f)["coords"])


def a_star_visual(G, i, f, nom_atribut_pes):
  distancies = [inf] * G.ordre()
  distancies[i] = 0

  predecessors = [None] * G.ordre()

  PQ = PriorityQueue()
  PQ.put((distancies[i], i))

  visualitzacio = []

  while not PQ.empty():
    u = PQ.get()[1]

    if predecessors[u] is not None:
      visualitzacio.append([[G.llegir_atributs(predecessors[u])["coords"], G.llegir_atributs(u)["coords"]], True])

    if u == f:
      return reconstruir_cami(predecessors, f), visualitzacio

    for v in G.llista_adjacencia[u]:
      g = distancies[u] + G.llegir_atributs((u, v))[nom_atribut_pes]

      if g < distancies[v]:
        predecessors[v] = u
        distancies[v] = g
        PQ.put((distancies[v] + heuristica(G, v, f), v))

        visualitzacio.append([[G.llegir_atributs(u)["coords"], G.llegir_atributs(v)["coords"]], False])

  return None, visualitzacio
