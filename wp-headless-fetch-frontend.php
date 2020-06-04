<?php
/**
 * Plugin Name: WP headless fetch frontend
 * Plugin URI: <https://github.com/deltary/wp-headless-fetch-frontend>
 * Description: Fetch new frontend from GitHub artifacts on save_post
 * Version: 1.0
 * Author: Konsta Purtsi
 * Author URI: https://github.com/kovipu
 */


add_action( 'save_post', 'send_repository_dispatch' );

function send_repository_dispatch($post_id) {

  if (wp_is_post_revision($post_id)) {
    return;
  }

  $ACCESS_TOKEN = "637b21ebb444274335765991ea218d8601e98a70";

  $response = wp_remote_post('https://api.github.com/repos/deltary/website/dispatches/', array(
      'method'    => 'POST',
      'headers'   => array(
        'User-Agent'      => 'https://delta.utu.fi',
        'Authorization'   => 'token ' . $ACCESS_TOKEN,
        'Accept'          => 'application/vnd.github.everest-preview+json',
        'Content-Type'    => 'application/json'
      ),
      'body'      => array(
        'event_type'      => 'repository_dispatch',
      ),
    )
  );

  if (is_wp_error($response)) {
    error_log("Failed");
    error_log($response->get_error_message());
  } else {
    error_log("Success");
    error_log(print_r($response, true));
  }
}