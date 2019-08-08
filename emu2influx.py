import logging
import sys
import os 
from datetime import datetime

from influxdb import InfluxDBClient

from emu import *

Y2K = 946684800
int_max = 2**31-1
uint_max = 2**32-1


def get_timestamp(obj):
    return datetime.utcfromtimestamp(Y2K + int(obj.TimeStamp, 16)).isoformat()

def get_reading(reading, obj):
    reading = int(reading, 16) * int(obj.Multiplier, 16)
    if reading > int_max:
        reading = -1 * (uint_max - reading)
    return reading / float(int(obj.Divisor, 16))



def get_price(obj):
    return int(obj.Price, 16) / float(10 ** int(obj.TrailingDigits, 16))


def main(client, db):
    client.start_serial()
    client.get_instantaneous_demand('Y')
    client.get_current_summation_delivered()
    client.get_price_blocks()

    last_demand = 0
    last_price = 0
    last_reading = 0

    while True:
        time.sleep(10)

        try:
            price_cluster = client.PriceCluster
            timestamp = get_timestamp(price_cluster)
            if timestamp > last_price:
                measurement = [
                    {
                        "measurement": "price",
                        "time": timestamp,
                        "fields": {
                            "price": get_price(price_cluster)
                        }
                    }
                ]
                logging.debug(price_cluster)
                logging.debug(measurement)
                db.write_points(measurement, time_precision='s')
                last_price = timestamp
        except AttributeError:
            pass

        try:
            instantaneous_demand = client.InstantaneousDemand
            timestamp = get_timestamp(instantaneous_demand)
            if timestamp > last_demand:
                measurement = [
                    {
                        "measurement": "demand",
                        "time": timestamp,
                        "fields": {
                            "demand": get_reading(instantaneous_demand.Demand, instantaneous_demand)
                        }
                    }
                ]
                logging.debug(instantaneous_demand)
                logging.debug(measurement)
                db.write_points(measurement, time_precision='s')
                last_demand = timestamp
        except AttributeError:
            pass

        try:
            current_summation_delivered = client.CurrentSummationDelivered
            timestamp = get_timestamp(current_summation_delivered)
            if timestamp > last_reading:
                measurement = [
                    {
                        "measurement": "reading",
                        "time": timestamp,
                        "fields": {
                            "reading": get_reading(current_summation_delivered.SummationDelivered,
                                                   current_summation_delivered)
                        }
                    }
                ]
                logging.debug(current_summation_delivered)
                logging.debug(measurement)
                db.write_points(measurement, time_precision='s')
                last_reading = timestamp
        except AttributeError:
            pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true', help="enable debug logging", required=False)
    parser.add_argument("--host", help="influx host", required=False, default='localhost')
    parser.add_argument("--port", help="influx port", required=False, default=8086)
    parser.add_argument("--username", help="influx username", required=False, default='root')
    parser.add_argument("--password", help="influx password", required=False, default='root')
    parser.add_argument("--db", help="influx database name", required=False, default='rainforest')
    parser.add_argument("--retries", help="influx retries", required=False, default=3)
    parser.add_argument("serial_port", help="Rainforest serial port, e.g. 'ttyACM0'")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(level=('DEBUG' if args.debug else 'WARN'),
                        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    influx = InfluxDBClient(database=args.db, host=args.host, port=args.port, username=args.username,
                            password=args.password, retries=args.retries)
    influx.create_database(args.db)
    
    try:
        main(client=emu(args.serial_port), db=influx)
    except KeyboardInterrupt:
        try:
                sys.exit(0)
        except SystemExit:
                os._exit(0)
