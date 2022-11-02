# Simple CircuitPython program for Raspberry Pi Pico,
# that reads the processor temperature then transmit it in the shortwave in morse code



# import packages
import board
import microcontroller
import time
import rp2pio
import adafruit_pioasm

# PIO assembler, square signal at the output
generator = adafruit_pioasm.assemble(
    """
    set pins, 0
    set pins, 1
"""
)

freq = 29000000 # The frequency of the transmitter in Hz. In reality, it can be 10khz different!

DI = 0.1  # The length of "DI"

DAH = DI * 3
BETWEENDIDAH = DI
BETWEENCHARS = DI * 3
BETWEENWORDS = DI * 7

morsecodes = [
    [DAH, DAH, DAH, DAH, DAH],  # code of 0
    [DI, DAH, DAH, DAH],  # 1 code of 1
    [DI, DI, DAH, DAH, DAH],  # code of 2
    [DI, DI, DI, DAH, DAH],  # code of 3
    [DI, DI, DI, DI, DAH],  # code of 4
    [DI, DI, DI, DI, DI],  # code of 5
    [DAH, DI, DI, DI, DI],  # code of 6
    [DAH, DAH, DI, DI, DI],  # code of 7
    [DAH, DAH, DAH, DI, DI],  # code of 8
    [DAH, DAH, DAH, DAH, DI],  # code of 9
]


def get_temperature():
    t1 = microcontroller.cpus[0].temperature  # Temperature of the first core
    t2 = microcontroller.cpus[1].temperature  # Temperature of the second core
    print('processor core-1:',t1,'C')
    print('processor core-2:',t2,'C')
    temperature = int(min(t1, t2))  # The colder processor core return more real data
    return temperature  # return temperature


def num_breakdown(number):  # for example, it breaks 32 celsius to 3, 2
    return [int(d) for d in str(number)]  # return the number in array


while True:
    temperature = get_temperature()
    print(f"The temperature is: {temperature}C")
    temp_numbers = num_breakdown(temperature)
    for d in temp_numbers:
        m = morsecodes[d]
        print(f"{d}: {m}")
        for DI_or_DAH in m:
            sm = rp2pio.StateMachine(
                generator, frequency=freq * 2, first_set_pin=board.GP16
            )
            time.sleep(DI_or_DAH)
            sm.deinit()
            time.sleep(BETWEENDIDAH)
        time.sleep(BETWEENCHARS)
    time.sleep(1)
