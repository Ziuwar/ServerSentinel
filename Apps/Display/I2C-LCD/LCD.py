##########################################
# LCD app for env. sensor data display   #
#					 #
# Avionik Straubing Entwicklungs GmbH	 #
#					 #
# Andreas Schroeder, 17.09.2020		 #
# Rev.: 1.0.0				 #
##########################################

import lcddriver
from time import*
import datetime

#Create an instance from the LCD method
lcd = lcddriver.lcd()
lcd.lcd_clear()

#Reads the sensor data file
def  read_file(file_loc):

	#Read the data from file
	with open(file_loc,"r") as file_data:

		#Read datasets (Read 12 lines of sensor data)
		sensor_data = ["\n","\n","\n","\n","\n","\n","\n","\n","\n","\n","\n","\n"]
		count = 0

		#Read the 12 lines of text from the file
		while count <= 11:

			sensor_data[count] = (file_data.readline()).rstrip()
			count = count + 1

			#Set the counter to invlid if data is missing (less than 12 lines)
			if sensor_data[count-1] == '':
				count = 12

		return sensor_data

#Check of the temperature is in ok range (> 18 or < 27) where 1 is OK and 0 is fail
def check_temp(temperature):
	if float(temperature) >= 18.00 and float(temperature) <= 27.00:
		return 1
	else:
		return 0

#Check of the humidity is in ok range (> 40 or < 50) where 1 is OK and 0 is fail
def check_humid(humidity):
	if float(humidity) >= 40.00 and float(humidity) <= 50.00:
		return 1
	else:
		return 0

#Check if the timestamp is not older than 5 min. Return 1 if OK and 0 if fail
def check_timestamp(timestamp):
	#Read the the current time
	now = datetime.datetime.now()

	#Convert the timestamp from datetime and decimal
	timestamp_d = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
	timestamp_dez = timestamp_d.hour + timestamp_d.minute * 1./60.

	#Convert the current time from datetime to decimal
	now_dez = int(now.hour) + int(now.minute) * 1./60.
	#Calculate the sensor data age
	data_age = round((now_dez - timestamp_dez) * 60)

	print('Data Age: ',data_age)

	#Return 1 for valid age and 0 if the data is older than 5 min
	if data_age >= 0.0 and data_age < 5.0:
		print('Time Valid')
		return 1
	else:
		print('Time Invalid')
		return 0

#Read the sensor data file
sensor_data = read_file("/home/pi/Documents/BME280_Data/chip_data.txt")

#Check for the right number of lines (12), all other cases shall give an error
if len(sensor_data) == 12:

	#check_data_age = check_timestamp("2020-09-29 08:55")
	check_data_age = check_timestamp(sensor_data[10])

	#Check if timestamp OK
	if  check_data_age == 1:
		#Format the data - Display 20 X 4
		#Temperature
		if check_temp(sensor_data[1]) == 1:
			Temperature = sensor_data[0] + " " + sensor_data[1][0:5] + " " + sensor_data[2]
		else:
			Temperature = "Temp.Alert! " + sensor_data[1][0:5] + " " + sensor_data[2]
		#Pressure
		Pressure = sensor_data[3] + " " + sensor_data[4][0:6] + " " + sensor_data[5]
		#Humidity
		if check_humid(sensor_data[7]) == 1:
			Humidity = sensor_data[6] + " " + sensor_data[7][0:5] + " " + sensor_data[8]
		else:
			Humidity = "Humid.Alert! " + sensor_data[7][0:5] + " " + sensor_data[8]
		#Timestamp
		Timestamp = sensor_data[10]

		#Send data to LCD
		lcd.lcd_display_string(Temperature.rstrip(),1)
		lcd.lcd_display_string(Pressure.rstrip(),2)
		lcd.lcd_display_string(Humidity.rstrip(),3)
		lcd.lcd_display_string(Timestamp.rstrip(),4)

	else:
		#Send data to LCD
		lcd.lcd_display_string("Timestamp Error",1)
else:
	lcd.lcd_display_string("Sensor Data Error",1)
