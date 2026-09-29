from typing import Annotated

from ocelescope import (
    OCEL,
    OCEL_FIELD,
    SLIDER_FIELD,
    ObjectTypeFilter,
    OCELAnnotation,
    Plugin,
    PluginInput,
    plugin_method,
)

from .resources.totem import Totem as TotemGraph
from .util import mine_totem


class MineInput(PluginInput):
    tau: Annotated[
        float,
        SLIDER_FIELD(
            min=0,
            max=1,
            default=0.9,
            step=0.01,
            title="Support Threshold (τ)",
            description=(
                "Minimum fraction of observations supporting a cardinality or temporal "
                "relation for it to be included. Higher values filter more noise."
            ),
        ),
    ] = 0.9

    included_objects: Annotated[
        list[str], OCEL_FIELD(field_type="object_type", ocel_id="ocel", theme="r4pm", default_frequency=0.8)
    ]


class Totem(Plugin):
    label = "TOTeM"
    description = (
        "Generate Temporal Object Type Models (TOTeM) to uncover type-level temporal and cardinality relations"
        " in event logs"
    )
    version = "1.7.5"

    @plugin_method(label="Discover TOTeM", description="Discovers a Temporal Object Type Model")
    def mine_totem(self, ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")], input: MineInput) -> TotemGraph:

        return mine_totem(
            ocel.filter([ObjectTypeFilter(object_types=input.included_objects, mode="include")]).ocel, input.tau
        )
