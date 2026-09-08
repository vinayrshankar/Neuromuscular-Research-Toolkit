import numpy as np

from nmrt.core.channelmap import ChannelRule, apply_channel_map
from nmrt.core.model import Recording, Signal
from nmrt.core.provenance import stable_config_hash


def test_channel_map_scale_offset_invert():
    r = Recording(signals={"ai0": Signal("ai0", np.array([1.0, 2.0]), 1000, unit="V")})
    out = apply_channel_map(r, [ChannelRule("ai0", "Force", "force", "N", scale=10, offset=1, invert=True)])
    assert np.allclose(out.signals["Force"].data, [-11, -21])
    assert out.signals["Force"].unit == "N"


def test_config_hash_order_independent():
    assert stable_config_hash({"a": 1, "b": 2}) == stable_config_hash({"b": 2, "a": 1})
