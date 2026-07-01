from typing import Annotated

from ocelescope import OCEL, OCELAnnotation, Plugin, PluginInput, plugin_method
from pydantic import Field

from .resources.totem import Totem as TotemGraph
from .util import mine_totem


class MineInput(PluginInput):
    tau: Annotated[
        float,
        Field(
            gt=0,
            le=1,
            default=0.9,
            title="Support Threshold (τ)",
            description=(
                "Minimum fraction of observations supporting a cardinality or temporal "
                "relation for it to be included. Higher values filter more noise."
            ),
        ),
    ] = 0.9


class Totem(Plugin):
    label = "TOTeM"
    description = (
        "Generate Temporal Object Type Models (TOTeM) to uncover type-level temporal and cardinality relations"
        " in event logs"
    )
    version = "1.7.3"

    @plugin_method(label="Discover TOTeM", description="Discovers a Temporal Object Type Model")
    def mine_totem(self, ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")], input: MineInput) -> TotemGraph:
        return mine_totem(ocel.ocel, input.tau)
