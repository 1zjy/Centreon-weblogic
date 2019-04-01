#!/bin/sh
xz=$1
wlst_str=$2
wlst_jb='/weblogic/middleware/wlserver_10.3/common/bin/wlst.sh'
cd /usr/lib/nagios/plugins/mycheck_weblogic
case $xz in
     state)
     mmstr=`$wlst_jb check_weblogic_state.py $wlst_str|tail -6|head -1`
     ;;
     thread)
     mmstr=`$wlst_jb check_weblogic_thread.py $wlst_str|tail -1`
     ;;
     jvm)
     mmstr=`$wlst_jb check_weblogic_jvm.py $wlst_str|tail -6|head -1`
     ;;
     jdbc)
     mmstr=`$wlst_jb check_weblogic_jdbc.py $wlst_str|tail -6|head -1`
     ;;
     uptime)
     mmstr=`$wlst_jb check_weblogic_uptime.py $wlst_str|tail -6|head -1`
     ;;
     *)
     echo "usage:[thread|jvm|jdbc|uptime]"
     ;;
esac
echo $mmstr
if [ `echo $mmstr|grep "OK"|wc -l` -eq 1 ];then
   exit 0
elif [ `echo $mmstr|grep "WARNNING"|wc -l` -eq  1 ];then
   exit 1
else
   exit 2
fi
