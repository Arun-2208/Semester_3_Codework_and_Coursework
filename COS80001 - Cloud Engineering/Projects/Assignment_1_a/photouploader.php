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
    input[type="date"],
    input[type="file"] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 14px;
    }

    input[type="submit"] {
        background-color: #28a745;
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
        background-color: #218838;
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

    #keywordid {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    #keywordid label {
        font-weight: bold;
        color: #444;
    }

    #keywordid input {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 14px;
    }
</style>


</head>
<body>
<h2>Photo uploader</h2>
<form name="upload" id="upload">
<fieldset>
	<dl>
		<dt><label for="phototitle">Photo title: </label></dt>
		<dd><input type="text" name="phototitle" id="phototitle" size="25" /></dd>
		<dt><label for="selectphoto">Select a photo: </label></dt>
		<dd><input type="file" name="selectphoto" id="selectphoto" /></dd>
		<dt><label for="description">Description: </label></dt>
		<dd><input type="text" name="description" id="description" size="25" /></dd>
		<dt><label for="date">Date: </label></dt>
		<dd><input type="date" name="date" id="date" /></dd>
		<dt id="keywordid">
			<label for="keywords">Keywords (comma-delimited e.g. keyword1; keyword 2, ...):</label>
			<input type="text" name="keywords" id="keywords" size="25" />
		</dt>
		<dt><input type="submit" value="Upload"/> <!-- Submit Button --></dt>
	</dl>
</fieldset>
</form>
<p><a href="photolookup.php" title="Photo Lookup">Photo Lookup</a></p>
</body>
</html>
