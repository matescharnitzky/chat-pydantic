FROM postgres:17-alpine

COPY infra/init.sh /usr/local/bin/init-infra
COPY infra/init.sql /usr/local/share/init-infra.sql
RUN chmod +x /usr/local/bin/init-infra

ENTRYPOINT ["init-infra"]
