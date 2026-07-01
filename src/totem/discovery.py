from typing import Annotated

from ocelescope import OCEL
from ocelescope.discovery.decorator import discovery_method
from pydantic import Field

from .resources.totem import Totem
from .util import mine_totem


@discovery_method(
    name="TOTeM Miner",
    description="Discover a Temporal Object Type Model (TOTeM) with type-level temporal and cardinality relations",
)
def discover_totem(
    ocel: OCEL,
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
    ] = 0.9,
) -> Totem:
    return mine_totem(ocel.ocel, tau)
