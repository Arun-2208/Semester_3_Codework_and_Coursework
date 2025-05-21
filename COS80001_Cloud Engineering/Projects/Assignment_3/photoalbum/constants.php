<?php
/**
* 	All constants defined in this file
*
*	@author Arun Ragavendhar Arunachalam Palaniyappan
*
*
*	============ READ ME !!! ============ 
* 	============ READ ME !!! ============ 
* 	============ READ ME !!! ============ 
*
*	Directory structure:
*	var
*	└───www
*		└───html
*			└───cos80001
*	    		└───photoalbum (this directory contains source files of the PhotoAlbum website)
*	   				│   album.php 					(executable) display all images in DB
*	   				│   const.php 					Constants defined here
*	   				│   defaultstyle.css			CSS style for the website
*	   				│   mydb.php					Interact with DB
*	   				│   photo.php					Photo object class
*	   				│
*	
*	
*	The values of the constant variables with "[ACTION REQUIRED]" in the comment must be updated. The current values are just examples.
*	You need to replace the values of those constant variables with values specific to your setup.
*
* 	
* 	============ READ THE ABOVE !!! ============ 
* 	============ READ THE ABOVE !!! ============ 
* 	============ READ THE ABOVE !!! ============ 
*/

// [ACTION REQUIRED] your full name
define('STUDENT_NAME', 'Arun Ragavendhar Arunachalam Palaniyappan');
// [ACTION REQUIRED] your Student ID
define('STUDENT_ID', '104837257');
// [ACTION REQUIRED] your tutorial session
define('TUTORIAL_SESSION', 'Friday 04:30 PM - 06:30 PM');

// [ACTION REQUIRED] name of the object storage bucket that stores images
define('BUCKET_NAME', 'ARagavendhar_bucket');
// [ACTION REQUIRED] region of the above bucket
define('REGION', 'us-ashburn-1');
// no need to update this const
define('S3_BASE_URL','https://objectstorage.us-ashburn-1.oraclecloud.com/p/Z1fthmgQp1OaL7xhTY6_r_uCaZslurGH9PVmvUY1K7hjbLpgSBGZs_JmQ3ltOQ0k/n/idkwwmzg22lm/b/ARagavendhar_bucket/o/');

// [ACTION REQUIRED] name of the database that stores photo meta-data (note that this is not the DB identifier of the database instance)
define('DB_NAME', 'photoalbum');
// [ACTION REQUIRED] endpoint/private IP of the MySQL database
define('DB_ENDPOINT', '172.17.3.78');
// [ACTION REQUIRED] administrator username of your database  
define('DB_USERNAME', 'admin');
// [ACTION REQUIRED] administrator password of your database 
define('DB_PWD', 'Oraclecloud@2023');

// [ACTION REQUIRED] name of the DB table that stores photo's meta-data
define('DB_PHOTO_TABLE_NAME', 'photosDB');
// The table above has 5 columns:
// [ACTION REQUIRED] name of the column in the above table that stores photo's titles
define('DB_PHOTO_TITLE_COL_NAME', 'photo_title');
// [ACTION REQUIRED] name of the column in the above table that stores photo's descriptions
define('DB_PHOTO_DESCRIPTION_COL_NAME', 'description');
// [ACTION REQUIRED] name of the column in the above table that stores photo's creation dates
define('DB_PHOTO_CREATIONDATE_COL_NAME', 'creation_date');
// [ACTION REQUIRED] name of the column in the above table that stores photo's keywords
define('DB_PHOTO_KEYWORDS_COL_NAME', 'keywords');
// [ACTION REQUIRED] name of the column in the above table that stores photo's links in S3 
define('DB_PHOTO_S3REFERENCE_COL_NAME', 'object_reference');
?>