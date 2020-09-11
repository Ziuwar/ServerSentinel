 <?php 

//echo date('Y-m-d H:i:s');
//phpinfo();

//Open the file
$file_data = fopen("/home/pi/Documents/BME280_Data/chip_data.txt", "r");

//Read 4 x 3 rows of sensor data (Temp, Pressure, Humidity, Timestamp)
if($file_data)
{	
	$count = 0;

	while((($buffer = fgets($file_data)) !== false) && ($count <= 11))
	{
		$sensor_data[$count] = $buffer;
		++$count;
	} 
	if(!feof($file_data))
	{
		echo "Fehler: fgets() fehlgeschlagen!";
	}
}
//Close the file
fclose($file_data);

echo "Hallo:".$sensor_data[1];
echo "Testtest";

?>

