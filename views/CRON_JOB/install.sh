redis-cli HSET M:CRON_JOB:Forms 0 "yes:yes:ID:id"
redis-cli HSET M:CRON_JOB:Forms 1 "no:yes:CRON-EXPR:cron"
redis-cli HSET M:CRON_JOB:Forms 2 "no:yes:Script name:script"
redis-cli HSET M:CRON_JOB:Forms 3 "no:yes:Params:argv"
redis-cli HSET M:CRON_JOB:Forms 4 "no:yes:Status:status"
redis-cli HSET M:CRON_JOB:Forms 5 "no:yes:Description:desc"
redis-cli HSET M:CRON_JOB:Button 0 "Red:Start:CRON_JOB_start:#id?user,password,interface"
redis-cli HSET M:CRON_JOB:Button 1 "Green:Stop:CRON_JOB_stop:"
redis-cli RPUSH Shaker:module:list CRON_JOB