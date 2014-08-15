<?
error_reporting(E_ALL);
include('includes/db.php');

$db = new Database();
$db->connect('localhost','root','W00t3n','www');

switch ($_POST['action']) {

	case "create":
		$fp = fopen($_FILES['ResumeFile']['tmp_name'],'r');
		$File = fread($fp, filesize($_FILES['ResumeFile']['tmp_name']));
		fclose($fp);

		echo $_FILES['ResumeFile']['tmp_name'] . ' ';
		echo filesize($_FILES['ResumeFile']['tmp_name']);
		
		$db->insert('Users', array(
				'FirstName'=>$_POST['firstname'],
				'LastName'=>$_POST['lastname'],
				'Email'=>$_POST['email'],
				'Street'=>($_POST['address'] . ' ' . $_POST['address2']),
				'City'=>$_POST['city'],
				'State'=>$_POST['state'],
				'Zip'=>$_POST['zip'],
				'Phone'=>$_POST['phone'],
				'Password'=>strrev(md5($_POST['password'])),
				'ResumeFile'=>$File
			));
		$db->close();
		//add code to send email confirmation
		
		//redirect to thank you (with instructions on email conf)
		break;
	
	case "login":
	
		session_start();
		$password = strrev(md5($_POST['password']));
		$rsLogin = $db->query("select * from Users where Email = '".$_POST['email']."'");
		if ($password == $rsLogin->values('Password')) {
			$_SESSION['LoggedIn'] = true;
			$_SESSION['User'] = $rsLogin->values('UserID');
			//insert redirect to account page
			header('Location: http://75.156.91.248:8888/account.php');
		} else {
			header('Location: http://75.156.91.248:8888/create_account.php');
		}
		break;
}	
?>