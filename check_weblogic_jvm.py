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
# jvm报警百分比 
jvm_warning_percent = int(wlst_str[5])

# jvm严重报警百分比 
jvm_critical_percent =int(wlst_str[6])

def monitor_jvm_heap_size_of_server(server_group):
    printstr=''
    print_stat=''
    ok_wlststr=''
    warn_wlststr=''
    exp_wlststr=''
    critical_wlststr=''
    domainConfig()
    serverNames = cmo.getServers()
    domainRuntime()
    for server in serverNames:
        svr_name=server.getName()
        for s in server_group.split(','):
            if svr_name == s:
               try:
                  cd('/ServerRuntimes/' + svr_name + '/JVMRuntime/' + svr_name)
                  used_percent = 100 - cmo.getHeapFreePercent()
                  # 获取jvm堆空闲比例
                  #jvm max 大小
                  #max_heap_size=round(round(cmo.getHeapSizeMax(),1)/1024/1024/1024)
                  #JVM当前大小
                  curr_heap_size=round(round(cmo.getHeapSizeCurrent(),1)/1024/1024/1024)
                  print_stat += ' Cheap(%s)=%d Uheap(%s)=%d ' % (svr_name,curr_heap_size,svr_name,used_percent)
                  if used_percent >= jvm_critical_percent:
                     critical_wlststr+='[%s]heapsize:%sGB,heapusage:%s%%,' % (svr_name,curr_heap_size,str(used_percent))
                  elif used_percent >= jvm_warning_percent:
                     warn_wlststr+='[%s]heapsize:%sGB,heapusage:%s%%,' % (svr_name,curr_heap_size,str(used_percent))
                  else:
                     ok_wlststr+='[%s]Heapsize:%sGB,heapusage:%s%%,' % (svr_name,curr_heap_size,str(used_percent))
               except WLSTException,e:
                     exp_wlststr+="[%s]State:shutdown," % svr_name
    if exp_wlststr=='':
       if critical_wlststr!='':
          printstr="CRITICAL,Weblogic JVM:"+critical_wlststr.strip(',')+' | '+print_stat
       elif warn_wlststr!='':
          printstr="WARNNING,Weblogic JVM:"+warn_wlststr.strip(',')+' | '+print_stat
       else:
          printstr="OK,Weblogic JVM:"+ok_wlststr.strip(',')+' | '+print_stat
    elif int(exp_wlststr.count("shutdown"))== len(server_group.split(',')):
         printstr="WARNNING,Weblogic State:"+ exp_wlststr.strip(',')+"please check Weblogic State."
    else:
        if  critical_wlststr!='':
            printstr="WARNNING,Weblogic JVM:"+critical_wlststr+","+exp_wlststr
        elif  warn_wlststr!='':
            printstr="WARNNING,Weblogic JVM:"+warn_wlststr+","+exp_wlststr 
        else:
            printstr="WARNNING,Weblogic JVM:"+ok_wlststr+","+exp_wlststr
    return printstr

#def monitor_jvm_heap_size_of_cluster():
#    domainConfig()
#    serverNames = cmo.getServers()
#    domainRuntime()
#    for server in serverNames:
#        print 'INFO: Now checking ' + server.getName()
#        try:
#            cd('/ServerRuntimes/' + server.getName() + '/JVMRuntime/' + server.getName())
#        except WLSTException,e:
#            # 通常意味着尚未启动服务器，忽略即可
#            pass
#        # 获取jvm堆空闲比例
#        used_percent = 100 - cmo.getHeapFreePercent()
#        if used_percent >= jvm_warning_percent:
#            print 'WARNING: Jvm heap usage ' + str(used_percent) + '% exceeds ' + str(jvm_warning_percent) + '%'
#        else:
#            print 'INFO: Jvm heap usage: ' + str(used_percent)

connect(adminserver_username, adminserver_password, 't3://' + adminserver_ip + ':' + str(adminserver_port)) 
print monitor_jvm_heap_size_of_server(server_group)
# monitor_jvm_heap_size_of_cluster()
disconnect()
exit()
