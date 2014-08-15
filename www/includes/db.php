<?php

class Database {
    
    var $link;
    
    function Database() {
    }
    
    /**
    * connect() connects to the database an SQL statement on the database
    */
    function connect($server, $username, $password, $database) {
        //Connect to the server
        $link = @mysql_connect($server, $username, $password);
        if (!$link)
            return false; //trigger_error("Unable to connect to the MySQL server (${server}, ${username}, ${password}.  Please check your settings and try again.\r\n" . mysql_error());
            
        if (!@mysql_select_db($database))
           return false; // trigger_error("Unable to connect to the database. Please check your settings and try again.\r\n" . mysql_error());
    }
    
    /**
    * query() executes an SQL statement on the database
    */
    function query($queryString) {
        $this->setLastError();

        $result = @mysql_query($queryString);
        if (!$result) {
            if (defined('DEBUG') && DEBUG)
                trigger_error("Query failed: " . mysql_error() . "<BR>{$queryString}");
            return false; 
        }
            
        return new ResultSet($result);
    }

    function execute($statement) {
        $this->setLastError();

        $result = @mysql_query($statement);
        if (!$result) {
            if (defined('DEBUG') && DEBUG) {
                echo $statement;
                trigger_error(mysql_error());
            }
            return false; //trigger_error("Query failed: " . mysql_error());
        }
            
        return true;
    }
    
    function insert($tablename, $fields) {
        $this->setLastError();

        $keys = array_keys($fields);

        $sql = "insert into ${tablename} (";
        foreach($keys as $fieldname)
            $sql .= $fieldname . ",";
        $sql = substr($sql, 0, -1);
        
        $sql .= ") values (";
        foreach($fields as $value) 
            $sql .= $this->prepareValue($value) . ',';
        $sql = substr($sql, 0, -1);
        $sql .= ")";
        
        $result = @mysql_query($sql);
        if (!$result)
			echo mysql_error();
            return false; //trigger_error("Insert failed: \r\n{$sql}\r\n\r\n" . mysql_error());
            
        return $result;
    }    

    function delete($tablename, $condition = "1") {
        $this->setLastError();
        
        $result = @mysql_query("delete from ${tablename}  where ${condition}");
        if (!$result)
            return false; //trigger_error("Delete failed: " . mysql_error());
            
        return $result;
    }

    function update($tablename, $fields, $condition = "1") {
        $this->setLastError();

        $sql = "update $tablename set ";
        foreach($fields as $fieldname=>$value)
            $sql .= $fieldname . "= '" . $value . "', ";
        $sql = substr($sql, 0, -2);
        
        $result = @mysql_query($sql . " where ${condition}");
        if (!$result)
            return false; //trigger_error($sql . " where ${condition}" . ">>>Update failed: " . mysql_error());
            
        return $result;
    }
    
	function close() {
		mysql_close($link);
	}

	function lastInsertId() {
        return mysql_insert_id();
    }    
    
    function lastError() {
        if (isset($this->lasterrorstr))
            return $this->lasterrorstr;
        else
            return mysql_error();
    }
    
    function setLastError($str = null) {
        if (null == $str)
            unset($this->lasterrorstr);
        else
            $this->lasterrorstr = $str;
    }
    
    function prepareValue($value) {
        if (is_bool($value)) {
            return ($value ? '1' : '0');
        } elseif (is_int($value) || is_float($value)) {
            return "{$value}";
        } elseif (is_null($value)) {
            return 'null';
        } elseif (substr($value, 0, 1) == '#') { //Make room for functions, etc.
            return substr($value, 1);
        } else { //Treat as string
		    if (function_exists('mysql_real_escape_string')) {
      			$value = mysql_real_escape_string($value);
		    } elseif (function_exists('mysql_escape_string')) {
      			$value = mysql_escape_string($value);
    		} else {
      			$value = addslashes($value);
    		}
			return "'{$value}'";
        }
    }
    
    function dateValue($time = null) {
        if (null === $time)
            $time = time();
        return date('Y-m-d H:i:s', $time);
    }
    
    function datetimeToPHPTime($dt) {

        $year = (int)substr($dt, 0, 4);
        $month = (int)substr($dt, 5, 2);
        $day = (int)substr($dt, 8, 2);
        $hour = (int)substr($dt, 11, 2);
        $minute = (int)substr($dt, 14, 2);
        $second = (int)substr($dt, 17, 2);

        $result = @mktime($hour, $minute, $second, $month, $day, $year);
        return $result;
        
    }
}

class ResultSet {
    
    var $result;
    var $resultSet = array();
    var $num_rows;
    
    function ResultSet($result) {
        $this->result = $result;
        $this->num_rows = mysql_num_rows($result);
        
        while ($arr = mysql_fetch_array($result, MYSQL_ASSOC))
            $this->resultSet[] = $arr;
            
        mysql_free_result($result);
        
        $this->moveFirst();
    }
    
    function getRecordCount() {
        return $this->num_rows;
    }
  
    function values($field) {
        $arr = current($this->resultSet);
        if ($arr == false)
            return null;
        else
            return $arr[$field];
    }
    
    function moveFirst() {
        reset($this->resultSet);
    }
    
    function moveLast() {
        end($this->resultSet);
    }
    
    function moveNext() {
        next($this->resultSet);
    }
    
    function movePrevious() {
        prev($this->resultSet);
    }

    function moveTo($record_number) {
        //hack
        reset($this->resultSet);
        for ($i = 1; $i < $record_number; $i++)
            next($this->resultSet);
    }
    
    function asArray() {
        return current($this->resultSet);
    }
    
    function eof() {
        return (current($this->resultSet) == false);
    }

    function find($value, $field) {
        return false;
    }
    
}

?>