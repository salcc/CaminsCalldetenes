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

import urllib.request

url = "https://www.openstreetmap.org/api/0.6/map?bbox=2.2347%2C41.8981%2C2.3554%2C41.952"
with urllib.request.urlopen(url) as response, open("processament/mapa.osm", 'wb') as mapa_osm:
    mapa_osm.write(response.read())

