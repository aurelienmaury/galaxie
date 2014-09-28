#! /bin/bash

XBMC_USERDATA=".xbmc/userdata"
TEMPLATE_DIR="/home/tuxa/galaxie/templates/openelec"
for HOST in tv1 tv2 tv3 tv4
do
echo "========================================"
echo " $HOST"
echo "========================================"
if ping -c 1 $HOST.galaxie.ici &> /dev/null
then
    #SSH Managment KEY
    ssh $HOST "mkdir -p .ssh"
    echo ""

    echo "Copy id_rsa_$HOST.pub $HOST:.ssh/authorized_keys"
    scp /home/tuxa/.ssh/id_rsa_$HOST.pub $HOST:.ssh/authorized_keys
    echo ""
    #Copy Common Setting
    echo "Copy advancedsettings.xml to $HOST:$XBMC_USERDATA/advancedsettings.xml" 
    scp $TEMPLATE_DIR/advancedsettings.xml $HOST:$XBMC_USERDATA/advancedsettings.xml
    echo ""

    echo "Copy sources.xml to $HOST:$XBMC_USERDATA/sources.xml"
    scp $TEMPLATE_DIR/sources.xml $HOST:$XBMC_USERDATA/sources.xml || echo "Error for $HOST"
    echo ""

    echo "Copy settings.xml to $HOST:$XBMC_USERDATA/addon_data/pvr.hts/settings.xml"
    ssh $HOST "mkdir -p .xbmc/userdata/addon_data/pvr.hts"
    scp $TEMPLATE_DIR/settings.xml $HOST:$XBMC_USERDATA/addon_data/pvr.hts/settings.xml
    echo ""

    #Pubish Video Audio setting 
    if [ $HOST = tv1 ]
    then
        echo "Copy guisettings.xml.1080p to $HOST:$XBMC_USERDATA/guisettings.xml"
        scp $TEMPLATE_DIR/guisettings.xml.1080p $HOST:$XBMC_USERDATA/guisettings.xml
    fi
    if [ $HOST = tv2 ]
    then
        echo "Copy guisettings.xml.720p to $HOST:$XBMC_USERDATA/guisettings.xml"
        scp $TEMPLATE_DIR/guisettings.xml.720p $HOST:$XBMC_USERDATA/guisettings.xml
    fi
    if [ $HOST = tv3 ]
    then
        echo "Copy guisettings.xml.720p to $HOST:$XBMC_USERDATA/guisettings.xml"
        scp $TEMPLATE_DIR/guisettings.xml.720p $HOST:$XBMC_USERDATA/guisettings.xml
    fi
    if [ $HOST = tv4 ]
    then
        echo "Copy guisettings.xml.720p to $HOST:$XBMC_USERDATA/guisettings.xml"
        scp $TEMPLATE_DIR/guisettings.xml.720p $HOST:$XBMC_USERDATA/guisettings.xml
    fi
    echo ""
    
    # Network path for media share
    echo "Copy favourites.xml to $HOST:$XBMC_USERDATA/favourites.xml"
    scp $TEMPLATE_DIR/favourites.xml $HOST:$XBMC_USERDATA/favourites.xml
    echo ""
    
    #Remote special case for tv2
    if [ $HOST = tv2 ]
    then
        echo "Copy lircd.conf to $HOST:/storage/.config/lirc/lircd.conf"
        scp $TEMPLATE_DIR/lircd.conf $HOST:/storage/.config/lircd.conf
        ssh $HOST "echo '#!/bin/sh' > /storage/.config/autostart.sh && chmod +x /storage/.config/autostart.sh && echo '/sbin/rmmod ir_rc5_decoder' >> /storage/.config/autostart.sh"
        echo ""
    fi

    #Add Universal Add on
    echo "Copy metadata.universal-2.6.0.zip to $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip"
    scp $TEMPLATE_DIR/metadata.universal-2.6.0.zip $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip
    ssh $HOST "cd .xbmc/addons/ && rm -rf ./metadata.universal && unzip ./packages/metadata.universal-2.6.0.zip"
    echo "Inject the setting of metadata.universal"
    ssh $HOST "rm -rf .xbmc/userdata/addon_data/metadata.universal"
    ssh $HOST "mkdir .xbmc/userdata/addon_data/metadata.universal"
    scp $TEMPLATE_DIR/metadata.universal.settings.xml $HOST:.xbmc/userdata/addon_data/metadata.universal/settings.xml
    echo ""

    #Add Weater Addon
    echo "Copy metadata.universal-2.6.0.zip to $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip"
    scp $TEMPLATE_DIR/metadata.universal-2.6.0.zip $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip
    ssh $HOST "cd .xbmc/addons/ && rm -rf ./metadata.universal && unzip ./packages/metadata.universal-2.6.0.zip"
    echo "Inject the setting of metadata.universal"
    ssh $HOST "rm -rf .xbmc/userdata/addon_data/metadata.universal"
    ssh $HOST "mkdir .xbmc/userdata/addon_data/metadata.universal"
    scp $TEMPLATE_DIR/metadata.universal.settings.xml $HOST:.xbmc/userdata/addon_data/metadata.universal/settings.xml
    echo ""

    #Add Youtube Addon
    echo "Copy metadata.universal-2.6.0.zip to $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip"
    scp $TEMPLATE_DIR/metadata.universal-2.6.0.zip $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip
    ssh $HOST "cd .xbmc/addons/ && rm -rf ./metadata.universal && unzip ./packages/metadata.universal-2.6.0.zip"
    echo "Inject the setting of metadata.universal"
    ssh $HOST "rm -rf .xbmc/userdata/addon_data/metadata.universal"
    ssh $HOST "mkdir .xbmc/userdata/addon_data/metadata.universal"
    scp $TEMPLATE_DIR/metadata.universal.settings.xml $HOST:.xbmc/userdata/addon_data/metadata.universal/settings.xml
    echo ""

    #Add Radio Addon
    echo "Copy metadata.universal-2.6.0.zip to $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip"
    scp $TEMPLATE_DIR/metadata.universal-2.6.0.zip $HOST:.xbmc/addons/packages/metadata.universal-2.6.0.zip
    ssh $HOST "cd .xbmc/addons/ && rm -rf ./metadata.universal && unzip ./packages/metadata.universal-2.6.0.zip"
    echo "Inject the setting of metadata.universal"
    ssh $HOST "rm -rf .xbmc/userdata/addon_data/metadata.universal"
    ssh $HOST "mkdir .xbmc/userdata/addon_data/metadata.universal"
    scp $TEMPLATE_DIR/metadata.universal.settings.xml $HOST:.xbmc/userdata/addon_data/metadata.universal/settings.xml
    echo ""

   
   #REboot in case the admin need
   #ssh $HOST "reboot"

else
    echo "Abort $HOST cause not a live..."
    echo ""
fi
done
