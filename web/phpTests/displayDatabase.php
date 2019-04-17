<?php
   class MyDB extends SQLite3 {
      function __construct() {
         $this->open('test.db');
      }
   }
   
   $db = new MyDB();
   if(!$db) {
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n<br><br>\n";
   }

   $sql =<<<EOF
      SELECT * from COMPANY;
EOF;

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
      echo "ID = ". $row['ID'] . "<br>\n";
      echo "NAME = ". $row['NAME'] ."<br>\n";
      echo "ADDRESS = ". $row['ADDRESS'] ."<br>\n";
      echo "SALARY = ".$row['SALARY'] ."<br><br>\n\n";
   }
   echo "Operation done successfully<br>\n";
   $db->close();
?>
