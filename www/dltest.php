<?
	$UserID = 13;
	$db = mysql_connect('localhost','root','W00t3n') or die ('could not connect');
	mysql_select_db('www',$db);
	$row = mysql_query("select ResumeFile from Users where UserID = ".$UserID);
	$info = mysql_fetch_array($row);
	$filename = "myresume.doc";

	header("Content-Disposition: attachment; filename=$filename");
	header("Content-Type: application/force-download");
	header("Content-Type: application/octet-stream");
	header("Content-Type: application/download");
	print $info[0];
	//echo "here";
?>