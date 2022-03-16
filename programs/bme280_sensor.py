import bme280
import smbus2
import database
from time import sleep


db = database.weather_database() #Local MySQL db



port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

bme280_data = bme280.sample(bus,address)
humidity  = bme280_data.humidity
pressure  = bme280_data.pressure
ambient_temperature = bme280_data.temperature
print(humidity, pressure, ambient_temperature)

print("Inserting...")
db.insert(0, temperature, 0, pressure, humidity,0)
print("done")
