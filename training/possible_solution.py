from tango.server import Device, attribute, command, device_property
from tango import DevState
from telnetlib import Telnet
from threading import RLock


class TrainingDevice(Device):
    telnet = None

    host = device_property(dtype=str, default_value="localhost")
    port = device_property(dtype=int, default_value=8888)

    waveform = attribute(dtype=(float,), max_dim_x=200)
    is_running = attribute(dtype=bool)

    def init_device(self):
        Device.init_device(self)
        self.lock = RLock()
        if not self.telnet:
            try:
                self.telnet = Telnet()
                self.telnet.open(self.host, self.port)
            except ConnectionRefusedError:
                self.set_state(DevState.FAULT)
                self.telnet = None
            else:
                self.read_is_running()

    def delete_device(self):
        self.telnet.close()
        self.telnet = None
        Device.delete_device(self)

    def ask(self, cmd):
        with self.lock:
            cmd = cmd + b"\n"
            self.telnet.write(cmd)
            return self.telnet.read_until(b"\n").decode()

    def compute_state(self, reply):
        if "ON" in reply:
            self.set_state(DevState.ON)
        else:
            self.set_state(DevState.OFF)

    def read_is_running(self):
        state = self.ask(b'STATE')
        self.compute_state(state)
        return "ON" in state

    @command()
    def TurnOn(self):
        state = self.ask(b"ON")
        self.compute_state(state)

    @command()
    def TurnOff(self):
        state = self.ask(b"OFF")
        self.compute_state(state)

    def read_waveform(self):
        data = self.ask(b"DATA")
        data = data.split(":")[1][:-1]
        data = list(map(float, data.split(",")))
        return data

    def is_waveform_allowed(self, request):
        return self.get_state() == DevState.ON

if __name__ == "__main__":
    TrainingDevice.run_server()
