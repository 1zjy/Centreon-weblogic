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

# department名称
deployname = wlst_str[5]
# 活动线程上限，超出此上限警告值%
#critical_executethread_limit = int(wlst_str[6])
# 线程数上限，超出此上限严重告警
critical_queue_limit = int(wlst_str[6])
# stuck 线程数上限，超出此上限严重告警
critical_stuck_limit = int(wlst_str[7])

def monitor_thread_of_server(server_group):
    ok_wlststr=''
    warn_wlststr=''
    critical_wlststr=''
    exp_wlststr=''
    print_stat=''
    # 阻止print的内容输出到屏幕
    redirect('/dev/null', 'false')
    domainRuntime()
    for server in server_group.split(','):
        try:
           cd("/ServerRuntimes/"+server+"/ThreadPoolRuntime/ThreadPoolRuntime")
           health_state=str(get("HealthState")).split(',')[1].split(':')[1]
           Execute=get("ExecuteThreadTotalCount")
           Stuck=get("HoggingThreadCount")
           Queue=get("QueueLength")
           Through=get("Throughput")
           print_stat += ' Execute(%s)=%d Stuck(%s)=%d Queue(%s)=%d Through(%s)=%d ' % (server,Execute,server,Stuck,server,Queue,server,Through)
           if  Stuck >= critical_stuck_limit or Queue >= critical_queue_limit or health_state!='HEALTH_OK':
               critical_wlststr+="[%s]State:%s,Execute:%d,Stuck:%d,Queue:%d,Throughout:%d;" % (server,health_state,Execute,Stuck,Queue,Through)
           else:
               ok_wlststr+="[%s]State:%s,Execute:%d,Stuck:%d,Queue:%d,Throughout:%d;" % (server,health_state,Execute,Stuck,Queue,Through)
        except WLSTException,e:
             exp_wlststr+="[%s]State:shutdown," % server 
    if exp_wlststr=='':
       if critical_wlststr!='':
          printstr="CRITICAL,Weblogic "+deployname+" Thread:"+critical_wlststr.strip(';')+' |'+print_stat.strip('|')
       else:
          printstr="OK,Weblogic "+deployname+" Thread:"+ok_wlststr.strip(';')+' |'+print_stat.strip('|')
    elif int(exp_wlststr.count("shutdown"))== len(server_group.split(',')):
         printstr="WARNNING,Weblogic "+deployname +" State:"+ exp_wlststr.strip(',')+",please check Weblogic State."
    else:
        if  critical_wlststr!='':
            printstr="WARNNING,Weblogic "+deployname+" Thread:"+critical_wlststr+","+exp_wlststr
        else:
            printstr="WARNNING,Weblogic "+deployname+" Thread:"+ok_wlststr+","+exp_wlststr

    return printstr



redirect('/dev/null', 'false')
connect(adminserver_username, adminserver_password, 't3://' + adminserver_ip + ':' + str(adminserver_port))
redirect('/dev/null','true')
print monitor_thread_of_server(server_group)
disconnect()
exit()



