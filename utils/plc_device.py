from tango.server import Device, attribute
from tango import AttrWriteType, DevState


class PlcDevice(Device):
    FB_R1_105S_DIA_RTO_AD__InAlarm = attribute(
        dtype=bool,
        fget="read",
        fset="write",
        access=AttrWriteType.READ_WRITE)

    def init_device(self):
        Device.init_device(self)
        self._error = False
        self.set_change_event("FB_R1_105S_DIA_RTO_AD__InAlarm", True, False)
        self.set_state(DevState.RUNNING)

    def read(self):
        return self._error

    def write(self, value):
        self.push_change_event("FB_R1_105S_DIA_RTO_AD__InAlarm", value)
        self._error = value


if __name__ == "__main__":
    import sys
    from tango import Database, DbDevInfo
    db = Database()
    device_name = "test/fakeplc/1"
    if device_name not in db.get_device_name("PlcDevice/*", "PlcDevice"):
        raise
        new_device = DbDevInfo()
        new_device.name = device_name
        new_device._class = "PlcDevice"
        new_device.server = "PlcDevice/{}".format(sys.argv[1])
        db.add_device(new_device)
    PlcDevice.run_server()
