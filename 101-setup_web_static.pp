# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Create or recreate symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Restart Nginx
service { 'nginx':
  ensure => 'running',
  enable => true,
}
