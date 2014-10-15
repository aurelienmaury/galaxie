#! /bin/bash
VERSION=1.0
DNSROOTS_GLOBAL=/etc/dnsroots.global
DNSROOTS_GLOBAL_OLD=$DNSROOTS_GLOBAL.old
DNSCACHE_SERVICE_DIR=/etc/service/dnscache
echo "Creat a backup of $DNSROOTS_GLOBAL in $DNSROOTS_GLOBAL_OLD"
mv $DNSROOTS_GLOBAL $DNSROOTS_GLOBAL_OLD
echo "Make the root servers request with you actual DNS server /etc/resolv.conf"
dnsip `dnsqr ns . | awk '/answer:/ { print $5; }' |sort`  > $DNSROOTS_GLOBAL
echo "Copy $DNSROOTS_GLOBAL to $DNSCACHE_SERVICE_DIR/root/servers/@"
cp $DNSROOTS_GLOBAL $DNSCACHE_SERVICE_DIR/root/servers/@
echo "Restart Dnscache service"
svc -du $DNSCACHE_SERVICE_DIR
sleep 1
svstat $DNSCACHE_SERVICE_DIR
echo "Here the diff"
diff $DNSROOTS_GLOBAL $DNSROOTS_GLOBAL_OLD
echo "All operations finish"
