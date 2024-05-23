mod flag;

use esp_idf_hal::{delay::Delay, gpio::PinDriver, peripherals::Peripherals};

fn main() {
    // It is necessary to call this function once. Otherwise some patches to the runtime
    // implemented by esp-idf-sys might not link properly. See https://github.com/esp-rs/esp-idf-template/issues/71
    esp_idf_svc::sys::link_patches();

    // Bind the log crate to the ESP Logging facilities
    esp_idf_svc::log::EspLogger::initialize_default();

    let peripherals = Peripherals::take().unwrap();

    let gpio22 = peripherals.pins.gpio22;
    let mut led = PinDriver::output(gpio22).unwrap();

    let gpio23 = peripherals.pins.gpio23;
    let mut button = PinDriver::input(gpio23).unwrap();
    button.set_pull(esp_idf_hal::gpio::Pull::Down).unwrap();

    let delay = Delay::default();

    loop {
        if button.is_low() {
            delay.delay_ms(10);
            continue;
        }

        delay.delay_ms(300);
        if button.is_high() {
            delay.delay_ms(10);
            continue;
        }

        delay.delay_ms(400);
        if button.is_low() {
            delay.delay_ms(10);
            continue;
        }

        delay.delay_ms(200);
        if button.is_high() {
            delay.delay_ms(10);
            continue;
        }

        delay.delay_ms(800);
        if button.is_low() {
            delay.delay_ms(10);
            continue;
        }

        flag::light_flag(&mut led, &delay);

        delay.delay_ms(100);
    }
}
