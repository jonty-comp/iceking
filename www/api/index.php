<?php

require_once('../config.php');
require_once('../includes/APIController.php');
require_once('../includes/DataModels.php');

$mode = 'debug'; // 'debug' or 'production'
$server = new RestServer($mode);
// $server->refreshCache();

$server->addClass('APIController');

$server->handle();

?>