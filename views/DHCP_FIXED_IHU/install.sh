redis-cli HSET M:DHCP_FIXED_IHU:Forms 0 "yes:yes:IP:ip"
redis-cli HSET M:DHCP_FIXED_IHU:Forms 1 "no:yes:MAC:mac"
redis-cli HSET M:DHCP_FIXED_IHU:Forms 2 "no:yes:hostname:hostname"
redis-cli HSET M:DHCP_FIXED_IHU:Button 0 "Red:Update:DHCP_FIXED_IHU_update:"
redis-cli HSET M:DHCP_FIXED_IHU:Info alias "DHCP IHU IP fixe (IP/MAC)"
redis-cli RPUSH Shaker:module:list DHCP_FIXED_IHU
