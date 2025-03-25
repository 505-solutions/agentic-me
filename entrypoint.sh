#!/bin/sh  
set -e  

# Start the proxy server in the background  
./proxy-server &  

# Start supervisord in the foreground  
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf  