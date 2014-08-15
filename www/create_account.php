<?
	include('includes/header.php');
?>

  <section id="middle">
	
	<div id="create_account">
		<form enctype="multipart/form-data" class="formLayout" method="post" action="actions.php">
			<input type="hidden" name="action" value="create">
			<b>Create your account:</b><br><br>
			<label>Email:</label>
			<input name="email"><br>
			<label>Password:</label>
			<input type="password" name="password"><br>
			<label>Confirm:</label>
			<input name="confirm"><br>
			<label>First Name:</label>
			<input name="firstname"><br>
			<label>Last Name</label>
			<input name="lastname"><br>
			<label>Address:</label>
			<input name="address"><br>
			<label></label>
			<input name="address2"><br>
			<label>City:</label>
			<input name="city"><br>
			<label>State/Prov:</label>
			<input name="state"><br>
			<label>Zip/Postal:</label>
			<input name="zip"><br>
			<label>Phone:</label>
			<input name="phone"><br><br>
			<label>Resume file:</label>
			<input type="file" name="ResumeFile"><br><br>
			<input type="submit" value="Create Account">
		</form>	
  </div>
	<div id="login">
		<form class="login" method="post" action="actions.php">
			<input type="hidden" name="action" value="login">
			<b>Login to your account</b><br><br>
			<label>Email:</label>
			<input name="email"><br>
			<label>Password:</label>
			<input type="password" name="password"><br><br>
			<input type="submit" value="Login">					
		</form>
	</div>

<?
	include('includes/footer.php');
?>	