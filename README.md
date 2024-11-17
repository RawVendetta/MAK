# MAK
More Advanced Keylogging for Python. This repository contains a framework to stream keystrokes between a server and a client.

## Description of files:
- __listener.py__
> listener.py contains the server for recieving data from a client. It recieves keystrokes and saves them in __*received_data.log*__, and recieves screenshot data in __*/CapturedImages/*__ as __*screenshotY/M/D/h/m/s.txt*__
- __daemon.py__
> daemon.py is the payload that sends the data to the specified server. All keystrokes and screenshots are never saved on the target system, and are instead all transfered directly through the socket via byte format.
- __mak.pyw__
> mak.pyw is an example to run the client and server on a local system for testing. It is also an example of how to spawn the daemon as a background process so no terminal will need to remain open after its execution.
- __read_data.py__
> read_data.py is a simple implementation to read the logged keystroke events stored in __*received_data.log*__
- __inspectimage.py__
> inspectimage.py is an example implementation of converting the __*screenshotY/M/D/h/m/s.txt*__ files in __*/CapturedImages/*__ into .png files and store them in __*/CapturedImages/Converted/*__
---
## Using this repository
### Start logging with MAK:
`python mak.pyw` or `python3 mak.pyw` or Double Click __"mak.pyw"__

Run mak.pyw and it will open a socket on the host and port specified by s_host and s_port in the code of listener.py and daemon.py 

*(Default: s_host:s_port // 'localhost':9999)*. 
> After execution all keystroke events are logged and sent to the listener, which is currently configured to save the log data in the same folder as the python programs. Additionally, screenshots are taken on a set interval specified by ss_interval in daemon.py and sent to the listener.

To use this code externally, you need to modify s_host and s_port to your specification. listener.py will be ran on the server and daemon.py will need to be ran on the remote client. The method used in mak.pyw can be used to spawn the daemon as a background process.
> By changing this configuration, all exfiltrated data is sent to the remote server rather than stored on the client. If there are issues receiving data, there is likely a firewall conflict between the server and client.

### Interacting with captured data:
To itneract with the captured keylogging and screenshot data, the two programs *read_data.py* and *inspectimage.py* are provided.
- using __read_data.py__
> by executing read_data.py, it will automatically search for received_data.log and parse the data into a readable format and print the output to the screen.
- using __inspectimage.py__
> Once inspectimage.py is executed, the user will be provided a menu. The user can either specify a single screenshot to convert to png, or convert all availible screenshot data files into png.


*Note: While the listener can currently accept multiple connections at once, the code is not formatted to separate the clients data. This results in convolution of your log and screenshot data if more than one client is being logged at once.*
