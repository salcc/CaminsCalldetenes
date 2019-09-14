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

from math import sqrt, radians, sin, cos, asin, inf


# Calcula la distància entre dues coordenades terrestres expressades en graus
# utilitzant la fórmula del Haversine.
def distancia(coord1, coord2):
  lat1, lon1 = coord1
  lat2, lon2 = coord2
  lat1, lon1, lat2, lon2 = radians(lat1), radians(lon1), radians(lat2), radians(
    lon2)
  return 2 * 6371008.8 * asin(sqrt(
    sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin(
      (lon2 - lon1) / 2) ** 2))


# Troba el vèrtex més proper a unes coordenades terrestres. Perquè funcioni el
# graf ha de tenir en tots els seus vèrtexs un atribut "coordenades" que indiqui
# les coordenades del vèrtex.
# La funció funciona trobant la distància entre cada vèrtex del graf i les
# coordenades donades i retorna el vèrtex tal que la seva distància és menor que
# la de tots els altres.
def vertex_mes_proper(graf, coordenades):
  distancia_minima = inf
  mes_proper = None
  for v in graf.vertexs():
    d = distancia(coordenades, graf.llegir_atributs(v)["coordenades"])
    if d < distancia_minima:
      distancia_minima = d
      mes_proper = v
  return mes_proper


#
def reconstruir_cami(prev, objectiu):
  cami = []
  while objectiu is not None:
    cami.insert(0, objectiu)
    objectiu = prev[objectiu]
  return cami
