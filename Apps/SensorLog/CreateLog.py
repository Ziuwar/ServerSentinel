##########################################
# App to create and clear the sensor log #
#                                        #
# Avionik Straubing Entwicklungs GmbH    #
#                                        #
# Andreas Schroeder, 01.10.2020          #
# Rev.: 1.0.0                            #
##########################################

from os import path

sensor_data_path = "/home/pi/Documents/BME280_Data/chip_data.txt"
sensor_data_log_path = "/home/pi/Documents/SensorLog/chip_data_log.txt"

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

#Format the sensor data for the log file
def format_data(sensor_data):
	data_string = sensor_data[10]+"|"+sensor_data[0]+": "+sensor_data[1][0:5]+" "+sensor_data[2]+"|"+sensor_data[3]+": "+sensor_data[4][0:6]+" "+sensor_data[5]+"|"+sensor_data[6]+": "+sensor_data[7][0:5]+" %|\r\n"
	return data_string

#Write log
def write_log(data_string):

	#Check if the files exists
	if path.isfile(sensor_data_log_path):

		#If file exists append the data
		with open(sensor_data_log_path, "a") as data_log:
			data_log.write(data_string)
	else:
		#If the file doesent exist create the file and write the data
		with open(sensor_data_log_path, "w") as data_log:
			data_log.write(data_string)

#Main routine
def main():

	#Format the data
	string_to_file = format_data(read_file(sensor_data_path))
	#print string_to_file

	#Write the file
	write_log(string_to_file)

#Main namespace
if __name__=="__main__":
 	main()

