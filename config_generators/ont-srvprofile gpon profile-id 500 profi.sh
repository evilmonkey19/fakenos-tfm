ont-srvprofile gpon profile-id 500 profile-name new_link

ont-port pots 4 eth 4

port vlan eth1 500

commit

quit

ont-lineprofile gpon profile-id 500 profile-name new_link

tcont 4 dba-profile-id 5

gem add 126 eth tcont 4

gem mapping 126 0 vlan 500 

commit

quit

display ont-lineprofile gpon all


interface gpon 0/0

display ont autofind 6

ont add 6 sn-auth QADE441BEU2JKGSE omci ont-lineprofile-id 500 ont-srvprofile-id 500 desc New_link

display ont info 6 2
[ "control_flag": active, "run_state": online, "config_state": normal, "match_state": match]

