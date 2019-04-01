# Centreon-weblogic
通过oracle官方推荐的wlst监控weblogic中间性能参数,目前由服务状态、jvm、线程、jdbc连接池、运行时间等监控

脚本介绍：
采用shell方式编写运行主脚本check_weblogic.sh，其他jvm、thread、state、uptime、jdbc为选择的分支脚本（python）;

脚本用法说明：

1、服务状态【state格式】

./check_weblogic.sh state '[管理控制台用户]|[控制台密码]|[管理节点IP]|[管理节点端口]|[server1,server2,…]|业务名称'

2、JVM使用率【jvm格式】

./check_weblogic.sh jvm '[管理控制台用户]|[控制台密码]|[管理节点IP]|[管理节点端口]|[server1,server2,…]|警告阀值|严重告警阀值'

3、线程状态及数量【thread格式】

./check_weblogic.sh thread '[管理控制台用户]|[控制台密码]|[管理节点IP]|[管理节点端口]|[server1,server2,…]|业务名称|Queue严重告警阀值|独占线程严重告警阀值'

4、运行时间【uptime格式】

./check_weblogic.sh uptime '[管理控制台用户]|[控制台密码]|[管理节点IP]|[管理节点端口]|[server1,server2,…]|业务名称|告警阀值'

5、jdbc健康状态【jdbc格式】

./check_weblogic.sh  jdbc '[管理控制台用户]|[控制台密码]|[管理节点IP]|[管理节点端口]|JDBC名称|活动连接数告警阀值|等待连接数严重告警阀值'
