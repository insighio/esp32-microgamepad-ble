from machine import Pin, ADC

Ry = ADC(Pin(35))
Ry.atten(ADC.ATTN_11DB)
Rx = ADC(Pin(34))
Rx.atten(ADC.ATTN_11DB)
button1 = Pin(25, Pin.IN)
Ly = ADC(Pin(33))
Ly.atten(ADC.ATTN_11DB)
Lx = ADC(Pin(32))
Lx.atten(ADC.ATTN_11DB)
button2 = Pin(26, Pin.IN)


def read_values():
    vrx_pos_l = 4095 - Rx.read()
    vry_pos_l = Ry.read()
    swt_val_l = 1 - button1.value()
    vrx_pos_r = Lx.read()
    vry_pos_r = 4095 - Ly.read()
    swt_val_r = 1 - button2.value()
    return ("{}|{}|{}-{}|{}|{}\n".format(vrx_pos_l, vry_pos_l, swt_val_l, vrx_pos_r, vry_pos_r, swt_val_r))
