# Redo the task #0 but by using Puppet

exec { 'update_apt':
  command => '/usr/bin/env apt -y update',
  path    => '/usr/bin:/bin',
}
package { 'nginx':
  ensure => 'installed',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  content => '<!DOCTYPE html>
<html>
<head></head>
<body>Holberton School</body>
</html>',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
}

exec { 'change_ownership':
  command     => 'chown -R ubuntu:ubuntu /data/web_static',
  path        => '/usr/bin:/bin',
  refreshonly => true,
}

file { '/etc/nginx/sites-available/web_static':
  content => "server {
    listen 80;
    server_name xtechitsupport.tech;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.nginx-debian.html;
    }

    location / {
        add_header X-Served-By \$hostname;
    }
  }",
}

file { '/etc/nginx/sites-enabled/web_static':
  ensure => 'link',
  target => '/etc/nginx/sites-available/web_static',
  notify => Service['nginx'],
}

file { '/etc/nginx/sites-enabled/default':
  ensure => 'absent',
  notify => Service['nginx'],
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Package['nginx'],
}
