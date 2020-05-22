<?php
    //Sintaxis de conexión de la base de datos de muestra para PHP y MySQL.

    //Conectar a la base de datos

    $hostname="localhost";
    $username="root";
    $password="";
    $dbname="backend360";
    $usertable="asunto";
    $yourfield = "";

    mysql_connect($hostname,$username, $password) or die ("html>script language='JavaScript'>alert('¡No es posible conectarse a la base de datos! Vuelve a intentarlo más tarde.'),history.go(-1)/script>/html>");
    mysql_select_db($dbname);

    # Comprobar si existe registro

    $query = “SELECT * FROM $usertable”;

    $result = mysql_query($query);

    if ($result){

    }
 ?>