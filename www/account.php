<?
session_start();
if ($_SESSION['LoggedIn'] == true) {

include('includes/db.php');

$db = new Database();
$db->connect('localhost','root','W00t3n','www');

include('includes/header.php');
?>

<section id="middle">
Account info here.<br><br>

Results here (or link here).<br><br>


<?
include('includes/footer.php');
}

else {
header('Location: create_account.php');
}

?>