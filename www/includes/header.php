<?php ?>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="utf-8" />
  <!--[if IE]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
  <!--[if lt IE 9]><script src="http://css3-mediaqueries-js.googlecode.com/svn/trunk/css3-mediaqueries.js"></script><![endif]-->
  <title></title>
  <meta name="keywords" content="" />
  <meta name="description" content="" />
  <link rel="stylesheet" href="css/style.css" type="text/css" media="screen, projection" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script language="javascript">
    function showUpload(hide) {
	 if (hide == 'undo') {
  	   document.getElementById('uploadBox').style.display='none';
	   document.getElementById('greyOut').style.display='none';
	 } else {
	   document.getElementById('uploadBox').style.display='block';
	   document.getElementById('greyOut').style.display='block';
	 }
	}
  </script>
</head>

<body>

<div id="wrapper">

  <header id="header">
    <a href="index.php"><img src="images/logo.png" id="logo" border="0"></a>
	<a href="index.php">Home</a> <a href="create_account.php">Login</a> <a href="about.php">About</a> <a href="contact.php">Contact</a>
  </header><!-- #header-->
