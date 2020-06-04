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

  if (wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
    return;
  }

  $ACCESS_TOKEN = GITHUB_ACCESS_TOKEN;

  $response = wp_remote_post('https://api.github.com/repos/deltary/website/dispatches', array(
      'method'    => 'POST',
      'headers'   => array(
        'User-Agent'      => 'https://delta.utu.fi',
        'Authorization'   => 'token ' . $ACCESS_TOKEN,
        'Accept'          => 'application/vnd.github.everest-preview+json',
        'Content-Type'    => 'application/json'
      ),
      'body'      => json_encode(array(
        'event_type'      => 'save_post',
      )),
    )
  );

  if (is_wp_error($response)) {
    error_log("Failed to dispatch github action");
    error_log($response->get_error_message());
  } 
}

add_action('wp_dashboard_setup', 'my_custom_dashboard_widgets');
  
function my_custom_dashboard_widgets() {
  global $wp_meta_boxes;
  wp_add_dashboard_widget('custom_dashboard_help');
}
 
function custom_dashboard_help() {
  echo '<h1>Github status</h1><img src="https://github.com/deltary/website/workflows/Build%20and%20deploy%20to%20production/badge.svg">';
}
