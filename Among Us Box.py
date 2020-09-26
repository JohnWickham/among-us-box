/*
 *  Requires CircuitPython
 */

switch_count = 5
led_pins = [7, 6, 5, 4, 3]
led_states = [False, False, False, False, False]
switch_pins = [12, 22, 10, 9, 8]

/* Set up pin modes */

for i in led_pins:
  