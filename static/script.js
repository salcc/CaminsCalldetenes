(() => {
  "use strict";

  // Carrega la capa topogràfica, proporcionada per OpenStreetMap
  const osm = new L.TileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    minZoom: 16,
    maxZoom: 20,
    maxNativeZoom: 19,
    attribution: "Dades del mapa d'<a href='https://www.openstreetmap.org/'>OpenStreetMap</a>"
  });

  // Carrega la capa ortofoto, proporcionada per l'Institut Cartogràfic i Geològic de Catalunya
  const icgc = L.tileLayer.wms("https://geoserveis.icgc.cat/icc_mapesbase/wms/service?", {
    layers: "orto25c",
    minZoom: 16,
    maxZoom: 20,
    attribution: "Imatges de l'<a href='https://icgc.cat/'>Institut Cartogràfic i Geològic de Catalunya</a> | " +
      "Dades del mapa d'<a href='https://openstreetmap.org/'>OpenStreetMap</a>"
  });

  // Crea el mapa
  const mapa = L.map("mapa", {
    maxBounds: [[41.9398, 2.2666], [41.9062, 2.3179]],
    maxBoundsViscosity: 0.5,
    layers: [osm],
    center: [41.9246, 2.2846],
    zoom: 17,
    zoomControl: false,
    preferCanvas: true
  });
  mapa.attributionControl.setPrefix("");

  // Canvia el cursor quan s'arrossega el mapa
  mapa.on("dragstart", () => {
    document.getElementById("mapa").style.cursor = "move";
  });
  mapa.on("dragend", () => {
    document.getElementById("mapa").style.cursor = "default";
  });

  // Crea el botó per canviar les capes amb la capa topogràgica i l'ortofoto
  L.control.layers({"Topogràfic": osm, "Ortofoto": icgc}).addTo(mapa);
  const botoCapes = document.getElementsByClassName("leaflet-control-layers-toggle")[0];
  const iconaCapes = document.createElement("i");
  botoCapes.appendChild(iconaCapes);
  iconaCapes.classList.add("material-icons");
  iconaCapes.innerText = "layers";

  let coordenadesInici, coordenadesFinal, timeoutID, retard = 100;

  const cami = L.layerGroup().addTo(mapa), verd = L.layerGroup().addTo(mapa), vermell = L.layerGroup().addTo(mapa);

  const elementNombreVertexsVisitats = document.getElementById("nombre-vertexs-visitats");

  // Funció per aturar l'execució durant uns quants mil·lisegons. Utilitzada per la visualització dels algorismes.
  function esperar(ms) {
    return new Promise((resolve) => timeoutID = setTimeout(resolve, ms));
  }

  // Funció que neteja les línies dibuixades en el mapa
  function netejar() {
    elementNombreVertexsVisitats.textContent = "0";
    if (timeoutID) {
      clearTimeout(timeoutID);
    }

    verd.clearLayers();
    vermell.clearLayers();
    cami.clearLayers();
  }

  // Funció que dibuixa el camí més curt entre els dos marcadors.
  function dibuixarCami() {
    if (coordenadesInici && coordenadesFinal) {
      // El camí el computa la part escrita en Python que es troba emmagatzemada al servidor.
      fetch("/", {
        method: "post",
        headers: {
          "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: "coordenades_origen=(" + coordenadesInici.lat + ", " + coordenadesInici.lng + ")" +
          "&coordenades_destinacio=(" + coordenadesFinal.lat + ", " + coordenadesFinal.lng + ")" +
          "&algorisme=a_star"
      }).then((response) => {
        return response.json();
      }).then((json) => {
        cami.addLayer(L.polyline([coordenadesInici, json[0]], {
          color: "rgb(204, 224, 255)",
          dashArray: "5, 5"
        }).addTo(mapa));
        cami.addLayer(L.polyline(json, {color: "rgb(68, 138, 255)", weight: 5}).addTo(mapa));
        cami.addLayer(L.polyline([json[json.length - 1], coordenadesFinal], {
          color: "rgb(204, 224, 255)",
          dashArray: "5, 5"
        }).addTo(mapa));
      }).catch((error) => {
        console.log("Error: " + error);
      });
    }
  }

  // Funció que dibuixa el camí més curt entre els dos marcadors i també els passos que fa l'algorisme per computar
  // aquest camí.
  function dibuixarCamiVisual(algorisme) {
    if (coordenadesInici && coordenadesFinal) {
      // El camí el computa la part escrita en Python que es troba emmagatzemada al servidor.
      fetch("/", {
        method: "post",
        headers: {
          "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: "coordenades_origen=(" + coordenadesInici.lat + ", " + coordenadesInici.lng + ")" +
          "&coordenades_destinacio=(" + coordenadesFinal.lat + ", " + coordenadesFinal.lng + ")" +
          "&algorisme=" + algorisme + "_visual"
      }).then((response) => {
        return response.json();
      }).then(async (json) => {
        cami.addLayer(L.polyline([coordenadesInici, json[0][0]], {
          color: "rgb(204, 224, 255)",
          dashArray: "5, 5"
        }).addTo(mapa));
        cami.addLayer(L.polyline([json[0][json[0].length - 1], coordenadesFinal], {
          color: "rgb(204, 224, 255)",
          dashArray: "5, 5"
        }).addTo(mapa));
        for (let i = 0, vertexsVisitats = 1; i < json[1].length; i++) {
          while (retard === 500) {
            await esperar(1);
          }
          if (json[1][i][1]) {
            verd.addLayer(L.polyline(json[1][i][0], {color: "rgb(0, 233, 0)"}));
            vertexsVisitats++;
            elementNombreVertexsVisitats.textContent = vertexsVisitats.toLocaleString("ca");
          } else {
            vermell.addLayer(L.polyline(json[1][i][0], {color: "rgb(240, 0, 0)", weight: 5}));
          }
          if (retard) {
            await esperar(retard);
          }
          vermell.clearLayers();
        }
        for (let i = 0; i < json[0].length - 1; i++) {
          cami.addLayer(L.polyline([json[0][i], json[0][i + 1]], {color: "rgb(68, 138, 255)", weight: 5}));
          if (retard) {
            await esperar(retard);
          }
        }
      }).catch((error) => {
        console.log("Error: " + error);
      });
    }
  }

  // Funcionament del "switch" per mostrar els constrols de visualització del panell lateral
  const switchMostrarVisualitzacio = document.getElementById("switch-mostar-visualitzacio"),
    divPanellControlsVisualitzacio = document.getElementById("panell-controls-visualitzacio"),
    divPanellSwitch = document.getElementById("panell-switch");
  switchMostrarVisualitzacio.checked = false;
  switchMostrarVisualitzacio.addEventListener("change", () => {
    if (switchMostrarVisualitzacio.checked) {
      divPanellSwitch.style.flexGrow = "0";
      divPanellControlsVisualitzacio.style.display = "block";
      divPanellControlsVisualitzacio.style.visibility = "visible";
      divPanellControlsVisualitzacio.style.opacity = "1";
      netejar();
      dibuixarCamiVisual(document.querySelector("input[name='algorisme']:checked").value);
    } else {
      divPanellControlsVisualitzacio.style.opacity = "0";
      divPanellControlsVisualitzacio.style.visibility = "hidden";
      netejar();
      dibuixarCami();
      setTimeout(() => {
        divPanellSwitch.style.flexGrow = "1";
        divPanellControlsVisualitzacio.style.display = "none";
      }, 250);
    }
  });

  // Funcionament dels botons dels marcadors
  const iconaMarcador = L.Icon.extend({
    options: {
      shadowUrl: "static/ombra-marcador.png",
      iconSize: [20, 32],
      iconAnchor: [10, 32],
      shadowSize: [41, 41],
      shadowAnchor: [12, 41],
      popupAnchor: [10, 16]
    }
  });
  const botoMarcadorInicial = document.getElementById("marcador-inicial"),
    botoMarcadorFinal = document.getElementById("marcador-final");
  let marcadorInicial, marcadorFinal, colocantMarcador = false;
  botoMarcadorInicial.addEventListener("click", () => {
    if (!colocantMarcador) {
      colocantMarcador = true;
      botoMarcadorInicial.style.cursor = "not-allowed";
      botoMarcadorFinal.style.cursor = "not-allowed";
      if (marcadorInicial) {
        mapa.removeLayer(marcadorInicial);
        netejar();
      }

      mapa.getContainer().style.cursor = "url('static/marcador-inicial.png') 10 32, auto";
      botoMarcadorInicial.style.filter = "grayscale(80%)";

      mapa.once("mousedown", (event) => {
        mapa.getContainer().style.cursor = "";
        botoMarcadorInicial.style.filter = "";

        marcadorInicial = L.marker(event.latlng, {
          icon: new iconaMarcador({iconUrl: "static/marcador-inicial.png"}), interactive: false
        }).addTo(mapa);
        botoMarcadorInicial.style.cursor = "";
        botoMarcadorFinal.style.cursor = "";

        colocantMarcador = false;

        coordenadesInici = event.latlng;

        if (switchMostrarVisualitzacio.checked) {
          dibuixarCamiVisual(document.querySelector("input[name='algorisme']:checked").value);
        } else {
          dibuixarCami();
        }
      });
    }
  });
  botoMarcadorFinal.addEventListener("click", () => {
    if (!colocantMarcador) {
      colocantMarcador = true;
      botoMarcadorInicial.style.cursor = "not-allowed";
      botoMarcadorFinal.style.cursor = "not-allowed";
      if (marcadorFinal) {
        mapa.removeLayer(marcadorFinal);
        netejar();
      }

      mapa.getContainer().style.cursor = "url('static/marcador-final.png') 10 32, auto";
      botoMarcadorFinal.style.filter = "grayscale(80%)";

      mapa.once("mousedown", (event) => {
        mapa.getContainer().style.cursor = "";
        botoMarcadorFinal.style.filter = "";

        marcadorFinal = L.marker(event.latlng, {
          icon: new iconaMarcador({iconUrl: "static/marcador-final.png"}), interactive: false
        }).addTo(mapa);
        botoMarcadorInicial.style.cursor = "";
        botoMarcadorFinal.style.cursor = "";

        colocantMarcador = false;

        coordenadesFinal = event.latlng;

        if (switchMostrarVisualitzacio.checked) {
          dibuixarCamiVisual(document.querySelector("input[name='algorisme']:checked").value);
        } else {
          dibuixarCami();
        }
      });
    }
  });

  // Funcionament dels botons "radio" per seleccionar l'algorisme a visualitzar
  document.getElementById("dijkstra").addEventListener("input", () => {
    netejar();
    dibuixarCamiVisual(document.querySelector("input[name='algorisme']:checked").value);
  });
  document.getElementById("a-star").addEventListener("input", () => {
    netejar();
    dibuixarCamiVisual(document.querySelector("input[name='algorisme']:checked").value);
  });

  // Funcionament del "slider" per controlar la velocitat de la visualització
  const sliderVelocitat = document.getElementById("velocitat");
  sliderVelocitat.value = 450;
  sliderVelocitat.addEventListener("input", () => {
    retard = 500 - sliderVelocitat.value;
  });

  // Funcionament del botó per repetir la visualització
  document.getElementById("repetir").addEventListener("click", () => {
    netejar();
    dibuixarCamiVisual(document.querySelector("input[name='algorisme']:checked").value);
  });

  // Funcionament del botó per netejar la visualització
  document.getElementById("netejar").addEventListener("click", () => {
    netejar();
    if (marcadorInicial) {
      mapa.removeLayer(marcadorInicial);
    }
    if (marcadorFinal) {
      mapa.removeLayer(marcadorFinal);
    }
    coordenadesInici = undefined;
    coordenadesFinal = undefined;
  });

  // Funcionament per mostrar i amagar la finestra d'informació que s'obra quan es clica l'enllaç "Més informació" de
  // la part inferior del panell lateral
  const finestraInfo = document.getElementById("finestra-info");
  document.getElementById("mes-info-a").addEventListener("click", () => {
    finestraInfo.style.display = "block";
  });
  document.getElementById("tancar-info").addEventListener("mousedown", () => {
    finestraInfo.style.display = "none";
  });
  window.addEventListener("mousedown", (event) => {
    if (event.target === finestraInfo) {
      finestraInfo.style.display = "none";
    }
  });

})();
