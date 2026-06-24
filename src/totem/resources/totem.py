from typing import Literal

from ocelescope import Resource
from ocelescope.visualization.default.graph import (
    EdgeArrow,
    Graph,
    GraphEdge,
    GraphNode,
    GraphvizLayoutConfig,
)
from ocelescope.visualization.util.color import generate_color_map
from pydantic import BaseModel

Temporal_Relation_Constant = Literal["D", "Di", "I", "Ii", "P"]

Cardinality = Literal["0", "1", "0...1", "1..*", "0...*"]

# Force-directed layout tuned to spread object types further apart.
# `K` raises the ideal edge length and `sep` adds margin around each node so
# the graph reads as spaced out rather than clustered.
TOTEM_GRAPH_LAYOUT = GraphvizLayoutConfig(
    engine="sfdp",
    graphAttrs={
        "overlap": "false",
        "splines": "spline",
        "K": 2.4,
        "repulsiveforce": 3.0,
        "sep": "+60",
    },
)


class TotemEdge(BaseModel):
    source: str
    target: str
    lc: Cardinality | None
    lc_inverse: Cardinality | None
    ec: Cardinality | None
    ec_inverse: Cardinality | None
    tr: Temporal_Relation_Constant | None
    tr_inverse: Temporal_Relation_Constant | None


class Totem(Resource):
    label = "TOTeM"
    description = "A TOTeM"

    object_types: list[str]
    edges: list[TotemEdge]
    type: Literal["totem"] = "totem"

    def visualize(self) -> Graph:
        def tr_to_arrow(tr: Temporal_Relation_Constant | None) -> EdgeArrow:
            mapping: dict[Temporal_Relation_Constant | None, EdgeArrow] = {
                "P": "triangle",
                "D": "tee",
                "I": "circle",
                "Ii": None,
                "Di": None,
                None: None,
            }
            return mapping[tr]

        def edge_label_for_forward(e: TotemEdge) -> str:
            parts = []
            if e.ec:
                parts.append(e.ec)
            if e.ec_inverse:
                parts.append(e.ec_inverse)
            return " · ".join(parts) if parts else ""

        color_map = generate_color_map(self.object_types)
        nodes: list[GraphNode] = []
        for ot in self.object_types:
            nodes.append(
                GraphNode(
                    id=ot,
                    label=ot,
                    shape="rectangle",
                    color=color_map.get(ot),
                    width=max(90.0, len(ot) * 8.0 + 24.0),
                    height=40,
                )
            )

        edges: list[GraphEdge] = []
        for e in self.edges:
            src_arrow = tr_to_arrow(e.tr_inverse)
            tgt_arrow = tr_to_arrow(e.tr)
            label = edge_label_for_forward(e)
            color = color_map.get(e.source)

            edges.append(
                GraphEdge(
                    source=e.source,
                    target=e.target,
                    start_arrow=src_arrow,
                    end_arrow=tgt_arrow,
                    color=color,
                    label=label,
                    end_label=e.lc,
                    start_label=e.lc_inverse,
                )
            )

        return Graph(
            type="graph",
            nodes=nodes,
            edges=edges,
            layout_config=TOTEM_GRAPH_LAYOUT,
        )
