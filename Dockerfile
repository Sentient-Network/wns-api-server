FROM centos:6

# Install namecoin
RUN yum -y install wget
RUN cd /etc/yum.repos.d/ && wget http://download.opensuse.org/repositories/home:p_conrad:coins/CentOS_CentOS-6/home:p_conrad:coins.repo
RUN yum -y install namecoin

# Configure namecoind
RUN useradd namecoin
RUN su - namecoin && mkdir /home/namecoin/.namecoin && echo "rpcuser=namecoin_user" >> /home/namecoin/.namecoin/namecoin.conf \
&& echo "rpcpassword=namecoin_password" >> /home/namecoin/.namecoin/namecoin.conf \
&& echo "rpcport=8883" >> /home/namecoin/.namecoin/namecoin.conf
RUN chown -R namecoin:namecoin /home/namecoin/.namecoin

# Install unbound build deps
RUN yum -y install tar openssl-devel python-devel expat-devel
RUN yum -y groupinstall "Development tools"

# Download and build unbound
RUN cd && mkdir unbound && cd unbound && curl -O http://www.unbound.net/downloads/unbound-1.4.22.tar.gz && tar -xvf unbound-1.4.22.tar.gz
RUN cd /root/unbound/unbound-1.4.22 && ./configure --with-pyunbound --with-ssl && make && make install
RUN useradd unbound

# Setup unbound trust anchor for ICANN DNSSEC resolution
RUN unbound-anchor || true

# Download and prepare Netki wns-api-server
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN useradd netki
RUN su - netki -c "git clone https://github.com/netkicorp/wns-api-server.git && echo 'export PYTHONPATH=/home/netki/wns-api-server' >>~/.bashrc"
RUN pip install -r /home/netki/wns-api-server/requirements.txt && pip install gunicorn

# Set namecoind and was-api-server to run
RUN mkdir /var/run/namecoin
RUN chown namecoin:namecoin /var/run/namecoin
RUN mkdir /var/run/wns-api-server
RUN mkdir /var/log/netki
RUN chown netki:netki /var/run/wns-api-server /var/log/netki
RUN cp /home/netki/wns-api-server/etc/init.d/namecoind /etc/init.d/namecoind
RUN chkconfig --add namecoind
RUN cp /home/netki/wns-api-server/etc/init.d/wns-api-server /etc/init.d/wns-api-server
RUN chkconfig --add wns-api-server
RUN echo 'service namecoind start' >>~/.bashrc
RUN echo 'service wns-api-server start' >>~/.bashrc
