redis-cli HSET M:Manage_vm:Forms yes:yes:ip:ip
redis-cli HSET M:Manage_vm:Forms no:yes:mac:mac
redis-cli HSET M:Manage_vm:Forms no:yes:hostname:host
redis-cli HSET M:Manage_vm:Forms no:yes:Role:role
redis-cli HSET M:Manage_vm:Forms no:yes:Gateway:gateway
redis-cli HSET M:Manage_vm:Forms no:yes:Dns:dns
redis-cli HSET M:Manage_vm:Forms no:no:Root password:pass
redis-cli HSET M:Manage_vm:Button Blue:Start:Manage_vm_start_vm:#ip
redis-cli HSET M:Manage_vm:Button Red:refresh:refreshOO:
redis-cli HSET M:Manage_vm:Button Red:Stop:Down:#ip
redis-cli RPUSH Shaker:module:list Manage_vm
