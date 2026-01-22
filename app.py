
import streamlit as st
import streamlit.components.v1 as components
import folium

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


def make_base_map():
    """
    Show a normal map without a route.
    We'll center on Berlin-ish coordinates (from your dataset description).
    """
    fmap = folium.Map(location=[52.52, 13.405], zoom_start=12, tiles="OpenStreetMap")
    return fmap.get_root().render()


# If nothing has been computed yet, show a base map
if st.session_state.route_html is None:
    st.session_state.route_html = make_base_map()


# Only compute a route when button is clicked AND both inputs exist
if st.button("Find route"):
    # If user left inputs blank: just show base map and reset route info
    if start == "" or destination == "":
        st.session_state.route_info = None
        st.session_state.route_html = make_base_map()
    else:
        if start == destination:
            st.warning("Pick two different node ids.")
        elif start not in m.locations:
            st.error(f"Start node '{start}' not found.")
        elif destination not in m.locations:
            st.error(f"Destination node '{destination}' not found.")
        else:
            with st.spinner("Computing route..."):
                path, total = m.dijkstra(start, destination)

            if not path:
                st.error("No route found (graph may be disconnected).")
                st.session_state.route_info = None
                st.session_state.route_html = make_base_map()
            else:
                st.session_state.route_info = (path, total)
                fmap = m.folium_route_map(path, max_points=2000)
                st.session_state.route_html = fmap.get_root().render()

# Show results (only if route exists)
if st.session_state.route_info:
    path, total = st.session_state.route_info
    st.success(f"Route found with {len(path):,} nodes.")
    st.write(f"Total distance/weight: **{total}**")

# Always show map HTML (route map or base map)
components.html(st.session_state.route_html, height=650, scrolling=False)
