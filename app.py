'''import streamlit as st
import streamlit.components.v1 as components
import folium
import math
from Maps import load_dimacs_map
from branca.element import MacroElement, Template

class LatLngPopup(MacroElement):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            function latLngPop(e) {
                var lat = e.latlng.lat.toFixed(6);
                var lng = e.latlng.lng.toFixed(6);
                L.popup()
                    .setLatLng(e.latlng)
                    .setContent("Lat: " + lat + "<br>Lng: " + lng)
                    .openOn({{this._parent.get_name()}});
            }
            {{this._parent.get_name()}}.on('click', latLngPop);
        {% endmacro %}
    """)

    def __init__(self):
        super().__init__()
        self._name = "LatLngPopup"

st.set_page_config(page_title="Route Finder", layout="wide")
st.title("Route Finder (Node IDs)")

GRAPH_PATH = "graph"
COORDS_PATH = "graph.coords"

@st.cache_resource
def get_graph():
    return load_dimacs_map(
        graph_path=GRAPH_PATH,
        coords_path=COORDS_PATH,
        name="Road Graph",
        add_reverse_edges=True
    )
def haversine(lon1, lat1, lon2, lat2):
    """
    Great-circle distance between two points on Earth (meters).
    Input: lon/lat in degrees.
    """
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def path_distance_meters(m, path):
    total = 0.0
    if not path or len(path) < 2:
        return total

    for u, v in zip(path[:-1], path[1:]):
        loc1 = m.locations[u]
        loc2 = m.locations[v]
        total += haversine(loc1.long, loc1.lat, loc2.long, loc2.lat)

    return total

m = get_graph()

st.caption(
    f"Loaded {len(m.locations):,} nodes and "
    f"{sum(len(v) for v in m.neighbours.values()):,} neighbour links."
)

col1, col2 = st.columns(2)

with col1:
    start = st.text_input("Start node id", value="").strip()

with col2:
    destination = st.text_input("Destination node id", value="").strip()

if "route_html" not in st.session_state:
    st.session_state.route_html = None
if "route_info" not in st.session_state:
    st.session_state.route_info = None

if "route_html" not in st.session_state:
    st.session_state.route_html = None
if "route_info" not in st.session_state:
    # we'll store: (path, graph_cost, geo_distance_m)
    st.session_state.route_info = None

def make_base_map():
    """
    Show a normal map without a route.
    We'll center on Berlin-ish coordinates (from your dataset description).
    """
    fmap = folium.Map(location=[52.52, 13.405], zoom_start=12, tiles="OpenStreetMap")
    fmap.add_child(LatLngPopup())
    return fmap.get_root().render()


# If nothing has been computed yet, show a base map
if st.session_state.route_html is None:
    st.session_state.route_html = make_base_map()    

if st.button("Find route"):
    if start == destination:
        st.warning("Pick two different node ids.")
    elif start not in m.locations:
        st.error(f"Start node '{start}' not found.")
    elif destination not in m.locations:
        st.error(f"Destination node '{destination}' not found.")
    else:
        with st.spinner("Computing route..."):
            path, graph_cost = m.dijkstra(start, destination)

        if not path:
            st.error("No route found (graph may be disconnected).")
            st.session_state.route_html = None
            st.session_state.route_info = None
        else:
            geo_distance_m = path_distance_meters(m, path)
            st.session_state.route_info = (path, geo_distance_m)

            fmap = m.folium_route_map(path, max_points=2000)
            st.session_state.route_html = fmap.get_root().render()

# Show results (only if route exists)
if st.session_state.route_info:
    path, geo_distance_m = st.session_state.route_info

    st.success(f"Route found with {len(path):,} nodes.")
    st.write(f"Geographic distance: **{geo_distance_m/1000:.2f} km**")


# Always show map HTML (route map or base map)
components.html(st.session_state.route_html, height=650, scrolling=False)'''


import math
import streamlit as st
import folium

from streamlit_folium import st_folium
from Maps import load_dimacs_map
from branca.element import MacroElement, Template


class LatLngPopup(MacroElement):
    """Show a small popup with lat/lng when the user clicks the map."""
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            function latLngPop(e) {
                var lat = e.latlng.lat.toFixed(6);
                var lng = e.latlng.lng.toFixed(6);
                L.popup()
                    .setLatLng(e.latlng)
                    .setContent("Lat: " + lat + "<br>Lng: " + lng)
                    .openOn({{this._parent.get_name()}});
            }
            {{this._parent.get_name()}}.on('click', latLngPop);
        {% endmacro %}
    """)

    def __init__(self):
        super().__init__()
        self._name = "LatLngPopup"


st.set_page_config(page_title="Route Finder (Click to Route)", layout="wide")
st.title("Click-to-Route Map")

GRAPH_PATH = "graph"
COORDS_PATH = "graph.coords"


@st.cache_resource
def get_graph():
    return load_dimacs_map(
        graph_path=GRAPH_PATH,
        coords_path=COORDS_PATH,
        name="Road Graph",
        add_reverse_edges=True
    )


def haversine(lon1, lat1, lon2, lat2):
    """Great-circle distance between two points on Earth (meters)."""
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def path_distance_meters(m, path):
    total = 0.0
    if not path or len(path) < 2:
        return total
    for u, v in zip(path[:-1], path[1:]):
        loc1 = m.locations[u]
        loc2 = m.locations[v]
        total += haversine(loc1.long, loc1.lat, loc2.long, loc2.lat)
    return total


m = get_graph()

st.caption(
    f"Loaded {len(m.locations):,} nodes and "
    f"{sum(len(v) for v in m.neighbours.values()):,} neighbour links."
)

# ---------- Session state ----------
defaults = {
    "start_click": None,        # (lat, lon) clicked
    "dest_click": None,         # (lat, lon) clicked
    "start_node": None,         # nearest node id
    "dest_node": None,          # nearest node id
    "route_path": None,         # list of node ids
    "route_geo_m": None,        # meters
    "last_click_sig": None,     # to avoid repeated processing
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_points():
    st.session_state.start_click = None
    st.session_state.dest_click = None
    st.session_state.start_node = None
    st.session_state.dest_node = None
    st.session_state.route_path = None
    st.session_state.route_geo_m = None
    st.session_state.last_click_sig = None


def ensure_points_from_click(lat: float, lon: float):
    """Assign click to start/destination in order; third click resets start."""
    if st.session_state.start_click is None:
        st.session_state.start_click = (lat, lon)
        st.session_state.start_node = m.nearest_node(lat, lon)
        st.session_state.route_path = None
        st.session_state.route_geo_m = None
        return

    if st.session_state.dest_click is None:
        st.session_state.dest_click = (lat, lon)
        st.session_state.dest_node = m.nearest_node(lat, lon)
        st.session_state.route_path = None
        st.session_state.route_geo_m = None
        return

    # If both set, start over with new start point
    st.session_state.start_click = (lat, lon)
    st.session_state.start_node = m.nearest_node(lat, lon)
    st.session_state.dest_click = None
    st.session_state.dest_node = None
    st.session_state.route_path = None
    st.session_state.route_geo_m = None


# ---------- Controls ----------
c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    if st.button("Reset points"):
        reset_points()

with c2:
    compute = st.button("Compute route", disabled=not (st.session_state.start_node and st.session_state.dest_node))

with c3:
    st.write("Click once for **Start**, click again for **Destination**. A third click replaces Start.")

# ---------- Build map to display ----------
def build_select_map():
    # Center on start if set, else Berlin-ish
    if st.session_state.start_click:
        center = [st.session_state.start_click[0], st.session_state.start_click[1]]
        zoom = 14
    else:
        center = [52.52, 13.405]
        zoom = 12

    fmap = folium.Map(location=center, zoom_start=zoom, tiles="OpenStreetMap")
    fmap.add_child(LatLngPopup())

    if st.session_state.start_click:
        lat, lon = st.session_state.start_click
        folium.Marker([lat, lon], tooltip="Start (clicked)", icon=folium.Icon(color="green")).add_to(fmap)

        # show snapped node too (optional)
        sn = st.session_state.start_node
        if sn and sn in m.coords:
            slat, slon = m.coords[sn]
            folium.CircleMarker([slat, slon], radius=6, tooltip=f"Nearest node: {sn}", fill=True).add_to(fmap)

    if st.session_state.dest_click:
        lat, lon = st.session_state.dest_click
        folium.Marker([lat, lon], tooltip="Destination (clicked)", icon=folium.Icon(color="red")).add_to(fmap)

        dn = st.session_state.dest_node
        if dn and dn in m.coords:
            dlat, dlon = m.coords[dn]
            folium.CircleMarker([dlat, dlon], radius=6, tooltip=f"Nearest node: {dn}", fill=True).add_to(fmap)

    return fmap


def build_route_map():
    # Draw the path using your existing helper
    fmap = m.folium_route_map(st.session_state.route_path, max_points=2000)
    fmap.add_child(LatLngPopup())
    return fmap


# ---------- Render map + capture click ----------
if st.session_state.route_path:
    fmap = build_route_map()
else:
    fmap = build_select_map()

map_state = st_folium(fmap, height=650, width=None)

# Process click from st_folium
clicked = map_state.get("last_clicked")
if clicked and isinstance(clicked, dict) and "lat" in clicked and "lng" in clicked:
    lat = float(clicked["lat"])
    lon = float(clicked["lng"])
    sig = (round(lat, 7), round(lon, 7))
    if sig != st.session_state.last_click_sig:
        st.session_state.last_click_sig = sig
        ensure_points_from_click(lat, lon)
        st.rerun()

# ---------- Compute route ----------
if compute:
    s = st.session_state.start_node
    t = st.session_state.dest_node
    if not s or not t:
        st.warning("Please click Start and Destination on the map first.")
    elif s == t:
        st.warning("Start and destination snapped to the same node. Click farther apart.")
    else:
        with st.spinner("Computing route..."):
            path, _graph_cost = m.dijkstra(s, t)

        if not path:
            st.error("No route found (graph may be disconnected).")
        else:
            st.session_state.route_path = path
            st.session_state.route_geo_m = path_distance_meters(m, path)
            st.rerun()

# ---------- Info panel ----------
info = st.container()
with info:
    colA, colB = st.columns(2)

    with colA:
        st.subheader("Selected points")
        if st.session_state.start_click:
            st.write(f"Start click: `{st.session_state.start_click[0]:.6f}, {st.session_state.start_click[1]:.6f}`")
            st.write(f"Nearest node: `{st.session_state.start_node}`")
        else:
            st.write("Start: not set")

        if st.session_state.dest_click:
            st.write(f"Destination click: `{st.session_state.dest_click[0]:.6f}, {st.session_state.dest_click[1]:.6f}`")
            st.write(f"Nearest node: `{st.session_state.dest_node}`")
        else:
            st.write("Destination: not set")

    with colB:
        st.subheader("Route")
        if st.session_state.route_path:
            st.success(f"Route found with {len(st.session_state.route_path):,} nodes.")
            st.write(f"Geographic distance: **{st.session_state.route_geo_m/1000:.2f} km**")
            if st.button("Clear route (keep points)"):
                st.session_state.route_path = None
                st.session_state.route_geo_m = None
                st.rerun()
        else:
            st.write("No route computed yet.")


