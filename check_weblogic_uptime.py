import sys
import datetime


argv=sys.argv
wlst_str=argv[1].split('|')

# 管理服务器控控制台用户名
adminserver_username =wlst_str[0]
# 管理服务器控制台密码
adminserver_password =wlst_str[1]
# 管理服务器ip
adminserver_ip =wlst_str[2]
# 管理服务器端口
adminserver_port = wlst_str[3]
# server名称组
server_groups = wlst_str[4]

# 应用部署名称
appname = wlst_str[5]
# 告警阀值
time_periodvalue = wlst_str[6]


def monitor_uptime_of_server(server_groups):
    printstr=''
    ok_wlststr=''
    critical_wlststr=''
    exp_wlststr=''
    domainRuntime()
    for s in server_groups.split(','):
        try:
           cd("ServerRuntimes/"+s)
           timestamp=round(get("ActivationTime")/1000)
           wls_time=datetime.datetime.fromtimestamp(timestamp)
           now_spanvalue=datetime.datetime.now()-datetime.timedelta(seconds=long(time_periodvalue))
           if wls_time>=now_spanvalue:
              critical_wlststr+="[%s]Starttime:%s," % (s,wls_time)
           else:
              ok_wlststr+="[%s]Starttime:%s," % (s,wls_time)
        except WLSTException,e:
              exp_wlststr+="[%s]State:shutdown," % s
    if exp_wlststr=='':
       if critical_wlststr!='':
          printstr="CRITICAL, Weblogic Server "+appname+" RebootTime:"+critical_wlststr.strip(',')+",please check."
       else:
          printstr="OK,Weblogic Server "+appname+" RebootTime:"+ok_wlststr.strip(',')
    elif int(exp_wlststr.count("shutdown"))== len(server_groups.split(',')):
         printstr="WARNNING,Weblogic "+appname +" State:"+ exp_wlststr.strip(',')+",please check Weblogic State."
    else:
         if  critical_wlststr!='':
             printstr="WARNNING,Weblogic "+appname+" RebootTime:"+critical_wlststr+exp_wlststr
         else:
             printstr="WARNNING,Weblogic "+appname+" RebootTime:"+ok_wlststr+exp_wlststr
    return printstr


connect(adminserver_username, adminserver_password, 't3://' + adminserver_ip + ':' + str(adminserver_port)) 
print monitor_uptime_of_server(server_groups)
disconnect()
exit()



