redis-cli HSET M:undefined:Forms 0 "yes:yes:ip:ip"
redis-cli HSET M:undefined:Forms 1 "no:yes:mac:mac"
redis-cli HSET M:undefined:Select 0 "yes:gogg:kiki:kaka,fofof,dfdfd,ok"
redis-cli HSET M:undefined:Button 0 "Blue:Start:start_vm:#ip?user,pass"
redis-cli HSET M:undefined:Button 1 "Red:refresh:refreshOO:"
redis-cli HSET M:undefined:Button 2 "Red:Stop:Down:#ip"
redis-cli HSET M:undefined:Info alias "undefined"
redis-cli RPUSH Shaker:module:list undefined
