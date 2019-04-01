# Centreon-weblogic
通过oracle官方推荐的wlst监控weblogic中间性能参数,目前由服务状态、jvm、线程、jdbc连接池、运行时间等监控

脚本介绍：
采用shell方式编写运行主脚本check_weblogic.sh，其他jvm、thread、state、uptime、jdbc为选择的分支脚本（python）;

标准用法：
state:
./check_weblogic.sh state '[管理控制台用户]|[控制台密码]|[管理节点IP]|[管理节点端口]|[server1,server2,…]|业务名称'


