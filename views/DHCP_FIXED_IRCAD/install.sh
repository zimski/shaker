redis-cli HSET M:DHCP_FIXED_IRCAD:Forms 0 "yes:yes:IP:ip"
redis-cli HSET M:DHCP_FIXED_IRCAD:Forms 1 "no:yes:MAC:mac"
redis-cli HSET M:DHCP_FIXED_IRCAD:Forms 2 "no:yes:hostname:hostname"
redis-cli HSET M:DHCP_FIXED_IRCAD:Button 0 "Red:Update:DHCP_FIXED_IRCAD_update:"
redis-cli HSET M:DHCP_FIXED_IRCAD:Info alias "DHCP ircad ip fixe"
redis-cli RPUSH Shaker:module:list DHCP_FIXED_IRCAD
