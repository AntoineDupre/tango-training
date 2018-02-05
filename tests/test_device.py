import pytest
from training.device import TrainingDevice
from tango.test_utils import DeviceTestContext


@pytest.yield_fixture
def device_proxy():
    with DeviceTestContext(TrainingDevice) as device:
        yield device


def test_state(device_proxy):
    assert device_proxy.State()
