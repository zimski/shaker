redis-cli HSET M:Manage_DHCP:Select 0 "yes:Area:area:ircad,ihu"
redis-cli HSET M:Manage_DHCP:Button 0 "Red:Set:undefined:ip?vvvvv,hoho"
redis-cli HSET M:Manage_DHCP:Button 1 "Green:Remove:undefined:"
redis-cli HSET M:Manage_DHCP:Button 2 "Green:Remove:undefined:"
redis-cli HSET M:Manage_DHCP:Info alias "Manage_DHCP"
redis-cli RPUSH Shaker:module:list Manage_DHCP
redis-cli HSET M:Manage_DHCP:Forms 0 "yes:yes:IP:ip"
redis-cli HSET M:Manage_DHCP:Forms 1 "no:yes:MAC:mac"
redis-cli HSET M:Manage_DHCP:Forms 2 "no:yes:MAChhh:machhh"
