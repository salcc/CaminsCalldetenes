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

from math import inf
from queue import PriorityQueue

from utils import distancia
from cami_mes_curt import reconstruir_cami


def dijkstra_visual(graf, origen, objectiu, nom_atribut_pes):
  cost = [inf] * graf.ordre()
  prev = [None] * graf.ordre()

  cost[origen] = 0

  pq = PriorityQueue()
  pq.put((cost[origen], origen))

  visualitzacio = []

  while not pq.empty():
    d, u = pq.get()

    if prev[u] is not None:
      visualitzacio.append([[graf.llegir_atributs(prev[u])["coordenades"], graf.llegir_atributs(u)["coordenades"]], True])

    if u == objectiu:
      return reconstruir_cami(prev, objectiu), visualitzacio

    if u not in prev:
      for v in graf.llista_adjacencia[u]:
        c = d + graf.llegir_atributs((u, v))[nom_atribut_pes]

        if c < cost[v]:
          prev[v] = u
          cost[v] = c
          pq.put((cost[v], v))

          visualitzacio.append([[graf.llegir_atributs(u)["coordenades"], graf.llegir_atributs(v)["coordenades"]], False])

  return None, visualitzacio


def heuristica(graf, a, b):
  return distancia(graf.llegir_atributs(a)["coordenades"], graf.llegir_atributs(b)["coordenades"])


def a_star_visual(graf, origen, objectiu, nom_atribut_pes):
  cost = [inf] * graf.ordre()
  prev = [None] * graf.ordre()

  cost[origen] = 0

  pq = PriorityQueue()
  pq.put((cost[origen], origen))

  visualitzacio = []

  while not pq.empty():
    d, u = pq.get()

    if prev[u] is not None:
      visualitzacio.append([[graf.llegir_atributs(prev[u])["coordenades"], graf.llegir_atributs(u)["coordenades"]], True])

    if u == objectiu:
      return reconstruir_cami(prev, objectiu), visualitzacio

    if u not in prev:
      for v in graf.llista_adjacencia[u]:
        c = d + graf.llegir_atributs((u, v))[nom_atribut_pes] + heuristica(graf, v, objectiu) - heuristica(graf, u, objectiu)

        if c < cost[v]:
          prev[v] = u
          cost[v] = c
          pq.put((cost[v], v))

          visualitzacio.append([[graf.llegir_atributs(u)["coordenades"], graf.llegir_atributs(v)["coordenades"]], False])

  return None, visualitzacio
