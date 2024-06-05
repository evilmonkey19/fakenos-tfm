"""
Module to generate configuration for Huawei SmartAX EA5800 series OLTs
"""
import string
import random
import yaml
from wonderwords import RandomSentence

s = RandomSentence()



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
    'H901OGHK': 48,
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

configurations['frames'][0]['slots'] = [
    {
        'boardname': gpon_board,
        'online_offline': '',
        'slotid': 0,
        'status': 'Normal',
        'subtype0': '',
        'subtype1': '',
        'ports': [[
            {
                **random.choice(ont_states),
                'ont_id': i,
                'description': s.bare_bone_with_adjective(),
                'sn': ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
                'registered': random.choice([True, False]),
                'is_epon': False,
                'oui_version': 'CTC3.0',
                'model': '240',
                'extended_model': 'HG8240',
                'nni_type': 'auto',
                'password': '0x303030303030303030300000000000000000000000000000000000000000000000000000(0000000000)',
                'loid': '000000000000000000000000',
                'checkcode': '000000000000',
                'vendor_id': 'HWTC',
                'version': 'MXU VER.A',
                'software_version': 'V8R017C00',
                'hardware_version': '140C4510',
                'equipment_id': "MXU",
                'customized_info': '',
                'mac': '',
                'equipment_sn': '',
                'multi-channel': 'Not support',
                
                
            } for i in range(random.randint(1,32))
        ] for _ in range(gpon_boards[gpon_board])]
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

with open('huawei_smartax.yaml.j2', 'w', encoding='utf-8') as f:
    f.write(yaml.dump(configurations))
