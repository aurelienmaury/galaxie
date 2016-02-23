Role Name
=========

Qmail-server role have goal to install and configure a s/qmail server from fehcom design.

s/qmail (pronounced skew-mail) is a Mail Transfer Agent (MTA) based on Qmail suited for high-speed and confidential email transport over IPv4 and IPv6 networks.
More informations:
http://fehcom.de/sqmail/sqmail.html

Requirements
------------
it should work on Debian's familly GNU/Linux distribution.
The role install it self requirements

The role use the daemons-tool provide by Debian packages

Features
--------
ucspi-tcp6:
conf-ld - auto 32/64 bit configuration

s/qmail:
conf-ids, conf-group -  edit a value inside defaults/main.yml will automatiquelly make consistant setting.

Role Variables
--------------

A maxium of variables have been set that for permit fine tuning inside host_var or group_var

Here the lists: (You can found it on ./defaults/main.yml too)

we have make our maximum for have explicite variable name, that should minimize the need of details.

Common and path

galaxie_qmail_server_supervise_dir: "/var/lib/supervise"

galaxie_qmail_server_multilog_user: "multilog"

galaxie_qmail_server_multilog_dir: "/var/multilog"

galaxie_qmail_server_qmaild_user: "qmaild"

galaxie_qmail_server_qmaill_user: "qmaill"

galaxie_qmail_server_qmailp_user: "qmailp"

galaxie_qmail_server_qmailq_user: "qmailq"

galaxie_qmail_server_qmailr_user: "qmailr"

galaxie_qmail_server_qmails_user: "qmails"

galaxie_qmail_server_qmail_group: "qmail"

galaxie_qmail_server_nofiles_group: "nofiles"

galaxie_qmail_server_alias_user: "alias"

galaxie_qmail_server_service_name: "qmail"

galaxie_qmail_server_service_send: "qmail-send"

galaxie_qmail_server_service_smtpd: "qmail-smtpd"

galaxie_qmail_server_service_smtpsd: "qmail-smtpsd"

galaxie_qmail_server_service_ip: "{{ ansible_default_ipv4.address }}"

galaxie_qmail_server_source_dir: "/usr/src/qmail"

galaxie_qmail_server_qmail_dir: "/var/qmail"


# qmail-scanner

galaxie_qmail_server_qmail_scanner_user: "clamav"

# simscan
galaxie_qmail_server_simscan_user: "simscan"
galaxie_qmail_server_simscan_group: "simscan"
# Special
galaxie_qmail_server_domain: "galaxie.ici"

galaxie_qmail_server_install_qmailctl: true
galaxie_qmail_server_install_qfixpermissions: true
galaxie_qmail_server_config_send: true
galaxie_qmail_server_config_smtpd: true
galaxie_qmail_server_config_smtpsd: false
galaxie_qmail_server_set_smtproutes: false
galaxie_qmail_server_set_virtualdomains: false
galaxie_qmail_server_config_qmail_scanner: false
galaxie_qmail_server_config_simscan: false

# Control
galaxie_qmail_server_control_me: "{{ ansible_hostname }}.{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_control_defaultdomain: "{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_control_plusdomain: "{{ galaxie_qmail_server_domain }}"

galaxie_qmail_server_control_locals:
  - "localhost"
  - "localhost.localdomain"
  - "{{ ansible_hostname }}"
  - "{{ ansible_hostname }}.{{ galaxie_qmail_server_domain }}"
  - "{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_control_rcpthosts:
  - "{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_control_smtproutes: ""

galaxie_qmail_server_control_virtualdomains: ""

galaxie_qmail_server_control_defaultdelivery: "./Maildir/"
galaxie_qmail_server_control_concurrencyremote: "255"
galaxie_qmail_server_control_concurrencyincoming: "30"
galaxie_qmail_server_control_spfbehavior: "3"
galaxie_qmail_server_control_bouncefrom: "postmaster"
galaxie_qmail_server_control_doublebouncehost: "{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_control_doublebounceto: "postmaster"
galaxie_qmail_server_control_databytes: "8000000"
galaxie_qmail_server_control_timeoutsmtpd: "30"

# cdb
galaxie_qmail_server_cdb_source_repository: "http://cr.yp.to/cdb"
galaxie_qmail_server_cdb_source_name: "cdb-0.75"
galaxie_qmail_server_cdb_source_extension: "tar.gz"
galaxie_qmail_server_cdb_source_url: "{{ galaxie_qmail_server_cdb_source_repository }}/{{ galaxie_qmail_server_cdb_source_name }}.{{ galaxie_qmail_server_cdb_source_extension }}"
galaxie_qmail_server_cdb_source_dir: "{{ galaxie_qmail_server_source_dir }}/cdb-0.75"

# checkpassword http://cr.yp.to/checkpwd/checkpassword-0.90.tar.gz
galaxie_qmail_server_checkpassword_source_repository: "http://cr.yp.to/checkpwd"
galaxie_qmail_server_checkpassword_source_name: "checkpassword-0.90"
galaxie_qmail_server_checkpassword_source_extension: "tar.gz"
galaxie_qmail_server_checkpassword_source_url: "{{ galaxie_qmail_server_checkpassword_source_repository }}/{{ galaxie_qmail_server_checkpassword_source_name }}.{{ galaxie_qmail_server_checkpassword_source_extension }}"
galaxie_qmail_server_checkpassword_source_dir: "{{ galaxie_qmail_server_source_dir }}/checkpassword-0.90"

# ucpi-ssl
galaxie_qmail_server_ucspi_ssl_certificates_dir: "/etc/ssl/certs"
galaxie_qmail_server_ucspi_ssl_dh_parameter_file: "{{ galaxie_qmail_server_ucspi_ssl_certificates_dir }}/dhparam.pem"
galaxie_qmail_server_ucspi_ssl_dh_bits: "2048"
galaxie_qmail_server_ucspi_ssl_source_repository: "http://www.fehcom.de/ipnet/ucspi-ssl"
galaxie_qmail_server_ucspi_ssl_source_name: "ucspi-ssl-0.95b"
galaxie_qmail_server_ucspi_ssl_source_extension: "tgz"
galaxie_qmail_server_ucspi_ssl_source_url: "{{ galaxie_qmail_server_ucspi_ssl_source_repository }}/{{ galaxie_qmail_server_ucspi_ssl_source_name }}.{{ galaxie_qmail_server_ucspi_ssl_source_extension }}"
galaxie_qmail_server_ucspi_ssl_source_dir: "{{ galaxie_qmail_server_source_dir }}/{{ galaxie_qmail_server_ucspi_ssl_source_name }}"
galaxie_qmail_server_ucspi_ssl_special_connard_dir: "{{ galaxie_qmail_server_ucspi_ssl_source_dir }}/host/superscript.com/net/{{ galaxie_qmail_server_ucspi_ssl_source_name }}"
galaxie_qmail_server_ucspi_ssl_conf_dhfile: "{{ galaxie_qmail_server_ucspi_ssl_special_connard_dir }}/src/conf-dhfile"
galaxie_qmail_server_ucspi_ssl_conf_cadir: "{{ galaxie_qmail_server_ucspi_ssl_special_connard_dir }}/src/conf-cadir"
galaxie_qmail_server_ucspi_ssl_binary_list:
  - "https@"
  - "sslcat"
  - "sslclient"
  - "sslconnect"
  - "sslprint"
  - "sslserver"

# certificate
galaxie_qmail_server_openssl_key_gen: false
galaxie_qmail_server_openssl_key_bit: "2048"
galaxie_qmail_server_openssl_key_days: "3650"
galaxie_qmail_server_openssl_cert_C: "FR"
galaxie_qmail_server_openssl_cert_ST: "Ile-de-France"
galaxie_qmail_server_openssl_cert_L: "Paris"
galaxie_qmail_server_openssl_cert_O: "Galaxie"
galaxie_qmail_server_openssl_cert_OU: "IT"
galaxie_qmail_server_openssl_cert_CN: "{{ ansible_hostname }}.{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_openssl_subj: "/C={{ galaxie_qmail_server_openssl_cert_C }}/ST={{ galaxie_qmail_server_openssl_cert_ST }}/L={{ galaxie_qmail_server_openssl_cert_L }}/O={{ galaxie_qmail_server_openssl_cert_O }}/OU={{ galaxie_qmail_server_openssl_cert_OU }}/CN={{ galaxie_qmail_server_openssl_cert_CN }}"
# Alias creation
galaxie_qmail_server_alias_root: "root@{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_alias_postmaster: "root@{{ galaxie_qmail_server_domain }}"
galaxie_qmail_server_alias_mailer_daemon: "root@{{ galaxie_qmail_server_domain }}"

galaxie_qmail_server_alias_list:
  - { name: nofiles, value: qmaild }


Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
