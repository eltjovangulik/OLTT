import time
import board
import busio
from adafruit_bh1750 import BH1750
from adafruit_hid.mouse import Mouse
from adafruit_hid.mouse_button import MouseButton
import adafruit_dotstar as dotstar
import os

# Initialize sensor, mouse, and LED
i2c = busio.I2C(board.SCL, board.SDA)
light_sensor = BH1750(i2c)
mouse = Mouse()
led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.1)

# Constants
NUM_CLICKS = 10
PAUSE_BETWEEN_CLICKS = 1
MUZZLE_FLASH_THRESHOLD = 1000
COUNTDOWN_SECONDS = 5

# Check for calibration data
avg_calibration_latency = 0
if "calibration.txt" in os.listdir("/CIRCUITPY"):
    with open("/CIRCUITPY/calibration.txt", "r") as f:
        latencies = [float(line.strip()) for line in f if line.strip()]
        if latencies:
            avg_calibration_latency = sum(latencies) / len(latencies)

def detect_muzzle_flash():
    """Detect the muzzle flash based on a threshold of light level."""
    while True:
        light_level = sensor.lux  # Read light level from the sensor
        if light_level >= MUZZLE_FLASH_THRESHOLD:
            return light_level

def countdown():
    """Perform a countdown with visual feedback using an LED."""
    for _ in range(COUNTDOWN_SECONDS):
        led[0] = (255, 0, 0)  # Red color
        led.show()
        time.sleep(0.5)
        led[0] = (0, 0, 0)  # Turn off LED
        led.show()
        time.sleep(0.5)

def main():
    countdown()
    led[0] = (0, 255, 0)
    led.show()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"/CIRCUITPY/latency_{timestamp}.csv"
    with open(filename, "w") as f:
        f.write("click_number,latency_ms\n")

        for i in range(NUM_CLICKS):
            mouse.click(MouseButton.LEFT)
            click_time = time.monotonic()
            detect_muzzle_flash()
            flash_time = time.monotonic()
            latency = (flash_time - click_time) * 1000
            adjusted_latency = latency - avg_calibration_latency

            f.write(f"{i + 1},{adjusted_latency:.2f}\n")
            time.sleep(PAUSE_BETWEEN_CLICKS)

    led[0] = (0, 0, 0)
    led.show()

if __name__ == "__main__":
    main()
