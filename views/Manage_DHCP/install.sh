redis-cli HSET M:Manage_DHCP:Forms yes:yes:IP:ip
redis-cli HSET M:Manage_DHCP:Forms no:yes:MAC:mac
redis-cli HSET M:Manage_DHCP:Button Red:Set:undefined:
redis-cli HSET M:Manage_DHCP:Button Green:Remove:undefined:
redis-cli RPUSH Shaker:module:list Manage_DHCP
