from time import sleep
from rpi_ws281x import PixelStrip, Color
import argparse

class ws2812:
    def init(self, LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_BRIGHTNESS):
        LED_DMA = 10
        LED_INVERT = False
        LED_CHANNEL = 0

        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()


    def color_display(self, disp_list=[]):
        if len(disp_list[1]) != self.strip.numPixels() or len(disp_list) == 0:
            raise ValueError("The number of LEDs exceeds the set value.")
        else:
            # disp_listは[brightness, [color...]] の二次元配列
            for i in range(self.strip.numPixels()):
                if disp_list[1][i] != -1:
                    self.strip.setPixelColor(i, self.wheel(disp_list[1][i]))
                else:
                    self.strip.setPixelColor(i, Color(0, 0, 0))
            self.strip.show()




    def wheel(self, pos):
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

if __name__ == "__main__":
    led_strip = ws2812(LED_COUNT=110, LED_PIN=18, LED_FREQ_HZ=800000, LED_BRIGHTNESS=255)

    for i in range(10, 10, 110):
        print(i)
        sleep(0.2)
    # led_strip.colorWipe(color=20, count=10)