"""
Module to generate configuration for Huawei SmartAX EA5800 series OLTs
"""
import string
import random
import yaml
from wonderwords import RandomSentence

s = RandomSentence()


def get_random_mac():
    """ It generates a random mac-address in the format xxxx-xxxx-xxxx """
    mac_address: str = ''
    for _ in range(3):
        mac_address += ''.join(random.choices(string.hexdigits, k=4)) + '-'
    return mac_address[:-1].lower()

def get_ont_global_id():
    """ Get ont global id """
    next_global_id = 0
    while True:
        yield next_global_id
        next_global_id += 1

ont_global_id = get_ont_global_id()

ont_models = [
    'EchoLife EG8145V5',
    'EchoLife EG8247H5',
    'EchoLife EG8040H6',
    'OptiXstar EG8145X6-10'
    'OptiXstar EN8010Ts-20',
    'OptiXstar EG8010Hv6-10',
    'OptiXstar P871E',
    'OptiXstar P615E-L1',
    'OptiXstar P815E-L1',
    'OptiXstar P605E-L1',
    'OptiXstar P612E-E',
    'OptiXstar P805E-L1',
    'OptiXstar P802E',
    'OptiXstar P603E-E'
    'OptiXstar P613E-E',
    'OptiXstar P803E-E',
    'OptiXstar P813E-E',
    'OptiXstar P670E',
    'OptiXstar S600E',
    'OptiXstar S800E',
    'OptiXstar W826P',
    'OptiXstar W826E',
    'OptiXstar W626E-10',
]

ont_states = [
    {
        'config_state': 'normal',
        'match_state': 'match',
        'online_offline': 'online',
        'run_state': 'online',
        'control_flag': 'active',
        'protect_side': 'no',
    },
    {
        'config_state': 'initial',
        'match_state': 'initial',
        'online_offline': 'offline',
        'run_state': 'offline',
        'control_flag': 'active',
        'protect_side': 'no',
    },
    {
        'config_state': 'normal',
        'match_state': 'mismatch',
        'online_offline': 'online',
        'run_state': 'online',
        'control_flag': 'active',
        'protect_side': 'no',
    },
    {
        'config_state': '-',
        'match_state': '-',
        'online_offline': '-',
        'run_state': '-',
        'control_flag': 'active',
        'protect_side': 'yes',
    }
]

gpon_boards = {
    'H901XGHDE': 8,
    'H901OGHK': 24,
    'H901NXED': 8,
    'H901OXHD': 8,
    'H902OXHD': 8,
    'H901GPSFE': 16,
    'H901OXEG': 24,
    'H901TWEDE': 8,
    'H901XSHF': 16,
    'H902GPHFE': 16,
}

configurations = {
    'frames': [
        {
            'frame_id': 0,
            'slots': [],
        },
    ]
}

gpon_board = random.choice(list(gpon_boards))

configurations["memory_usage"] = 50
configurations["cpu_usage"] = 50

configurations['services'] = [
    {
        'service_name': 'telnet',
        'port': 23,
        'state': 'disable',
    },
    {
        'service_name': 'trace',
        'port': 1026,
        'state': 'disable',
    },
    {
        'service_name': 'ssh',
        'port': 22,
        'state': 'enable',
    },
    {
        'service_name': 'snmp',
        'port': 161,
        'state': 'enable',
    },
    {
        'service_name': 'ftp-client',
        'port': None,
        'state': None,
    },
    {
        'service_name': 'sftp-client',
        'port': None,
        'state': None,
    },
    {
        'service_name': 'ntp',
        'port': 123,
        'state': 'enable',
    },
    {
        'service_name': 'radius',
        'port': None,
        'state': 'enable',
    },
    {
        'service_name': 'dhcp-relay',
        'port': 67,
        'state': 'disable',
    },
    {
        'service_name': 'dhcpv6-relay',
        'port': 547,
        'state': 'disable',
    },
    {
        'service_name': 'ntp6',
        'port': 123,
        'state': 'disable',
    },
    {
        'service_name': 'ipdr',
        'port': 4737,
        'state': 'enable',
    },
    {
        'service_name': 'twamp',
        'port': 862,
        'state': 'enable',
    },
    {
        'service_name': 'netconf',
        'port': 830,
        'state': 'enable',
    },
    {
        'service_name': 'telnetv6',
        'port': 23,
        'state': 'disable',
    },
    {
        'service_name': 'sshv6',
        'port': 22,
        'state': 'disable',
    },
    {
        'service_name': 'snmpv6',
        'port': 161,
        'state': 'disable',
    },
    {
        'service_name': 'web-proxy',
        'port': 8024,
        'state': 'disable',
    },
    {
        'service_name': 'portal',
        'port': 2000,
        'state': 'disable',
    },
    {
        'service_name': 'capwap',
        'port': 5246,
        'state': 'enable',
    },
    {
        'service_name': 'mqtt',
        'port': 8883,
        'state': 'disable',
    },
]

configurations['alarm_policies'] = [{
    'policy_id': 0,
    'policy_name': 'alarm-policy_0',
}]

configurations['dba_profiles'] = [
    {
        'profile_id': 0,
        'profile_name': 'dba-profile_0',
        'type': 3,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 0,
        'assure_kbps': 8192,
        'max_kbps': 20480,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 1
    },
    {
        'profile_id': 1,
        'profile_name': 'dba-profile_1',
        'type': 1,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 5120,
        'assure_kbps': 0,
        'max_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 3
    },
    {
        'profile_id': 2,
        'profile_name': 'dba-profile_2',
        'type': 1,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 1024,
        'assure_kbps': 0,
        'max_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    },
    {
        'profile_id': 3,
        'profile_name': 'dba-profile_3',
        'type': 4,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 0,
        'assure_kbps': 0,
        'max_kbps': 32768,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    },
    {
        'profile_id': 4,
        'profile_name': 'dba-profile_4',
        'type': 1,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 1024000,
        'assure_kbps': 0,
        'max_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    },
    {
        'profile_id': 5,
        'profile_name': 'dba-profile_5',
        'type': 1,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 32768,
        'assure_kbps': 0,
        'max_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    },
    {
        'profile_id': 6,
        'profile_name': 'dba-profile_6',
        'type': 1,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 102400,
        'assure_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'max_kbps': 0,
        'bind_times': 0
    },
    {
        'profile_id': 7,
        'profile_name': 'dba-profile_7',
        'type': 2,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 0,
        'assure_kbps': 32768,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'max_kbps': 0,
        'bind_times': 0
    },
    {
        'profile_id': 8,
        'profile_name': 'dba-profile_8',
        'type': 2,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 0,
        'assure_kbps': 102400,
        'max_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    },
    {
        'profile_id': 9,
        'profile_name': 'dba-profile_9',
        'type': 3,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 0,
        'assure_kbps': 32768,
        'max_kbps': 65536,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    },
    {
        'profile_id': 10,
        'profile_name': 'dba-profile_10',
        'type': 1,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 2752,
        'assure_kbps': 0,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'max_kbps': 0,
        'bind_times': 0
    },
    {
        'profile_id': 20,
        'profile_name': 'dba-profile_20',
        'type': 5,
        'bandwidth_compensation': 'No',
        'fix_delay': 'No',
        'fix_kbps': 2048,
        'assure_kbps': 2048,
        'max_kbps': 10240,
        'additional_bandwidth': 'best-effort',
        'best_effort_weight': 0,
        'best_effort_priority': 0,
        'bind_times': 0
    }
]

configurations['t_conts'] = [
    {
        'tcont_id': 0,
        'dba_profile_id': 1,
        'gems': [],
    },
    {
        'tcont_id': 1,
        'dba_profile_id': 2,
        'gems': [],
    },
    {
        'tcont_id': 4,
        'dba_profile_id': 5,
        'gems': [126],
    }
]

configurations['line_profiles'] = [
    {
        'profile_id': 10,
        'profile_name': 'line-profile_10',
        'access-type': 'gpon',
        'fec_upstream_switch': 'Disable',
        'omcc_encrypt_switch': 'On',
        'qos_mode': 'PQ',
        'mapping_mode': 'VLAN',
        'tr069_management': 'disable',
        'tr069_ip_index': '0',
        't_conts': [1],
    },
    {
        'profile_id': 500,
        'profile_name': 'new_link',
        'access-type': 'gpon',
        'fec_upstream_switch': 'Disable',
        'omcc_encrypt_switch': 'On',
        'qos_mode': 'PQ',
        'mapping_mode': 'VLAN',
        'tr069_management': 'disable',
        'tr069_ip_index': '0',
        't_conts': [4],
    }
]

configurations['srv_profiles'] = [
    {
        'profile_id': 1,
        'profile_name': 'srv-profile_1',
        'access-type': 'gpon',
        'ont_ports': {
            'pots': [{} for _ in range(2)],
            'eth': [
                {
                    'qinqmode': 'unconcern',
                    'prioritypolicy': 'unconcern',
                    'inbound': 'unconcern',
                    'outbound': 'unconcern',
                    'dscp_mapping_table_index': 0,
                    'service_type': None,
                    'index': None,
                    's__vlan': None,
                    's__pri': None,
                    'c__vlan': None,
                    'c__pri': None,
                    'encap': None,
                    's__pri_policy': None,
                    'igmp__mode': None,
                    'igmp__vlan': None,
                    'igmp__pri': None,
                    'max_mac_count': 'Unlimited',
                } for _ in range(4)
            ],
            'iphost': [{
                'dscp_mapping_table_index': 0,
            }],
            'tdm': [],
            'moca': [],
            'catv': [],
        },
        'tdm_port_type': 'E1',
        'tdm_service_type': 'TDMoGem',
        'mac_learning_function_switch': 'enable',
        'ont_transparent_function_switch': 'disable',
        'multicast_forward_mode': 'Unconcern',
        'multicast_forward_vlan': None,
        'multicast_mode': 'Unconcern',
        'upstream_igmp_packet_forward_mode': 'Unconcern',
        'upstream_igmp_packet_forward_vlan': None,
        'upstream_igmp_packet_priority': None,
        'native_vlan_option': 'Concern',
        'upstream_pq_color_policy': None,
        'downstream_pq_color_policy': None,
    },
    {
        'profile_id': 500,
        'profile_name': 'new_link',
        'access-type': 'gpon',
        'ont_ports': {
            'pots': [{} for _ in range(2)],
            'eth': [
                {
                    'qinqmode': 'unconcern',
                    'prioritypolicy': 'unconcern',
                    'inbound': 'unconcern',
                    'outbound': 'unconcern',
                    'dscp_mapping_table_index': 0,
                    'service_type': 'Translation' if i == 0 else None,
                    'index': '1' if i == 0 else None,
                    's__vlan': 500 if i == 0 else None,
                    's__pri': None,
                    'c__vlan': 500 if i == 0 else None,
                    'c__pri': None,
                    'encap': None,
                    's__pri_policy': None,
                    'igmp__mode': None,
                    'igmp__vlan': None,
                    'igmp__pri': None,
                    'max_mac_count': 'Unlimited',
                } for i in range(4)
            ],
            'iphost': [{
                'dscp_mapping_table_index': 0,
            }],
            'tdm': [],
            'moca': [],
            'catv': [],
        },
        'tdm_port_type': 'E1',
        'tdm_service_type': 'TDMoGem',
        'mac_learning_function_switch': 'enable',
        'ont_transparent_function_switch': 'disable',
        'multicast_forward_mode': 'Unconcern',
        'multicast_forward_vlan': None,
        'multicast_mode': 'Unconcern',
        'upstream_igmp_packet_forward_mode': 'Unconcern',
        'upstream_igmp_packet_forward_vlan': None,
        'upstream_igmp_packet_priority': None,
        'native_vlan_option': 'Concern',
        'upstream_pq_color_policy': None,
        'downstream_pq_color_policy': None,
    }
]

configurations['srv_profiles'][0]['ont_ports']['eth'][0].update({
    'qinqmode': 'unconcern',
    'prioritypolicy': 'unconcern',
    'inbound': 'unconcern',
    'outbound': 'unconcern',
    'dscp_mapping_table_index': 0,
    'service_type': 'Translation',
    'index': 1,
    's__vlan': 100,
    's__pri': None,
    'c__vlan': 100,
    'c__pri': None,
    'encap': None,
    's__pri_policy': None,
})

configurations["gems"] = [{
    'gem_id': 1,
    'service_type': 'eth',
    'encrypt': 'off',
    'gem_car': '',
    'cascade': 'off',
    "tcont_id": 1,
    'upstream_priority_queue': 0,
    'downstream_priority_queue': None,
    'mappings': [{
        'mapping_index': 1,
        'vlan': 100,
        'priority': '',
        'port_type': '',
        'port_id': '',
        'bundle_id': '',
        'flow_car': '',
        'transparent': '',
    }],
},
{
    'gem_id': 126,
    'service_type': 'eth',
    'encrypt': 'off',
    'gem_car': '',
    'cascade': 'off',
    "tcont_id": 4,
    'upstream_priority_queue': 0,
    'downstream_priority_queue': None,
    'mappings': [{
        'mapping_index': 0,
        'vlan': 500,
        'priority': '',
        'port_type': '',
        'port_id': '',
        'bundle_id': '',
        'flow_car': '',
        'transparent': '',
        }],
}]



configurations['frames'][0]['slots'] = [
    {
        'boardname': gpon_board,
        'online_offline': '',
        'slotid': 0,
        'status': 'Normal',
        'subtype0': '',
        'subtype1': '',
        'ports': [],
    },
    {
        'boardname': '',
        'online_offline': '',
        'slotid': 1,
        'status': '',
        'subtype0': '',
        'subtype1': '',
    },
    {
        'boardname': '',
        'online_offline': '',
        'slotid': 2,
        'status': '',
        'subtype0': '',
        'subtype1': '',
    },
    {
        'boardname': random.choice(["H901PILA", "H901PISA", "H901PISB", "H902PISB"]),
        'online_offline': '',
        'slotid': 2,
        'status': 'Normal',
        'subtype0': '',
        'subtype1': '',
    },
    {
        'boardname': random.choice(['H902MPLAE', 'H901MPSCE']),
        'online_offline': '',
        'slotid': 3,
        'status': 'Normal',
        'subtype0': 'CPCF',
        'subtype1': '',
    },
    {
        'boardname': random.choice(['H901MPSCE', 'H902MPLAE']),
        'online_offline': 'Offline',
        'slotid': 4,
        'status': 'Standby_failed',
        'subtype0': 'CPCF',
        'subtype1': '',
    },
    {
        'boardname': '',
        'online_offline': '',
        'slotid': 5,
        'status': '',
        'subtype0': '',
        'subtype1': '',
    }
]

configurations["vlans"] = {
    100: {
        "type": "smart",
        "attr": "common",
    },
}

configurations["service_ports"] = {}

for i in range(gpon_boards[gpon_board]):
    registered = 0
    onts = []
    for _ in range(random.randint(1, 32)):
        register = False
        if i == 6:
            if random.random() < 0.2:
                register = True
        elif random.random() < 0.8:
            register = True
        ont = {
            **random.choice(ont_states),
            'ont_id': registered if register else None,
            'description': s.bare_bone_with_adjective(),
            'sn': ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
            'registered': register,
            'is_epon': False,
            'oui_version': 'CTC3.0',
            'model': '240',
            'extended_model': 'HG8240',
            'nni_type': 'auto',
            'actual_nni_type': 'auto',
            'last_actual_nni_type': 'auto',
            'password': '0x303030303030303030300000000000000000000000000000000000000000000000000000(0000000000)',
            'loid': '000000000000000000000000',
            'checkcode': '000000000000',
            'vendor_id': 'HWTC',
            'version': 'MXU VER.A',
            'software_version': 'V8R017C00',
            'hardware_version': '140C4510',
            'equipment_id': "MXU",
            'customized_info': '',
            'mac': get_random_mac(),
            'equipment_sn': '',
            'multi-channel': 'Not support',
            'llid': '',
            'distance_m': random.randint(10, 90),
            'last_distance_m': random.randint(10, 90),
            'rtt_tq': '',
            'memory_occupation': random.randint(10, 90),
            'cpu_occupation': random.randint(10, 90),
            'temperature': random.randint(30,60),
            'authentic_type': 'SN-auth',
            'management_mode': 'OMCI',
            'software_work_mode': 'normal',
            'multicast_mode': 'IGMP-Snooping',
            'last_down_cause': 'dying-gasp',
            'type_d_support': 'Not support',
            'isolation_state': 'normal',
            'interoperability_mode': 'unknown',
            'vs_id': 0,
            'vs_name': 'admin-vs',
            'global_ont_id': next(ont_global_id),
            'fiber_route': '',
            'line_profile_id': 10,
            'srv_profile_id': 1,
            'alarm_policy_id': 0,
            'rx_power': round(random.uniform(-5, -32), 2),
            'tx_power': round(random.uniform(4, -5), 2),
            'olt_rx_ont_power': round(random.uniform(-7, -29), 2),
            'voltage_v': round(random.uniform(3.2, 3.6), 2),
            'current_ma': random.randint(5, 9),
            "ports": {
                "eth": {
                    1: {
                        "c__vlan": None,
                        "c__pri": 2,
                        "eth__type": None,
                        "vlan__type": "Translation",
                        "s__vlan": 1,
                        "s__pri": 7,
                        "s__pri_policy": None,
                        "native_vlan": 1,
                        "default_priority": 0,
                        "downstream_mode": "operation",
                        "mismatch_policy": "discard",
                    },
                    2: {
                        "c__vlan": 100,
                        "c__pri": None,
                        "eth__type": "IPoE",
                        "vlan__type": "QINQ",
                        "s__vlan": 20,
                        "s__pri": 3,
                        "s__pri_policy": "DSCP",
                        "native_vlan": None,
                        "default_priority": None,
                        "downstream_mode": None,
                        "mismatch_policy": None,
                    },
                    3: {
                        "c__vlan": 1,
                        "c__pri": None,
                        "eth__type": None,
                        "vlan__type": "Translation",
                        "s__vlan": 1,
                        "s__pri": None,
                        "s__pri_policy": None,
                        "native_vlan": 1,
                        "default_priority": 0,
                        "downstream_mode": "operation",
                        "mismatch_policy": "discard",
                    },
                    4: {
                        "c__vlan": 100,
                        "c__pri": None,
                        "eth__type": "0x6321",
                        "vlan__type": "QINQ",
                        "s__vlan": 70,
                        "s__pri": None,
                        "s__pri_policy": None,
                        "native_vlan": None,
                        "default_priority": None,
                        "downstream_mode": None,
                        "mismatch_policy": None,
                    },
                },
            },
            "gemports": [126],
        }
        if register:
            registered += 1
        onts.append(ont)
    configurations['frames'][0]['slots'][0]['ports'].append(onts)


with open('huawei_smartax.yaml.j2', 'w', encoding='utf-8') as f:
    f.write(yaml.dump(configurations))
