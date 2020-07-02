server {
        listen 80;
        listen [::]:80;

        root /var/www/remote.nandi.io/html;
        index index.html index.htm index.nginx-debian.html;
        auth_basic "Administrator Login";
        auth_basic_user_file /var/www/remote.nandi.io/.htpasswd;

        server_name remote.nandi.io;

        location / {
                try_files $uri $uri/ =404;
        }
}
