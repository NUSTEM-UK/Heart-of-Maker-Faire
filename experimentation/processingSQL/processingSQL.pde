// MySQL test reads

import de.bezier.data.sql.*;

MySQL mysql;

void setup() {
  size(100,100);

  String user = "root";
  String pass = "plokij";

  String server = "192.168.0.28";
  String dbname = "Heart";

  mysql = new MySQL( this, server, dbname, user, pass );

  if ( mysql.connect() ) {
    mysql.query( "SELECT * FROM heart_store");

    while (mysql.next()) {
      int heartNum = mysql.getInt("cell_id");
      int heartRate = mysql.getInt("heart_rate");
      println( "Heart: " + heartNum + " :: Rate : " + heartRate);
      // something like:  hearts[heartNum].setRate(heartRate);
      // Probably need to do something with hearts not pulled from database,
      // so zero all the rates first?
    }

  } else {
    // Connection failed!
  }



}

void draw() {
  //
}
