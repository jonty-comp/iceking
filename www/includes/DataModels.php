<?php

require_once('DB.php');
DB::connect();

class Referer {
	
	public $id;
	public $url;

}

class Referers {

	public static function get_by_id($id) { return DB::select("* FROM referers WHERE id = :id", $id, "Referer", false); }
	public static function get_by_url($url) { return DB::select("* FROM referers WHERE id = :url", $url, "Referer", false); }

}

class MountPoint {
	
	public $id;
	public $mount_point;
	public $bitrate;
	public $date_added;
	public $date_retired;
	public $count;
}

class MountPoints {

	public static function get_by_id($id) { return DB::select("* FROM mount_points WHERE id = :id", $id, "MountPoint", false); }
	public static function get_by_mount_point($mount_point) { return DB::select("* FROM mount_points WHERE mount_point = :mount_point", $mount_point, "MountPoint", false); }
	public static function get_by_bitrate($bitrate) { return DB::select("* FROM mount_points WHERE bitrate = :bitrate", $bitrate, "MountPoint", true); }

	public static function get_counted() { return DB::select("* FROM mount_points WHERE count = TRUE", NULL, "MountPoint", true); }

}

class UserAgent {
	
	public $id;
	public $ua_string;

}

class UserAgents {

	public static function get_by_id($id) { return DB::select("* FROM user_agents WHERE id = :id", $id, "UserAgent", false); }
	public static function get_by_ua_string($ua_string) { return DB::select("* FROM user_agents WHERE ua_string = :ua_string", $ua_string, "UserAgent", false); }

}

class LogItem {

	public $id;
	public $ip;
	public $timestamp;
	public $mount_point_id;
	public $user_agent_id;
	public $referer_id;
	public $bytes;

	public $mount_point;
	public $user_agent;
	public $referer;

	public function __construct() {
		$this->mount_point = MountPoints::get_by_id($this->mount_point_id);
		$this->user_agent = UserAgents::get_by_id($this->user_agent_id);
		$this->referer = Referers::get_by_id($this->referer_id); 
	}

}

class LogItems {

	public static function get_by_id($id) { return DB::select("* FROM log WHERE id = :id", $id, "LogItem", false); }

}

?>