import unittest
import emu2influx
from api_classes import *
from lxml import objectify


class Emu2InfluxTest(unittest.TestCase):
    def test_price(self):
        block_string = """
    <PriceCluster>
      <DeviceMacId>0xd8d5b9000000f8bc</DeviceMacId>
      <MeterMacId>0x00135003005dba2b</MeterMacId>
      <TimeStamp>0x234e56bd</TimeStamp>
      <Price>0x0000025b</Price>
      <Currency>0x0348</Currency>
      <TrailingDigits>0x04</TrailingDigits>
      <Tier>0x00</Tier>
      <StartTime>0x234da0d0</StartTime>
      <Duration>0x05a0</Duration>
      <RateLabel></RateLabel>
    </PriceCluster>"""
        xml_tree = objectify.fromstring(block_string)
        price_cluster = PriceCluster(xml_tree, block_string)
        self.assertEqual(0.0603, emu2influx.get_price(price_cluster))

    def test_demand(self):
        block_string = """
    <InstantaneousDemand>
      <DeviceMacId>0xd8d5b9000000f8bc</DeviceMacId>
      <MeterMacId>0x00135003005dba2b</MeterMacId>
      <TimeStamp>0x234e5af3</TimeStamp>
      <Demand>0x00014d</Demand>
      <Multiplier>0x00000001</Multiplier>
      <Divisor>0x000003e8</Divisor>
      <DigitsRight>0x03</DigitsRight>
      <DigitsLeft>0x0f</DigitsLeft>
      <SuppressLeadingZero>Y</SuppressLeadingZero>
    </InstantaneousDemand>"""
        xml_tree = objectify.fromstring(block_string)
        instantaneous_demand = InstantaneousDemand(xml_tree, block_string)
        # noinspection PyUnresolvedReferences
        self.assertEqual(0.333, emu2influx.get_reading(instantaneous_demand.Demand, instantaneous_demand))

    def test_timestamp(self):
        block_string = """
    <CurrentSummationDelivered>
      <DeviceMacId>0xd8d5b9000000f8bc</DeviceMacId>
      <MeterMacId>0x00135003005dba2b</MeterMacId>
      <TimeStamp>0x234e5b55</TimeStamp>
      <SummationDelivered>0x0000000002cb3ad2</SummationDelivered>
      <SummationReceived>0x0000000000000000</SummationReceived>
      <Multiplier>0x00000001</Multiplier>
      <Divisor>0x000003e8</Divisor>
      <DigitsRight>0x03</DigitsRight>
      <DigitsLeft>0x0f</DigitsLeft>
      <SuppressLeadingZero>Y</SuppressLeadingZero>
    </CurrentSummationDelivered>"""
        xml_tree = objectify.fromstring(block_string)
        current_summation_delivered = CurrentSummationDelivered(xml_tree, block_string)
        self.assertEqual("2018-10-08T18:15:49", emu2influx.get_timestamp(current_summation_delivered))
