import sys

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
server_group = wlst_str[4]

#应用名称
appname = wlst_str[5]

def monitor_state_of_server(server_group):
    printstr=''
    print_stat=''
    ok_wlststr=''
    warn_wlststr=''
    critical_wlststr=''
    domainRuntime()
    cd('ServerRuntimes')
    Servers=domainRuntimeService.getServerRuntimes()
    #Servers=cmo.getServer()
    for s in server_group.split(','):
        if s not in str(Servers):
           critical_wlststr+='%s(NOTRUNNING,UNKNOWN),' % s
           print_stat+=' State(%s)=0 Health(%s)=0 ' % (s,s)
        else:
           for server in Servers:
               servername=server.getName()
               s_state=server.getState()
               s_health=server.getHealthState().getState()
               if servername==s:
                  if s_state=="RUNNING" and s_health==0:
                     ok_wlststr+='%s(RUNNING,OK),' % s
                     print_stat+=' State(%s)=1 Health(%s)=1 ' % (s,s)
                  elif s_state=="RUNNING" and s_health!=0:
                     critical_wlststr+='%s(RUNNING,UNKNOWN),' % s
                     print_stat+=' State(%s)=1 Health(%s)=0 ' % (s,s)
                  else:
                     critical_wlststr+='%s(%s,UNKNOWN),' % (s,s_state)
                     print_stat+=' State(%s)=0 Health(%s)=0 ' % (s,s)
    if critical_wlststr!='':
       printstr="CRITICAL,Weblogic "+appname +" State:"+critical_wlststr.strip(',')+',please check.|'+print_stat
    else:
       printstr="OK,Weblogic "+appname+" State:"+ok_wlststr.strip(',')+'.|'+print_stat
    return printstr


connect(adminserver_username, adminserver_password, 't3://' + adminserver_ip + ':' + str(adminserver_port)) 
print monitor_state_of_server(server_group)
disconnect()
exit()
