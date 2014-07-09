redis-cli HSET M:DHCP_FIXED_HARAS:Forms 0 "yes:yes:IP:ip"
redis-cli HSET M:DHCP_FIXED_HARAS:Forms 1 "no:yes:MAC:mac"
redis-cli HSET M:DHCP_FIXED_HARAS:Forms 2 "no:yes:hostname:hostname"
redis-cli HSET M:DHCP_FIXED_HARAS:Button 0 "Red:Update:DHCP_FIXED_HARAS_update:"
redis-cli HSET M:DHCP_FIXED_HARAS:Info alias "DHCP HARAS ip fixe"
redis-cli RPUSH Shaker:module:list DHCP_FIXED_HARAS
