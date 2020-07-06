server {
    listen 80;
    server_name api.remote.nandi.io;

location / {
  include proxy_params;
  proxy_pass http://unix:/var/www/api/app.sock;
    }
}
