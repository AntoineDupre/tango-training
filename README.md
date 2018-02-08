About this repository
===


This repository is an example of a tango device server.

This tango device server is suppose to control a virtual scope throught tcp/ip.

The project contains:

 - An utils folder with:
     - tcp server (```utils/tcp_server.py```) which serves a dummy scope.
     - A dummy plc tango device that pushes event.
 - A tests folder that contains a test protocol. It can be used to validate the required features.
 - A training python package which contains an empty tango device file and a basic example of a possible implementation (Please look at it only after the training session)


---

The TCP server:
===

Protocol
---
 - Request should and with ```b'\n'```
 - Get scope state: 
     - request: ```b'STATE\n'```
     - reply: ```b'State:ON\n'``` or ```b'State:OFF\n'```
 - Turn acquisition on: 
     - request: ```b'ON\n'```
     - reply: ```b'State:ON\n'```
 - Turn acquisition off: 
     - request: ```b'OFF\n'```
     - reply: ```b'State:OFF\n'```
 - Get Waveform:
     - request: ```b'DATA\n'```
     - reply example: ```b'Data:2.938672855118084e-10, 1.9815536275824104e-10, ...., 3.88063288479267e-10\n''```

Basic shell client
---
This protocol can be test from the linux shell with a basic tcp client: 
```bash
$ nc host port
ON
State:ON
```
Basic python script
---
```python

from telnetlib import Telnet

telnet = Telnet()
telnet.open(host, port)
telnet.write(b"ON\n")
print(telnet.read_until(b"\n"))
telnet.close()
```

---


GOALS:
===

1 - Run the tango device
---
Validation:

 - tests/test_device.py::test_server_running: PASSED

2 - Connection with tango properties
---
Requires:

 - tango property: host
 - tango property: port

Validation:

 - tests/test_device.py::test_server_running: PASSED


3 - Start/Stop acquisition
---
Requires:

 - Tango command "TurnOn" (start the acquisition)
 - Tango command "TurnOff" (stop the acquisition)
 - Tango State handling:
     - FAULT if the connection failed
     - ON if the scope is acquiring
     - OFF if the scope is not acquiring

Validation:

 - tests/test_device.py::test_on_state
 - tests/test_device.py::test_off_state

4 - Expose waveform as tango attribute
---
Requires:

 - A Tango spectrum float attribute named "waveform".
 - It should be not allowed to read this attribute if the scope is not acquiring.

Validation:

 - tests/test_device.py::test_wavefrom_attribute

5 - Expose the maximum value as tango attribute
---
Requires:

 - A Tango scalar float attribute named "maximum"

Validation:

 - tests/test_device.py::test_maximum_attribute

6 - Add an offset to the waveform
---
Requires:

 - Tango writable scalar float attribute named "offset"
 - Add the offset setpoint to the waveform tango attribute

Validation:

 - tests/test_device.py::test_offset_attribute

7 - Control the communication rate
---
Requires:

 - Tango expert polled command named "Update"
 - The Update command should manage the tcp request.

Subscribe to a PLC alarm tag:
---
Requires:

 - Add a alarm tag attribute:  test/fakeplc/1/fb_r1_105s_dia_rto_ad__inalarm
 - Switch the tango State to ```Alarm``` if the tag is raised

---

Test
====
Run with setup.py:
```bash
$ python3 setup.py test
```

Test state:

 - xfail: The feature is not implemented.
 - ERROR: The test has failed.
 - PASSED: The test succeed.



Add extra test argument:
```bash
$ python3 setup.py --addopts "-k test_server_running" 
```
(The previous command line runs only the test named ```test_server_running```)


Build
====


Build rpm package from jenkins
----
[Jenkins job](http://w-v-ci-0.maxiv.lu.se/job/dev-maxiv-tangotraining-testing)


Build using setup.py
----
python setup build




Installation
=======

Install from maxiv rpm repository
--------
```bash
$ sudo yum makecache --enablerepo=maxiv-testing
$ sudo yum install tangods-training --enablerepo=maxiv-testing
```


Install from sources in the user space:
----
```bash
$ python setup.py install --user
```
