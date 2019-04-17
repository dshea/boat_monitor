<?php

class BoatDB extends SQLite3 {
  function __construct() {
    $this->open('boat.db');
  }
}


function open_database() {
  $db = FALSE;
  if(file_exists('boat.db')) {
    //echo "database exists<br>\n";
    $db = new BoatDB();
  } else {
    //echo "database does not exists<br>\n";
    $db = new BoatDB();
    $sql =<<<EOF
      CREATE TABLE bilge
      (time INT PRIMARY KEY NOT NULL,
       pump INT,
       duration INT);
EOF;
    $ret = $db->exec($sql);
    if(!$ret){
      die($db->lastErrorMsg());
    }

    $sql =<<<EOF
      CREATE TABLE voltage
      (time INT PRIMARY KEY NOT NULL,
       bank0 REAL,
       bank1 REAL,
       temp REAL,
       humidity REAL);
EOF;
    $ret = $db->exec($sql);
    if(!$ret){
      die($db->lastErrorMsg());
    }

  } // database does not exist
  return $db;
}

function add_bilge_record($db, $rec) {
  $timestamp = new DateTime($rec->time);
  //echo $rec->time, ", ", $timestamp->getTimestamp(), ", ", $rec->duration, "<br>\n";
  $sql = sprintf("INSERT INTO bilge (time,pump,duration) \n VALUES (%d, %d, %d);\n",
		 $timestamp->getTimestamp(), $rec->pump, $rec->duration);

  $ret = $db->exec($sql);
  if(!$ret) {
    die($db->lastErrorMsg() . "<br>\n");
  }
}

function add_voltage_record($db, $rec) {
  $timestamp = new DateTime($rec->time);
  //echo $rec->time, ", ", $timestamp->getTimestamp(), ", ", $rec->bank0, "<br>\n";
  $sql = sprintf("INSERT INTO voltage (time,bank0,bank1,temp,humidity) \n VALUES (%d, %f, %f, %f, %f);\n",
		 $timestamp->getTimestamp(), $rec->bank0, $rec->bank1, $rec->temp, $rec->humidity);

  $ret = $db->exec($sql);
  if(!$ret) {
    die($db->lastErrorMsg() . "<br>\n");
  }
}

function add_json_files($db) {
  //echo "json files in dir<br>\n";
  $files = scandir(dirname(__FILE__));
  foreach($files as $filename) {
    if(strpos($filename, ".json") != FALSE) {
      //echo "    -", $filename, "-<br>\n";
      $json_str = file_get_contents($filename);
      $data = json_decode($json_str);

      // loop bilge
      foreach($data->bilge as $rec) {
	add_bilge_record($db, $rec);
      }
      
      // loop voltage
      foreach($data->voltage as $rec) {
	add_voltage_record($db, $rec);
      }

      // move json file to loaded dir
      rename($filename, "loadedFiles/" . $filename);
      
    } // if json file
  } // for files
}


// open database
$db = open_database();

// loop through json files
// add them to database
// delete json file
add_json_files($db);


// query database
$sql = "SELECT * from bilge;";
$ret = $db->query($sql);
$bilge0_cycle_data = "";
$bilge1_cycle_data = "";
$bilge0_on_data = "";
$bilge1_on_data = "";
$last_time0 = 0;
$last_time1 = 0;
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
  if($row["pump"] == 0) {
    if($last_time0 == 0) {
      $last_time0 = $row["time"];
    } else {
      $delta = $row["time"] - $last_time0;  // number of seconds between bilge cycles
      $bilge0_cycle_data .= sprintf("{ x: new Date(%d), y: %f },\n", $row["time"] * 1000, $delta / 60.0);
      $bilge0_on_data .= sprintf("{ x: new Date(%d), y: %d },\n", $row["time"] * 1000, $row["duration"]);
      $last_time0 = $row["time"];
    }
  } else if($row["pump"] == 1) {
    if($last_time1 == 0) {
      $last_time1 = $row["time"];
    } else {
      $delta = $row["time"] - $last_time1;  // number of seconds between bilge cycles
      $bilge1_cycle_data .= sprintf("{ x: new Date(%d), y: %f },\n", $row["time"] * 1000, $delta / 60.0);
      $bilge1_on_data .= sprintf("{ x: new Date(%d), y: %d },\n", $row["time"] * 1000, $row["duration"]);
      $last_time1 = $row["time"];
    }
  }
}

$sql = "SELECT * from voltage;";
$ret = $db->query($sql);
$bank0_data = "";
$bank1_data = "";
$temp_data = "";
$humidity_data = "";
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
  $bank0_data .= sprintf("{ x: new Date(%d), y: %f },\n", $row["time"] * 1000, $row["bank0"]);
  $bank1_data .= sprintf("{ x: new Date(%d), y: %f },\n", $row["time"] * 1000, $row["bank1"]);
  $temp_data .= sprintf("{ x: new Date(%d), y: %f },\n", $row["time"] * 1000, $row["temp"]);
  $humidity_data .= sprintf("{ x: new Date(%d), y: %f },\n", $row["time"] * 1000, $row["humidity"]);
}


// write out plot javascript

echo '

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.13.0/moment.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.min.js"></script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <title>My Chart.js Chart</title>
</head>
<body>

<p>A line chart is a way of plotting data points on a line. Often, it is used to show trend data, or the comparison of two data sets.</p>

<p><div class="chartjs-wrapper"><canvas id="chartjs-0" class="chartjs" width="undefined" height="undefined"></canvas>

<script>
new Chart(document.getElementById("chartjs-0"),{
    "type":"line",
    "data":{
        "datasets":[{
            "label":"My First Dataset",
            "data":[{ x: new Date(1547100000*1000), y: 5 },
                    { x: new Date("2019-01-10T06:10:00"), y: 4 },
                    { x: new Date("2019-01-10T06:20:00"), y: 3 },
                    { x: new Date("2019-01-10T06:30:00"), y: 2.5 },
                    { x: new Date("2019-01-10T06:40:00"), y: 2.4 },
                    { x: new Date("2019-01-10T06:45:00"), y: 2.6 },
                    { x: new Date("2019-01-10T06:50:00"), y: 4 },
                    { x: new Date("2019-01-10T06:55:00"), y: 6 }
            ],
            "fill":false,
            //"borderColor":"rgb(75, 192, 192)",
            //"lineTension":0.1
        }]
    },
    "options":{
        scales: {
            xAxes: [{
                type: "time",
                //distrubution: "linear",
                //time: { unit: "day"},
                //type: "linear",
                position: "bottom"
            }]
        }
    }
});

</script>

</div></p>

</body>
</html>
';


// query database
$sql = "SELECT * from bilge;";
$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
  echo "time = ", $row["time"], "<br>\n";
  echo "pump = ", $row["pump"], "<br>\n";
  echo "duration = ", $row["duration"]. "<br><br>\n\n";
}


// close database
$db->close();
//echo "closed the file<br>\n"



?>


