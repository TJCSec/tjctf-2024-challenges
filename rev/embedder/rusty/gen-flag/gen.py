import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# morse mapping
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ',':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', ' ':'/'}


flag = open(f"{dir_path}/flag.txt", "r").read().strip()

flag = flag.replace("_", " ")
flag = flag.replace("{", "(")
flag = flag.replace("}", ")")


flag = flag + " replace parentheses with curly braces,letters are lowercase"

flag_enc = " ".join([MORSE_CODE_DICT[c] for c in flag.upper()])

with open(f"{dir_path}/../src/flag.rs", "w") as f:
    f.write("""
use esp_idf_hal::{
    delay::Delay,
    gpio::{Gpio22, Output, PinDriver}
};

#[inline(always)]
pub fn light_flag(led: &mut PinDriver<Gpio22, Output>, delay: &Delay) {
""")
        
    for c in flag_enc:
        match c:
            case '.':
                f.write("   led.set_high().unwrap();\n")
                f.write("   delay.delay_ms(100);\n")
                f.write("   led.set_low().unwrap();\n")
                f.write("   delay.delay_ms(100);\n")
            case '-':
                f.write("   led.set_high().unwrap();\n")
                f.write("   delay.delay_ms(300);\n")
                f.write("   led.set_low().unwrap();\n")
                f.write("   delay.delay_ms(100);\n")
            case '/':
                f.write("   delay.delay_ms(300);\n")
            case ' ':
                f.write("   delay.delay_ms(100);\n")
    
    f.write("}\n")
