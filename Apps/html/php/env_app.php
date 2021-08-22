<?php session_start(); ?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="60">
    <title>Server Environmental Sentinel</title>
    <link rel="stylesheet" type="text/css" href="../css/env_app.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
  </head>
  <body>

  <?php 
 
 //Temperature check and generate the class tag for the right color
  function check_temp($temperature){
	if($temperature < 18 || $temperature > 27){
		return '<td class ="fail_color">'.sprintf("%01.2f",$temperature).'</td>';
	} else {
		return '<td class ="ok_color">'.sprintf("%01.2f",$temperature).'</td>';
	}
  }

//Humidity check and generate the class tag for the right color
  function check_humid($humidity){

	$humidity_formated = sprintf("%01.2f",$humidity);

	if($humidity_formated < 40 || $humidity_formated > 50){
		return '<td class ="fail_color">'.$humidity_formated.'</td>';
	} else {
		return '<td class ="ok_color">'.$humidity_formated.'</td>';
	}
  }

//Check the timestamp, if older than 5 min -> set ret color ro red
  function check_time($ts){

  // 1: Read the hh:mm in seperate variables and convert to int
	$ts_unix = strtotime($ts);
	$ts_hour = idate('H', $ts_unix);
	$ts_minute = idate('i',$ts_unix);

  // 2: Convert into decimal 
	$ts_sum = $ts_hour + ($ts_minute * 1/60);

	$time_now_hour = idate('H');
	$time_now_minute = idate('i');
	
	$time_now_sum = $time_now_hour + ($time_now_minute * 1/60);
 
  // 3: Calculate the difference between now and the timestamp
	$div_minutes = ($time_now_sum - $ts_sum) * 60;

  // 4: Generate a tag with red background if difference > 5 min
	if(($div_minutes <= 5) && ($div_minutes >= 0) && (date("Y-m-d") == date("Y-m-d",$ts_unix)))
	{
		return '<td class ="ok_color">'.$ts.'</td>';
	} else
	{
		return '<td class ="fail_color">'.$ts.'</td>';
	}
  }

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
  ?>

  <h2 id ="top_heading" class ="table_header" align ="center"> Server Environmental Data </h2>

  <table class ="data" style ="width:30%" align ="center">

  <tr class ="header""> <th>Type</th> <th>Value</th> <th>Unit</th> </tr>
  <tr align ="center"> <td><?php echo $sensor_data[0];?></td> <?php echo check_temp($sensor_data[1]);  ?> <td><?php echo "°".$sensor_data[2];?></td> </tr>
  <tr align ="center"> <td><?php echo $sensor_data[3];?></td> <td><?php echo sprintf("%01.2f",$sensor_data[4]); ?> </td> <td><?php echo $sensor_data[5];?></td> </tr>
  <tr align ="center"> <td><?php echo $sensor_data[6];?></td> <?php echo check_humid($sensor_data[7]); ?><td><?php echo $sensor_data[8];?></td> </tr>
  <tr align ="center"> <td><?php echo $sensor_data[9];?></td> <?php echo check_time($sensor_data[10]); ?><td></td> </tr>
  </table>

  <footer>Copyright 2020 -  A. Schröder - Avionik Straubing Entwicklungs GmbH - V0.1</footer>

  </body>
</html>
