FROM nginx:1.13

# Add start script
ADD ./services/webserver/config/start.sh /
RUN chmod +x start.sh

# Add nginx config file
ADD ./services/webserver/config/nginx.tmpl /

# # ADD SSL cert to location specified in nginx.conf
# ADD ./services/webserver/config/*.crt /etc/ssl/certs/
# ADD ./services/webserver/config/*.key /etc/ssl/private/

EXPOSE 80 443

# Execute start script
CMD ["./start.sh"]
