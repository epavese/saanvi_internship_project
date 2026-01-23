import streamlit as st
import streamlit.components.v1 as components
import folium
import math

from Maps import load_dimacs_map

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
components.html(st.session_state.route_html, height=650, scrolling=False)

'''import math
import streamlit as st
import streamlit.components.v1 as components
from Maps import load_dimacs_map

from branca.element import MacroElement, Template


class LatLngPopup(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                data = e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4);
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent( "<br /><a href="+data+"> click </a>")
                        .openOn({{this._parent.get_name()}})
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);

            {% endmacro %}
            """)  # noqa

    def __init__(self):
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'


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
    start = st.text_input("Start node id", value="1").strip()
with col2:
    destination = st.text_input("Destination node id", value="2").strip()

if "route_html" not in st.session_state:
    st.session_state.route_html = None
if "route_info" not in st.session_state:
    st.session_state.route_info = None

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
            st.session_state.route_info = (path, graph_cost, geo_distance_m)

            fmap = m.folium_route_map(path, max_points=2000)
            fmap.add_child(LatLngPopup())  # <-- enable click lat/lng popup
            st.session_state.route_html = fmap.get_root().render()

# Show results
if st.session_state.route_info:
    path, graph_cost, geo_distance_m = st.session_state.route_info

    st.success(f"Route found with {len(path):,} nodes.")
    st.write(f"Geographic distance: **{geo_distance_m/1000:.2f} km**")
    st.caption(f"Graph cost/weight (from edge weights): {graph_cost}")

if st.session_state.route_html:
    components.html(st.session_state.route_html, height=650, scrolling=False)
else:
    st.info("Enter start and destination node ids, then click Find route.")'''
