<?php

require_once('RestServer.php');

class APIController {
	/**
	 * Base URL response
	 *
	 * @url GET /
	 */
	public function base() {
		return "Hello";
	}

	/**
	 * Mountpoint information
	 *
	 * @url GET /data/mountpoint/$id
	 */
	public function mountpoint($id) {
		return MountPoints::get_by_id($id);
	}

	/**
	 * Referer information
	 *
	 * @url GET /data/referer/$id
	 */
	public function referer($id) {
		return Referers::get_by_id($id);
	}

	/**
	 * User-Agent information
	 *
	 * @url GET /data/useragent/$id
	 */
	public function user_agent($id) {
		return UserAgents::get_by_id($id);
	}

	/**
	 * Single log item
	 *
	 * @url GET /data/log/$id
	 */
	public function log($id) {
		return LogItems::get_by_id($id);
	}

	/**
	 * Detailed user-agent information
	 * requires PHP's browscap directive to be set
	 *
	 * @url GET /info/useragent/$id
	 */
	public function user_agent_detail($id) {
		$ua = UserAgents::get_by_id($id);
		return @get_browser($ua->ua_string);
	}
}

?>