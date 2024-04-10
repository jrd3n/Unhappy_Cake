FROM ubuntu:jammy

# Install system dependencies
RUN apt update -y && apt upgrade -y && \
    apt install -y python3-pip nginx openssl && \
    rm -rf /var/lib/apt/lists/*

# # Setup SSL
# RUN mkdir -p /etc/ssl/nginx && \
#     openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#     -keyout /etc/ssl/nginx/nginx-selfsigned.key \
#     -out /etc/ssl/nginx/nginx-selfsigned.crt \
#     -subj "/C=UK/ST=Hemel/L=Hemel/O=Happy Cake Factory/OU=IT Department/CN=happycakefactory.bsi/emailAddress=admin@happycakefactory.bsi"

# Copy application code and Nginx config
COPY . /unhappy_cake
COPY nginx.conf /etc/nginx/sites-available/unhappy_cake.conf

# Link Nginx config and remove default
RUN ln -s /etc/nginx/sites-available/unhappy_cake.conf /etc/nginx/sites-enabled/ && \
    rm /etc/nginx/sites-enabled/default

# Install Python dependencies
WORKDIR /unhappy_cake
RUN python3 -m pip install -r requirements.txt

# Expose ports
EXPOSE 80 443 5000

CMD ["sh", "start.sh"]