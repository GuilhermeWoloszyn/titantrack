FROM kong:latest

COPY kong.yml /usr/local/kong/kong.yml

EXPOSE 8000 8443

ENTRYPOINT ["/usr/local/bin/kong", "reload"]