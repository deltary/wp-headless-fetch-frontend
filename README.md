# wp-headless-fetch-frontend

WP-plugin, joka lähettää github actionin save_post, joka kerta kun wordpressissä päivitetään sivu.

WP:n config filuun wp-config.php pitää lisätä seuraava rivi.
```
define('GITHUB_ACCESS_TOKEN', 'TÄHÄN GITHUBIN ACCESS TOKEN');
```
