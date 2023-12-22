# Import necessary libraries
import time
import board
import busio
import adafruit_bh1750
from adafruit_hid.mouse import Mouse
from adafruit_hid.mouse_button import MouseButton
import adafruit_dotstar as dotstar
from datetime import datetime

# Constants
NUM_CLICKS = 10  # Number of mouse clicks to perform for latency testing
PAUSE_BETWEEN_CLICKS = 1  # Time in seconds to pause between clicks
MUZZLE_FLASH_THRESHOLD = 1000  # Light level threshold to detect a 'muzzle flash'
COUNTDOWN_SECONDS = 5  # Duration of the countdown before starting the test

# Initialize I2C, sensor, mouse, and LED
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bh1750.BH1750(i2c, mode=adafruit_bh1750.CONTINUOUS_HIGH_RES_MODE)
mouse = Mouse()
led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.1)

def countdown():
    """Perform a countdown with visual feedback using an LED."""
    for _ in range(COUNTDOWN_SECONDS):
        led[0] = (255, 0, 0)  # Red color
        led.show()
        time.sleep(0.5)
        led[0] = (0, 0, 0)  # Turn off LED
        led.show()
        time.sleep(0.5)

def detect_muzzle_flash():
    """Detect the muzzle flash based on a threshold of light level."""
    while True:
        light_level = sensor.lux  # Read light level from the sensor
        if light_level >= MUZZLE_FLASH_THRESHOLD:
            return light_level

def main():
    """Main function to execute the latency testing process."""
    countdown()  # Perform countdown before starting the test
    led[0] = (0, 255, 0)  # Green color to indicate start
    led.show()

    # Prepare the file for recording latency data
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"/CIRCUITPY/latency_{timestamp}.csv"
    with open(filename, "w") as f:
        f.write("click_number,latency_ms\n")

        # Perform a series of mouse clicks and measure the latency
        for i in range(NUM_CLICKS):
            mouse.click(MouseButton.LEFT)  # Simulate a mouse click
            click_time = time.monotonic()  # Record the time of the click
            detect_muzzle_flash()  # Wait for the muzzle flash detection
            flash_time = time.monotonic()  # Record the time when flash is detected
            latency = (flash_time - click_time) * 1000  # Calculate latency in milliseconds
            f.write(f"{i + 1},{latency:.2f}\n")  # Write the latency data to the file
            time.sleep(PAUSE_BETWEEN_CLICKS)  # Pause between clicks

    led[0] = (0, 0, 0)  # Turn off LED after test completion
    led.show()

if __name__ == "__main__":
    main()  # Execute the main function
