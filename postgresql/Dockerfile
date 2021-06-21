FROM postgres:12-alpine
COPY ./postgresql.conf /etc/postgresql.conf
# Если необходимо будет включить поддержку удаленного подключения к MYSQL
#RUN apk add --update make git gcc libc-dev mariadb-dev clang llvm8 llvm
#RUN mkdir /mysql_fdw
#WORKDIR /mysql_fdw
#RUN git clone https://github.com/EnterpriseDB/mysql_fdw.git ./
#RUN sed -i 's/| RTLD_DEEPBIND//g' mysql_fdw.c
#RUN make USE_PGXS=1
#RUN make USE_PGXS=1 install

# Если нам потребуется русская локаль
#ENV MUSL_LOCPATH=/usr/local/share/i18n/locales/musl
#RUN apk add --update cmake musl-dev gettext-dev libintl
#RUN cd /tmp && git clone https://github.com/rilian-la-te/musl-locales.git
#RUN cd /tmp/musl-locales && cmake . && make && make install

#ENV LANG=ru_RU.UTF-8 \
#    LANGUAGE=ru_RU.UTF-8
