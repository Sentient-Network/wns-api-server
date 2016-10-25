# Wallet Name Lookup Server

Netki Open Wallet Name Lookup API Server

# General

The Netki open Wallet Name lookup API server allows you to quickly integrate the Wallet Name standard into your digital
currency platform. Using the Wallet Name Service allows you to avoid difficult Bitcoin, Dogecoin, Litecoin, etc. wallet addresses
and instead use a much more memorable naming scheme that runs on top of DNS using DNSSEC to keep the Chain-of-Trust unbroken.

# Noteworthy Requirements

## Python Modules
- [Flask](http://flask.pocoo.org)
- [wnsresolver](https://github.com/netkicorp/wns-resolver) - Netki Wallet Name Service Resolver
- [bcresolver](https://github.com/netkicorp/blockchain-resolver) - Netki Blockchain DNS Resolver


**NOTE:** WNSResolver and BCResolver both require pyUnbound. While it is not a direct requirement of the Wallet Name Lookup Server, it is required by both of
 the required python modules. Because of this, pyUnbound setup instructions are included below.

# PyUnbound Setup
This version of **wns-resolver** has been tested with Unbound v1.4.22. ([https://unbound.net/downloads/unbound-1.4.22.tar.gz](https://unbound.net/downloads/unbound-1.4.22.tar.gz))

## Install via Repository

**unbound-python** is available via installation by yum and is available in the [EPEL](https://fedoraproject.org/wiki/EPEL) repository.

    [user@host ~]$ yum install -y unbound-python
    
This will install unbound-python, compat-libevent, and unbound-libs packages.

## Manual Download, Installation and Setup 

When ./configure-ing unbound, make sure to use the **--with-pyunbound** flag. This will make pyunbound available after make and make install

Please refer to [https://www.unbound.net/documentation/pyunbound/install.html](https://www.unbound.net/documentation/pyunbound/install.html) for Unbound installation help.

Use the [unbound-anchor](https://www.unbound.net/documentation/unbound-anchor.html) tool to setup the ICANN-supplied DNSSEC Root Trust Anchor.

Make sure to set the **PYTHON_VERSION** environment variable if you have multiple *Python* versions installed, otherwise
the module will be installed for the default system *Python* version.

    [user@host ~]$ export set PYTHON_VERSION=2.7
    [user@host ~]$ wget https://unbound.net/downloads/unbound-1.4.22.tar.gz
    [user@host ~]$ tar -xzf unbound-1.4.22-py.tar.gz
    [user@host ~]$ cd unbound-1.4.22
    [user@host ~]$ ./configure --with-pyunbound
    [user@host ~]$ make
    [user@host ~]$ make install

# Setup

Install requirements in your Python environment

    [user@host ~]$ pip install -r requirements.txt

Edit etc/app.prod.config (default) config file to setup your Namecoin node information as well as log directories, resolv.conf, ICANN DNSSEC Root File and temporary resolver ramdisk location.

**NOTE**: There is a **NETKI_ENV** environment variable that can be set to run different configurations taken from a config file named *app.&lt;env&gt;.config*

To startup the server without a WSGI host, run *python api_server.py* and the server will be started listening on port 5000 by default.

# Docker Container

The most complete Dockerfile here is DockerfileWithoutNamecoinUbuntu. This dockerfile allows for ICANN domains Wallet Name resolution, but not Namecoin (.bit) name resolution. In order to use this correctly, 
you need to supply build-args **SSL_CERT** and **SSL_KEYFILE**. Both of these must be files that are dropped into the **etc/ssl/** directory and are **ADD**'ed into the Docker container during build. 
The container exposes ports **80** and **443**, with port **80** performing an immediate _redirect_ to the HTTPS URL.

# Use

The server responds to API requests in the following format:

**http://example.com/api/wallet_lookup/&lt;wallet_name&gt;/&lt;currency&gt;**

For example, please try [https://pubapi.netki.com/api/wallet_lookup/&lt;wallet_name&gt;/&lt;currency&gt;](https://pubapi.netki.com/api/wallet_lookup/&lt;wallet_name&gt;/&lt;currency&gt;) to see how this works.
 

