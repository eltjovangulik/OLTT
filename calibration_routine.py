import time
import board
import busio
from adafruit_bh1750 import BH1750

# Initialize the BH1750 light sensor
i2c = busio.I2C(board.SCL, board.SDA)
light_sensor = BH1750(i2c)

def detect_light_change(threshold=50):
    """
    Detects a significant change in light level.
    
    Args:
        threshold (int): The change in light level required to register as a significant event.
    
    Returns:
        None
    """
    prev_light_level = light_sensor.read_lux()
    while True:
        current_light_level = light_sensor.read_lux()
        change = abs(current_light_level - prev_light_level)

        if change >= threshold:
            break

        prev_light_level = current_light_level
        time.sleep(0.01)

def calibration_measurements(num_measurements, pattern_interval):
    """
    Performs a series of calibration measurements.
    
    Args:
        num_measurements (int): Number of measurements to take.
        pattern_interval (float): The time interval in seconds between pattern changes.
    
    Returns:
        list: A list of latency measurements.
    """
    calibration_data = []

    for _ in range(num_measurements):
        # Wait for the pattern change event
        time.sleep(pattern_interval)

        # Record the time of the pattern change event
        event_time = time.monotonic()

        # Wait for the sensor to detect the light change
        detect_light_change()

        # Record the time of the detected light change
        light_change_time = time.monotonic()

        # Calculate the latency
        latency = (light_change_time - event_time) * 1000  # Convert to milliseconds
        calibration_data.append(latency)

    return calibration_data

def save_calibration_data(calibration_data, file_name="calibration.txt"):
    """
    Saves the calibration data to a file.
    
    Args:
        calibration_data (list): List of latency measurements.
        file_name (str): File name for saving the data.
    
    Returns:
        None
    """
    with open(file_name, "w") as f:
        for latency in calibration_data:
            f.write(f"{latency}\n")

# Calibration process
num_calibration_measurements = 10
pattern_interval = 1  # This should match the interval of the black and white pattern
calibration_data = calibration_measurements(num_calibration_measurements, pattern_interval)
save_calibration_data(calibration_data)
