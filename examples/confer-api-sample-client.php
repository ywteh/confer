<?php

/**
 * @author: Anant Bhardwaj
 * @date: Jan 26, 2014
 * 
 * A sample of how to use confer APIs
 */

$params = array(
    'login_id' => 'anantb@csail.mit.edu',
    'conf_id' => 'cscw2014',
    'app_id' => 'common_ties',
    'app_token' => 'xxx');

$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($params),
    ),
);

$context  = stream_context_create($options);

$likes = file_get_contents('http://confer.csail.mit.edu/api/likes', false, $context);
var_dump($likes);

$similar_people = file_get_contents('http://confer.csail.mit.edu/api/similar_people', false, $context);
var_dump($similar_people);

?>
