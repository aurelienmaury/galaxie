#! /bin/bash
echo "==================================================================="
echo "Met ca mon coco"
echo "==================================================================="
echo "    Country Name (2 letter code) [AU]:FR"
echo "    State or Province Name (full name) [Some-State]:Ile-de-France"
echo "    Locality Name (eg, city) []:Guitrancourt"
echo "    Organization Name (eg, company) [GX Networks Ltd]:Galaxie"
echo "    Organizational Unit Name (eg, section) []:Mail Server"
echo "    Common Name (eg, YOUR name) []:mail.galaxie.eu.org"
echo "    Email Address []:"
echo "    A challenge password []:"
echo "    An optional company name []:"
echo "==================================================================="
cd /var/qmail/control
openssl genrsa -des3 -out servercert.key.enc 2048
openssl rsa -in servercert.key.enc -out servercert.key
openssl req -new -key servercert.key -out servercert.csr
openssl req -days 365 -x509 -key servercert.key -in servercert.csr > servercert.crt
cat servercert.key servercert.crt > /var/qmail/control/mail.galaxie.eu.org.key-cert.pem
qmailctl restart
