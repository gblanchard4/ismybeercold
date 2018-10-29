FROM arm32v7/nginx:1.15.5

# Nginx port
EXPOSE 80
# Remove the default config file that
# /etc/nginx/nginx.conf includes
RUN rm /etc/nginx/conf.d/default.conf
# We copy the requirements file in order to install
# Python dependencies
COPY app.conf /etc/nginx/conf.d
