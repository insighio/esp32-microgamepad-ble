from machine import Pin, ADC
from time import sleep

# This example demonstrates a peripheral implementing the Nordic UART Service (NUS).

import ubluetooth
from ble_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_UART_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    ubluetooth.FLAG_NOTIFY,
)
_UART_RX = (
    ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    ubluetooth.FLAG_WRITE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)


class BLEUART:
    def __init__(self, ble, name="mpy-uart", rxbuf=100):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        # Increase the size of the rx buffer and enable append mode.
        self._ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        # Optionally add services=[_UART_UUID], but this is likely to make the payload too large.
        self._payload = advertising_payload(name=name, appearance=_ADV_APPEARANCE_GENERIC_COMPUTER)
        self._advertise()

    def irq(self, handler):
        self._handler = handler

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if conn_handle in self._connections and value_handle == self._rx_handle:
                self._rx_buffer += self._ble.gatts_read(self._rx_handle)
                if self._handler:
                    self._handler()

    def any(self):
        return len(self._rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def write(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def close(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

Ry = ADC(Pin(34))
Ry.atten(ADC.ATTN_11DB)       #Full range: 3.3v
Rx = ADC(Pin(35))
Rx.atten(ADC.ATTN_11DB)       #Full range: 3.3v
button1 = Pin(25, Pin.IN)
Ly = ADC(Pin(32))
Ly.atten(ADC.ATTN_11DB)       #Full range: 3.3v
Lx = ADC(Pin(33))
Lx.atten(ADC.ATTN_11DB)       #Full range: 3.3v
button2 = Pin(26, Pin.IN)

ble = ubluetooth.BLE()
uart = BLEUART(ble)

def on_rx():
    print("rx: ", uart.read().decode().strip())

def readVal(pin, measurement_cycles=10):
    tmp = 0.0
    for _ in range(0, measurement_cycles):
        tmp += pin.read()
    # typical voltage_divider levels: 3.054 --> Exp Board 2.0, 2 --> Exp Board 3, 11 --> in-house implementation

    #should we use round function since the following division returns millivolt?
    return round((tmp/measurement_cycles))

uart.irq(handler=on_rx)
nums = [4, 8, 15, 16, 23, 42]
i = 0

while True:
    vrx_pos_l = Rx.read()
    vry_pos_l = Ry.read()
    swt_val_l = button1.value()
    vrx_pos_r = Lx.read()
    vry_pos_r = Ly.read()
    swt_val_r = button2.value()
    str = ("{}|{}|{}-{}|{}|{}\n".format(vrx_pos_l, vry_pos_l, swt_val_l, vrx_pos_r, vry_pos_r, swt_val_r))
    print(str)
    uart.write(str)
    sleep(0.1)

uart.close()
