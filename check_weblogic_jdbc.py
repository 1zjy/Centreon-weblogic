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
#JDBC名称
jdbcname = wlst_str[4]
# 活动链接数严重告警百分比
critical_activevalue = int(wlst_str[5])

# 等待链接数严重告警值
critical_waitvalue = int(wlst_str[6])


###
#JDBC名称：jdbcName
#JDBC最大容量：MaximumCapacity
#当前活动连接计数：ActiveConnectionsCurrentCount     最大容量80%
#等待连接当前计数：WaitingForConnectionCurrentCount  10
#连接泄露数量：LeakedConnectionCount   >0

def monitor_state_of_jdbc(jdbcname):
    printstr=''
    print_stat=''
    ok_wlststr=''
    critical_wlststr=''
    domainConfig()
    try:
       cd("JDBCSystemResources/"+jdbcname+"/JDBCResource/"+jdbcname+"/JDBCConnectionPoolParams/"+jdbcname)
       maxcap80=get('MaxCapacity')*critical_activevalue*0.01
    except WLSTException,e:
        printstr="CRITICAL,please check inputjdbc name[%s]" % jdbcname
        return printstr
    domainRuntime()
    cd('ServerRuntimes')
    Servers=domainRuntimeService.getServerRuntimes()
    for s in Servers:
        svrname=s.getName()
        jdbcRuntime=s.getJDBCServiceRuntime()
        datasources=jdbcRuntime.getJDBCDataSourceRuntimeMBeans()
        for ds in datasources:
            dsname=ds.getName()
            if dsname==jdbcname:
               dsaccc=round(ds.getActiveConnectionsCurrentCount(),0)
               dswfccc=round(ds.getWaitingForConnectionCurrentCount(),0)
               dslcc=round(ds.getLeakedConnectionCount(),0)
               # print s.getName()+"|"+dsname+"|"+str(dsaccc)+"|"+str(dswfccc)+"|"+str(dslcc)+"|"+str(maxcapacity)
               print_stat+=' ACCC(%s)=%d WFCCC(%s)=%d LCC(%s)=%d ' % (svrname,dsaccc,svrname,dswfccc,svrname,dslcc)
               if dsaccc >= maxcap80 or dswfccc >= critical_waitvalue or dslcc > 0:
                  critical_wlststr+="[%s](ACCC=%d,WFCCC=%d,LCC=%d):" % (svrname,dsaccc,dswfccc,dslcc) 
               else:
                  ok_wlststr+="[%s](ACCC=%d,WFCCC=%d,LCC=%d):" % (svrname,dsaccc,dswfccc,dslcc) 
                  #ok_wlststr+="[%s]当前活动链接数:%s,等待链接当前计数:%s,连接泄露数:%s" % (svrname,str(dsaccc),str(dswfccc),str(dslcc)) 
    if critical_wlststr!='':
       printstr="CRITICAL,"+critical_wlststr.strip(',')+'|'+print_stat
    else:
       printstr="OK,"+ok_wlststr.strip(',')+'|'+print_stat
    return printstr


connect(adminserver_username, adminserver_password, 't3://' + adminserver_ip + ':' + str(adminserver_port)) 
print monitor_state_of_jdbc(jdbcname)
disconnect()
exit()

