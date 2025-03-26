<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<title>Photo Album</title>

    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f6f8;
        margin: 0;
        padding: 0;
    }

    h2 {
        text-align: center;
        color: #333;
        margin-top: 40px;
    }

    form {
        max-width: 500px;
        margin: 20px auto;
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    fieldset {
        border: none;
        padding: 0;
        margin: 0;
    }

    dl {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    dt {
        margin-bottom: 5px;
        font-weight: bold;
        color: #444;
    }

    dd {
        margin: 0;
    }

    input[type="text"],
    input[type="date"] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 14px;
    }

    input[type="submit"] {
        background-color: #007BFF;
        color: #fff;
        padding: 12px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
        transition: background-color 0.3s ease;
        width: 100%;
    }

    input[type="submit"]:hover {
        background-color: #0056b3;
    }

    p {
        text-align: center;
        margin-top: 20px;
    }

    a {
        color: #007BFF;
        text-decoration: none;
        font-weight: bold;
    }

    a:hover {
        text-decoration: underline;
    }
</style>


</head>
<body>
<h2>Photo lookup</h2>
<form name="upload" id="upload">
<fieldset>
	<dl>
		<dt><label for="phototitle">Photo title: </label></dt>
		<dd><input type="text" name="phototitle" id="phototitle" size="25" /></dd>
		<dt><label for="keyword">Keyword: </label></dt>
		<dd><input type="text" name="keyword" id="keyword" size="25" /></dd>
		<dt><label for="fromdate">From Date: </label></dt>
		<dd><input type="date" name="fromdate" id="fromdate" /></dd>
		<dt><label for="todate">To Date: </label></dt>
		<dd><input type="date" name="todate" id="todate" /></dd>
		<dt><input type="submit" value="Search"/> <!-- Submit Button --></dt>
	</dl>
</fieldset>
</form>
<p><a href="photouploader.php" title="Photo Uploader">Photo Uploader</a></p>
</body>
</html>
