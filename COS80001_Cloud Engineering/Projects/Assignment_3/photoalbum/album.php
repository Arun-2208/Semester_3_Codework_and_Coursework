<?php
/**
* 	Showing all photos in DB
*
*	@author Arun Ragavendhar Arunachalam Palaniyappan - 104837257
*/
ini_set('display_errors', 1);
require 'mydb.php';
require_once 'constants.php';
?>
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="defaultstyle.css">
    <title>Photo Album</title>
  </head>
  <body>
    <div class="container">
      <header>
        <h1>Photo Album</h1>
      </header>
      <div class="student-info">
        <h4>Student name: <?php echo STUDENT_NAME; ?></h4>
        <h4>Student ID: <?php echo STUDENT_ID; ?></h4>
        <h4>Tutorial session: <?php echo TUTORIAL_SESSION; ?></h4>
      </div>
      <h3>Uploaded photos:</h3>
      <table id="photo_table" border= "1" >
        <tr>
          <th>Photo</th>
          <th>Name</th> 
          <th>Description</th>
          <th>Creation date</th>
          <th>Keywords</th>
        </tr>
        <?php 
          $my_db = new MyDB();
          $photos = $my_db->getAllPhotos();
          foreach ($photos as $photo) {
            echo "<tr>";
            echo "<td><img class='photo_cell' src='" . $photo->getS3Reference() . "' alt='" . $photo->getName() . "' /></td>";
            echo "<td>" . $photo->getName() . "</td>";
            echo "<td>" . $photo->getDescription() . "</td>";
            echo "<td>" . $photo->getCreationDate() . "</td>";
            echo "<td>" . $photo->getKeywords() . "</td>";
            echo "</tr>";
          }
        ?>
      </table>
    </div>
  </body>
</html>
