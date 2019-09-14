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
from queue import Queue, PriorityQueue

from utils import distancia, reconstruir_cami


def cerca_en_amplada(graf, origen, objectiu):
  cost = [inf] * graf.ordre()
  prev = [None] * graf.ordre()

  cost[origen] = 0

  q = Queue()
  q.put(origen)

  while not q.empty():
    u = q.get()

    if u == objectiu:
      return reconstruir_cami(prev, objectiu)

    if u not in prev:
      for v in graf.llista_adjacencia[u]:
        if cost[v] == inf:
          prev[v] = u
          cost[v] = cost[u] + 1
          q.put(v)

  return None


def dijkstra(graf, origen, objectiu, nom_atribut_pes):
  cost = [inf] * graf.ordre()
  prev = [None] * graf.ordre()

  cost[origen] = 0

  pq = PriorityQueue()
  pq.put((cost[origen], origen))

  while not pq.empty():
    d, u = pq.get()

    if u == objectiu:
      return reconstruir_cami(prev, objectiu)

    if u not in prev:
      for v in graf.llista_adjacencia[u]:
        c = d + graf.llegir_atributs((u, v))[nom_atribut_pes]

        if c < cost[v]:
          prev[v] = u
          cost[v] = c
          pq.put((cost[v], v))

  return None


def heuristica(graf, a, b):
  return distancia(graf.llegir_atributs(a)["coordenades"], graf.llegir_atributs(b)["coordenades"])


def a_star(graf, origen, objectiu, nom_atribut_pes):
  cost = [inf] * graf.ordre()
  prev = [None] * graf.ordre()

  cost[origen] = 0

  pq = PriorityQueue()
  pq.put((cost[origen], origen))

  while not pq.empty():
    d, u = pq.get()

    if u == objectiu:
      return reconstruir_cami(prev, objectiu)

    if u not in prev:
      for v in graf.llista_adjacencia[u]:
        c = d + graf.llegir_atributs((u, v))[nom_atribut_pes] + heuristica(graf, v, objectiu) - heuristica(graf, u, objectiu)

        if c < cost[v]:
          prev[v] = u
          cost[v] = c
          pq.put((cost[v], v))

  return None

