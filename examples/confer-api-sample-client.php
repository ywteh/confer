<?php

/*
 * @author: Anant Bhardwaj
 * @date: Jan 26, 2014
 * 
 * A sample of how to use confer APIs
 */

/**
 * Step 1: Create your app at http://confer.csail.mit.edu/developer/apps (click on the button 'Create a New App')
 * Step 2: You can get your app_token at http://confer.csail.mit.edu/developer/apps at any time
 * Step 3: Redirect your first-time users to http://confer.csail.mit.edu/developer/allow_access?app_id=<your app id> 
 *         so that they can allow your app to access their data.
 */
$params = array(
    'login_id' => 'anantb@csail.mit.edu',
    'conf_id' => 'cscw2014',
    'app_id' => 'test_app',
    'app_token' => '68b6fdc3285886ac0f9f3d01bc86a9ad06867777');

$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($params),
    ),
);

$context  = stream_context_create($options);

// get likes for a confer login_id
$likes = file_get_contents('http://confer.csail.mit.edu/api/likes', false, $context);
var_dump($likes);

/*
 * If you get msg = "ACCESS_DENIED" in the response, it means user has revoked the access to your app. 
 * You can redirect the user to http://confer.csail.mit.edu/developer/allow_access?app_id=test_app to
 * grant the access
 */

// get similar_people for a confer login_id
$similar_people = file_get_contents('http://confer.csail.mit.edu/api/similar_people', false, $context);
var_dump($similar_people);

?>
