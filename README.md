`emu2influx` uses Rainforest Automation's [Emu-Serial-API](https://github.com/rainforestautomation/Emu-Serial-API) to insert EMU-2 ([Amazon.com](https://www.amazon.com/Rainforest-EMU-2-Energy-Monitoring-Unit/dp/B00BGDPRAI)) energy monitoring data into InfluxDB

Your EMU-2 must be provisioned with your utility company and connected to your PC

### Prerequisites

* macOS with [Homebrew](https://brew.sh): `brew install python2 influxdb`
* Debian/Ubuntu: `sudo apt install python-pip libxslt1-dev influxdb`

### Setup

```
$ git clone --recursive https://github.com/abaker/emu2influx.git
$ cd emu2influx
$ pip install -r requirements.txt 
```

### Run

`$ python emu2influx.py <emu2_serial_port>`

By default `emu2influx` will connect to a local InfluxDB install, use the default credentials, and store data in a table named `rainforest`

```
usage: emu2influx.py [-h] [--debug] [--host HOST] [--port PORT]
                     [--username USERNAME] [--password PASSWORD] [--db DB]
                     serial_port

positional arguments:
  serial_port          Rainforest serial port, e.g. 'ttyACM0'

optional arguments:
  -h, --help           show this help message and exit
  --debug              enable debug logging
  --host HOST          influx host
  --port PORT          influx port
  --username USERNAME  influx username
  --password PASSWORD  influx password
  --db DB              influx database name
``` 
