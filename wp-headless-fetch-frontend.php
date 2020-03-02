<?php
/**
 * Plugin Name: WP headless fetch frontend
 * Plugin URI: <https://github.com/deltary/wp-headless-fetch-frontend>
 * Description: Fetch new frontend from GitHub artifacts on save_post
 * Version: 1.0
 * Author: Konsta Purtsi
 * Author URI: https://github.com/kovipu
 */

add_action( 'save_post', function () { exec("python3 fetch.py"); } );