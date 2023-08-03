# ------------------------------------------------------------------------------
# Install compiler and compile darkhttpd
FROM ubuntu:jammy AS build
ADD darkhttpd /dark
WORKDIR /dark
RUN apt-get update && \
	apt-get install -y build-essential && \
	gcc -Wall -O2 darkhttpd.c -o darkhttpd.exe && \
	strip darkhttpd.exe

# ------------------------------------------------------------------------------
# Pull base image
FROM ubuntu:jammy
MAINTAINER Brett Kuskie <fullaxx@gmail.com>

# ------------------------------------------------------------------------------
# Set environment variables
ENV DEBIAN_FRONTEND noninteractive

# ------------------------------------------------------------------------------
# Install software and clean up
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	  supervisor python3-pip && \
	pip3 install yfinance && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/*

# ------------------------------------------------------------------------------
# Prepare the image
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY gen_html.py /app/
COPY static/* /www/static/
COPY --from=build /dark/darkhttpd.exe /app/

# ------------------------------------------------------------------------------
# Expose ports
EXPOSE 80

# ------------------------------------------------------------------------------
# Define default command
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
# CMD ["ls", "-l", "/app"]
