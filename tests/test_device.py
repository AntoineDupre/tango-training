import pytest
from training.device import TrainingDevice
from tango.test_utils import DeviceTestContext
from tango import DevFailed
from utils import tcp_server
import multiprocessing
from training import device
from mock import MagicMock
import functools


mock_proxy = MagicMock()
try:
    device.tango.DeviceProxy = mock_proxy
except AttributeError:
    try:
        device.DeviceProxy = mock_proxy
    except AttributeError:
        pass


def catch_unimplemented(func):
    @functools.wraps(func)
    def wrapper(device_proxy):
        try:
            return func(device_proxy)
        except DevFailed as e:
            if "not found" in str(e):
                pytest.xfail()
            else:
                raise e
    return wrapper


class TcpContext():
    proc = None

    def __enter__(self):
        if not self.proc:
            self.proc = multiprocessing.Process(target=tcp_server.main)
        self.proc.start()
        return self.proc

    def __exit__(self, exc_type, exception, trace):
        self.proc.terminate()


@pytest.yield_fixture
def server():
    with TcpContext() as tcp:
        yield tcp


@pytest.yield_fixture
def device_proxy(server):
    with DeviceTestContext(TrainingDevice, port=9999) as device:
        yield device


def test_server_running(device_proxy):
    assert device_proxy.State()


@catch_unimplemented
def test_on_state(device_proxy):
    device_proxy.command_inout("TurnOn")
    read_out = device_proxy.read_attribute("State")
    assert read_out
    assert str(read_out.value) == "ON"


@catch_unimplemented
def test_off_state(device_proxy):
    device_proxy.command_inout("TurnOn")
    device_proxy.command_inout("TurnOff")
    read_out = device_proxy.read_attribute("State")
    assert read_out
    assert str(read_out.value) == "OFF"


@catch_unimplemented
def test_wavefrom_attribute(device_proxy):
    device_proxy.command_inout("TurnOn")
    read_out = device_proxy.read_attribute("waveform")
    assert read_out
    assert len(read_out.value) == 200


@catch_unimplemented
def test_maximum_attribute(device_proxy):
    try:
        device_proxy.command_inout("TurnOn")
        device_proxy.read_attribute("waveform")
    except DevFailed:
        pytest.xfail()
    read_out = device_proxy.read_attribute("maximum")
    assert read_out
    assert read_out.value >= 0.5


@catch_unimplemented
def test_offset_attribute(device_proxy):
    try:
        device_proxy.command_inout("TurnOn")
        device_proxy.read_attribute("waveform")
    except DevFailed:
        pytest.xfail()
    try:
        device_proxy.write_attribute("offset", 1)
    except TypeError:
        pytest.xfail()
    read_out = device.read_attribute("offset")
    assert read_out
    assert read_out.value == 1
    read_out = device_proxy.read_attribute("waveform")
    assert max(read_out.value) >= 1.5
