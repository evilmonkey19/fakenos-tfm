"""
NOS module for Huawei SmartAX
"""

# import time
# import os
import copy
import os
import re
import random
import time
from datetime import datetime
import datetime
import random
from typing import Dict, List

from fakenos.plugins.nos.platforms_py.base_template import BaseDevice


NAME: str = "huawei_smartax"
INITIAL_PROMPT: str = "{base_prompt}>"
ENABLE_PROMPT: str = "{base_prompt}#"
CONFIG_PROMPT: str = "{base_prompt}(config)#"
DEVICE_NAME: str = "HuaweiSmartAX"
CONFIG_GPON_LINEPROFILE: str = r"^{base_prompt}(config-gpon-lineprofile-\d+)#"
CONFIG_GPON_SRVPROFILE: str = r"^{base_prompt}(config-gpon-srvprofile-\d+)#"
CONFIG_IF_GPON: str = r"^{base_prompt}(config-if-gpon-\d+\/\d+)#"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIGURATION = os.path.join(BASE_DIR, "configurations/huawei_smartax.yaml.j2")


# Huawei when doing tables use predefined spacing.
# The spacing corresponds to the largest possible value in the column
# unless the column title is larger than the largest value if there 
# isn't a space in between the title.
# Example:
# F/S/P: 0/ 1/11 (value is larger)
# ONT ID: 0 (title is larger)
FRAME_SPACING: Dict[str, int] = {
    "SlotID": ("left", len(max("SlotID", "0", "1", "2", "3", "4", "5", key=len))),
    "BoardName": ("left", len(max("BoardName", "A123ABCD", key=len))),
    "Status": ("left", len(max("Status", "Normal", "Active_normal", "Standby_failed", key=len))),
    "SubType0": ("left", len(max("SubType0", "CPCF", key=len))),
    "SubType1": ("left", len(max("SubType1", "CPCF", key=len))),
    "Online/Offline": ("left", len(max("Online/Offline", "Offline", "Online", key=len))),
    "F/S/P": ("left", len(max("F/S/P", "0/ 1/1", "0/ 1/11", key=len))),
    "ONT ID": ("right", len(max("ONT", "ID", "1", "11", key=len))),
    "ONT-ID": ("right", len(max("ONT-ID", "1", "11", key=len))),
    "SN": ("center", len(max("SN","1234567890ABCDEF", key=len))),
    "Control flag": ("left", len(max("control", "flag","active", "configuring", key=len))),
    "Config state": ("left", len(max("config", "state", "online", "normal", "failing" ,key=len))),
    "Run state": ("left", len(max("run", "state", "online", "offline", key=len))),
    "Match state": ("left", len(max("match", "state", "initial", "match", "mismatch", key=len))),
    "Protect side": ("left", len(max("protect", "side", "yes", "no", key=len))),
    "Description": ("left", len(max("description", "Generic_description", "The acoustic explanation slaps.", key=len))),
    "Network service": ("left", len(max("network service", "dhcpv6-relay", key=len))),
}

SERVICES_SPACING: Dict[str, int] = {
    "Network service": ("left", len(max("Network service", "dhcpv6-relay", key=len))),
    "Port": ("left", len(max("Port", "4294967295", key=len))),
    "State": ("left", len(max("State", "disable", "enable", key=len))),
}

DBA_PROFILES_SPACING: Dict[str, int] = {
    "Profile-ID": ("right", len(max("Profile-ID", "10", "1", key=len))),
    "Type": ("right", len(max("Type", "1", "2", "3", "4", "5", key=len))),
    "Bandwidth Compensation": ("right", len(max("Bandwidth", "Compensation", "no", "yes", key=len))),
    "Fix (kbps)": ("right", len(max("Fix", "(kbps)", "102400", "10240000", key=len))),
    "Assure (kbps)": ("right", len(max("Assure", "(kbps)", "102400", "10240000", key=len))),
    "Max (kbps)": ("right", len(max("Max", "(kbps)", "102400", "10240000", key=len))),
    "Bind times": ("right", len(max("Bind", "times", "1", "10", key=len))),
}

ONT__LINEPROFILE_SPACING: Dict[str, int] = {
    "Profile-ID": ("left", len(max("Profile-ID", "10", "1", key=len))),
    "Profile-name": ("left", 40),
    "Binding times": ("left", len(max("Binding times", "1", "10", key=len))),
}

GPON_BOARDS: Dict[str, int] = {
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

class HuaweiSmartAX(BaseDevice):
    """
    Class that keeps track of the state of the Huawei SmartAX device.
    """
    SYSTEM_STARTUP_TIME: datetime = datetime.datetime.now() \
            - datetime.timedelta(days=random.randint(1, 365), 
                                 hours=random.randint(1, 24),
                                 minutes=random.randint(1, 60), 
                                 seconds=random.randint(1, 60))
    
    changing_config: dict = {}

    def _add_whitespaces_column(self, column: List[str], spacing: Dict[str, int] = None):
        """
        Add whitespacing to a column depending on the
        largest element in the column.
        """
        max_length = spacing[column[0]][1]
        if spacing[column[0]][0] == "right":
            return [str(row).rjust(max_length) for row in column]
        if spacing[column[0]][0] == "center":
            return [str(row).center(max_length) for row in column]
        return [str(row).ljust(max_length) for row in column]

    def _get_keywords(self, titles: List[str]):
        """ Return a list of keywords from a list of titles. """
        if any(' ' in t for t in titles):
            titles_parsed = [title.split(' ') if ' ' in title else [title, ""] for title in titles]
            titles_parsed = ["_".join(title).lower() if title[1] else title[0].lower() for title in titles_parsed]
            titles_parsed = [title.replace("/", "_").replace("-", "_").replace("(", "").replace(")", "") for title in titles_parsed]
            return titles_parsed
        return [title.lower().replace("/", "_") for title in titles]
    
    def make_display_board(self, **kwargs):
        """ Return String of board information. """
        args = kwargs['args']
        if not isinstance(args, str) and args.isdigit():
            return "Please provide the frame number correctly."
        args = int(args)
        boards = copy.deepcopy(self.configurations["frames"][args]["slots"])
        return self.render("huawei_smartax/display_board.j2", boards=boards)

    def make_display_onts(self, **kwargs):
        """ Return the ONTs information 
        
        Example:
            -----------------------------------------------------------------------------
            F/S/P   ONT         SN         Control     Run      Config   Match    Protect
                    ID                     flag        state    state    state    side 
            -----------------------------------------------------------------------------
            0/ 1/0    0  1234567890ABCDEF  active      online   normal   match    no 
            0/ 1/0    1  1234567890ABCDEF  active      online   normal   match    no 
            0/ 1/0    2  1234567890ABCDEF  active      online   normal   match    no 
            -----------------------------------------------------------------------------
            F/S/P       ONT  Description  
                        ID  
            -----------------------------------------------------------------------------
            0/ 1/0       0   Generic_description
            0/ 1/0       1   Generic_description
            0/ 1/0       2   Generic_description
            -----------------------------------------------------------------------------
            In port 0/ 1/0 , the total of ONTs are: 3, online: 3
            -----------------------------------------------------------------------------
        """
        prompt_config_if_gpon = CONFIG_IF_GPON.replace("(", "\\(").replace(")", "\\)")
        prompt_config_if_gpon = prompt_config_if_gpon.format(base_prompt=kwargs["base_prompt"])
        if not all(val.isdigit() for val in kwargs['args'].split(" ")):
            return "Please provide the port number correctly."
        if re.match(prompt_config_if_gpon, kwargs["current_prompt"]):
            matches_args = re.findall(r'(\d+)', kwargs['args'])
            if len(matches_args) < 1 or len(matches_args) > 3:
                return "Please provide the port number correctly."
            matches = re.findall(r'\d+', kwargs['current_prompt'])
            frame = matches[-1]
            slot = matches[-2]
            kwargs["args"] = f"{frame} {slot} {kwargs['args']}"
        pattern = r"^\d+\s\d+\s\d+\s*(\d+)?$"
        if not re.match(pattern, kwargs['args']):
            return "Please provide the port number correctly."
        if len(kwargs['args'].split(" ")) == 3:
            return self.make_display_ont_info_list(**kwargs)
        return self.make_display_ont_info_one(**kwargs)
    
    def make_display_ont_info_list(self, **kwargs):
        """ Return the ONTs information in a list format"""    
        try:
            frame_index, board_index, port_index = (int(value) for value in kwargs['args'].split(" "))
            frame = copy.deepcopy(self.configurations["frames"][frame_index])
            if frame['slots'][board_index]['boardname'] not in GPON_BOARDS:
                return "The board is not a PON board."
            if port_index >= GPON_BOARDS[frame['slots'][board_index]['boardname']]:
                return "The port does not exist in the board."
            board = frame['slots'][board_index]
            onts = board["ports"][port_index]
            onts = [ont for ont in onts if ont.get("registered")]
            port = f"{frame_index}/ {board_index}/{port_index}"
            for ont in onts:
                ont["f_s_p"] = port
                ont["ont-id"] = ont["ont_id"]
            return self.render("huawei_smartax/display_ont_info_list.j2", onts=onts)
        except (IndexError, ValueError):
            return "There are no ONTs in the specified port."
        
    def make_display_ont_info_one(self, **kwargs):
        """ Return the ONTs information in a single format"""    
        try:
            frame_index, board_index, port_index, ont_id = (int(value) for value in kwargs['args'].split(" "))
            configurations = copy.deepcopy(self.configurations)
            frame = configurations["frames"][frame_index]
            if frame['slots'][board_index]['boardname'] not in GPON_BOARDS:
                return "The board is not a PON board."
            if port_index >= GPON_BOARDS[frame['slots'][board_index]['boardname']]:
                return "The port does not exist in the board."
            board = frame['slots'][board_index]
            onts = board["ports"][port_index]
            ont = next((ont for ont in onts if ont["ont_id"] == ont_id), None)
            if not ont:
                return "The ONT does not exist in the port."
            ont['fsp'] = f"{frame_index}/ {board_index}/{port_index}"
            line_profile = next((line_profile for line_profile in configurations["line_profiles"] if line_profile["profile_id"] == ont["line_profile_id"]), None)
            t_conts = [t_cont for t_cont in configurations["t_conts"] if line_profile["t_conts"]]
            for t_cont in t_conts:
                t_cont["gems"] = [gem for gem in configurations["gems"] if gem["gem_id"] in t_cont["gems"]]
            service_profile = next((service_profile for service_profile in configurations["srv_profiles"] if service_profile["profile_id"] == ont["srv_profile_id"]), None)
            alarm_policy = next((alarm_policy for alarm_policy in configurations["alarm_policies"] if alarm_policy["policy_id"] == ont["alarm_policy_id"]), None)
            return self.render(
                "huawei_smartax/display_ont_info_one.j2", 
                **ont,
                line_profile=line_profile,
                service_profile=service_profile,
                t_conts=t_conts,
                alarm_policy=alarm_policy,
                )
        except (IndexError, ValueError):
            return "There are no ONTs in the specified port."

    def make_display_sysman_service_state(self, **kwargs):
        """ Return the sysman service state information """
        services = copy.deepcopy(self.configurations["services"])
        return self.render("huawei_smartax/display_sysman_service_state.j2", services=services)

    def make_dba__profile_add(self, **kwargs):
        """ Adds a DBA profile with the corresponding parameters. """
        if not isinstance(kwargs['args'], str):
            return "Please provide the profile name."
        args = kwargs['args'].split(' ')
        new_dba_profile = {
            'profile_id': len(self.configurations["dba_profiles"]) + 1,
            'profile_name': f'profile_id_{len(self.configurations["dba_profiles"]) + 1}',
            'type': None,
            'bandwidth_compensation': 'No',
            'fix_delay': 'No',
            'fix_kbps': 0,
            'assure_kbps': 0,
            'max_kbps': 0,
            'additional_bandwidth': 'best-effort',
            'best_effort_weight': 0,
            'best_effort_priority': 0,
            'bind_times': 0,
        }
        args_iterator = iter(args)
        for arg in args_iterator:
            if arg == "profile-id":
                next_arg = next(args_iterator)
                if not next_arg.isdigit():
                    return "Please provide the correct profile id."
                new_dba_profile['profile_id'] = int(next_arg)
            elif arg == "profile-name":
                next_arg = next(args_iterator)
                if next_arg.isdigit():
                    return "Please provide the correct profile name that is not only numbers."
                new_dba_profile['profile_name'] = next_arg
            elif arg in ["type1", "type2", "type3", "type4", "type5"]:
                new_dba_profile['type'] = int(arg[-1])
            elif arg == "bandwidth-compensation":
                next_arg = next(args_iterator)
                if not next_arg in ["yes", "no"]:
                    return "Please provide the correct bandwidth compensation."
                new_dba_profile['bandwidth-compensation'] = next_arg
            elif arg in ["fix", "assure", "max"]:
                next_arg = next(args_iterator)
                if not next_arg.isdigit():
                    return "Please provide the correct kbps value."
                new_dba_profile[f"{arg}_kbps"] = int(next_arg)
            else:
                return "Please provide the correct arguments."
        if new_dba_profile['profile_id'] in [dba_profile['profile_id'] for dba_profile in self.configurations["dba_profiles"]] \
            or new_dba_profile['profile_name'] in [dba_profile['profile_name'] for dba_profile in self.configurations["dba_profiles"]]:
            return "The DBA profile already exists."
        self.configurations["dba_profiles"].append(new_dba_profile)
        self.configurations["dba_profiles"].sort(key=lambda x: x['profile_id'])

        return self.render("huawei_smartax/dba__profile_add.j2", **new_dba_profile)

    def make_display_dba__profile(self, **kwargs):
        """ Display the DBAs based on the args. """
        args = kwargs['args'].split(' ')
        if args[0] == 'all':
            return self.make_display_dba__profile_all()
        elif args[0] == 'profile-name':
            if not len(args) != 2:
                return "Please provide the profile name correctly."
            return self.make_display_dba__profile_profile__name(profile_name=args[1])
        return "Please provide the correct arguments."
        
    def make_display_ont_autofind(self, **kwargs):
        """ Displays the ONT autofind information. """
        port: int = None
        if kwargs["args"].isdigit():
            port = int(kwargs["args"])
        gpon_onts, epon_onts = self._get_onts_autofind(port_number=port)
        return self.render("huawei_smartax/display_ont_autofind_all.j2", gpon_onts = gpon_onts, epon_onts = epon_onts)
    
    def _get_onts_autofind(self, port_number: int = None):
        """ Return the ONTs information that are not registered yet. """
        frames = copy.deepcopy(self.configurations["frames"])
        autofind_time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S%z")
        onts_autofind: List = []
        for frame in frames:
            for slot in frame["slots"]:
                if 'ports' not in slot:
                    continue
                if port_number:
                    for ont in slot["ports"][port_number]:
                        if not ont["registered"]:
                            ont["fsp"] = f"{frames.index(frame)}/{frame['slots'].index(slot)}/{port_number}"
                            ont["autofind_time"] = autofind_time
                            onts_autofind.append(ont)
                else:
                    for port in slot["ports"]:
                        for ont in port:
                            if not ont["registered"]:
                                ont["fsp"] = f"{frames.index(frame)}/{frame['slots'].index(slot)}/{port.index(ont)}"
                                ont["autofind_time"] = autofind_time
                                onts_autofind.append(ont)
        gpon_onts = [ont for ont in onts_autofind if not ont["is_epon"]]
        epon_onts = [ont for ont in onts_autofind if ont["is_epon"]]
        return gpon_onts, epon_onts
    
    def make_display_dba__profile_all(self, **kwargs):
        """ Displays all the DBA profiles. """
        dba_profiles = copy.deepcopy(self.configurations["dba_profiles"])
        titles = ["Profile-ID", "Type", "Bandwidth Compensation", "Fix (kbps)", "Assure (kbps)", "Max (kbps)", "Bind times"]
        titles: dict = {title:keyword for title, keyword in zip(titles, self._get_keywords(titles))}
        for title, keyword in titles.items():
            dba_profiles_column = [dba_profile[keyword] for dba_profile in dba_profiles]
            results = self._add_whitespaces_column([title] + dba_profiles_column, DBA_PROFILES_SPACING)
            dba_profiles_column = results[1:]
            titles[title] = results[0]
            for dba_profile in dba_profiles:
                dba_profile[keyword] = dba_profiles_column[dba_profiles.index(dba_profile)]
        return self.render("huawei_smartax/display_dba__profile_all.j2", dba_profiles=dba_profiles)
    
    def make_display_dba__profile_profile__name(self, profile_name: str = None):
        """ Displays one DBA profile based on the name. """
        dba_profiles= copy.deepcopy(self.configurations["dba_profiles"])
        dba_profile = next((dba_profile for dba_profile in dba_profiles if dba_profile["profile_name"] == profile_name), None)
        return self.render("huawei_smartax/display_dba__profile_profile__name.j2", **dba_profile)

    def make_quit(self, **kwargs):
        """ Exit the current level of the CLI """
        base_prompt = kwargs["base_prompt"]
        current_prompt = kwargs["current_prompt"]
        initial_prompt = INITIAL_PROMPT.format(base_prompt=base_prompt)
        enable_prompt = ENABLE_PROMPT.format(base_prompt=base_prompt)
        config_prompt = CONFIG_PROMPT.format(base_prompt=base_prompt)
        config_gpon_srvprofile = CONFIG_GPON_SRVPROFILE.format(base_prompt=base_prompt)
        config_gpon_lineprofile = CONFIG_GPON_LINEPROFILE.format(base_prompt=base_prompt)
        config_if_gpon = CONFIG_IF_GPON.format(base_prompt=base_prompt)
        patterns = [config_gpon_lineprofile, config_gpon_srvprofile, config_if_gpon]
        patterns = [pattern.replace("(", "\\(").replace(")", "\\)") for pattern in patterns]
        self.changing_config = None
        if current_prompt in [initial_prompt, enable_prompt]:
            return True
        if current_prompt in config_prompt:
            return {"output": None, "new_prompt": ENABLE_PROMPT}
        if any(re.match(pattern, current_prompt) for pattern in patterns):
            return {"output": None, "new_prompt": CONFIG_PROMPT}
        raise RuntimeError(f"make_quit does not know how to handle '{current_prompt}' prompt")

    def make_display_ont_info_all(self):
        """ Return the ONTs information that are not registered yet. """

    def make_display_ont_info(self, **kwargs):
        """ Return the ONTs information """
        args = kwargs['args']
        if args == "all":
            return self.make_display_ont_info_all()
        raise NotImplementedError(f"make_display_ont_info does not know how to handle '{args}'")

    def make_display_sysuptime(self, **kwargs):
        """ Return the system uptime. """
        uptime: datetime = datetime.datetime.now() - self.SYSTEM_STARTUP_TIME
        days: int = uptime.days
        hours: int = uptime.seconds // 3600
        minutes: int = (uptime.seconds // 60) % 60
        seconds: int = uptime.seconds % 60
        return self.render(
            "huawei_smartax/display_sysuptime.j2",
            days=days, hours=hours, minutes=minutes, seconds=seconds
        )
    
    def make_ont__srvprofile(self, **kwargs):
        """ Return the ONT service profile based on the profile id. """
        pattern = r'^(gpon|epon) profile-id \d+ profile-name \S+$'
        if not re.match(pattern, kwargs["args"]):
            return "Invalid args format"
        self.changing_config = copy.deepcopy(self.configurations)
        new_srv_profile = {
            "profile_id": int(kwargs["args"].split(" ")[2]),
            "profile_name": kwargs["args"].split(" ")[-1],
            "access_type": kwargs["args"].split(" ")[0],
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
        self.changing_config["srv_profiles"].append(new_srv_profile)
        ont_srvprofile_prompt = "{base_prompt}(config-gpon-srvprofile-{profile_id})#"
        prompt = ont_srvprofile_prompt.format(base_prompt=kwargs["base_prompt"], profile_id=new_srv_profile["profile_id"])
        return {"output": "", "new_prompt": prompt}
    
    def make_ont__port(self, **kwargs):
        """ Configure the service profile for the ONT ports. """
        pattern = r"(pots|eth|tdm|moca|catv) (\d+)"
        matches = re.findall(pattern, kwargs["args"])
        if not matches or len(matches) != len(set(m[0] for m in matches)) or \
            len(matches) != len(kwargs['args'].split(' '))/2:
            return "Invalid args format"
        ont_srvprofile_id = int(kwargs["current_prompt"].split("-")[-1].split(")")[0])
        srv_profile = next((srv_profile for srv_profile in self.changing_config["srv_profiles"] if srv_profile["profile_id"] == ont_srvprofile_id), None)
        ont_ports = {
            "pots": [],
            "eth": [],
            'iphost': [{
                'dscp_mapping_table_index': 0,
            }],
            "tdm": [],
            "moca": [],
            "catv": [],
        }
        for port_type, count in matches:
            for _ in range(int(count)):
                if port_type == "pots":
                    ont_ports["pots"].append({})
                elif port_type == "eth":
                    ont_ports["eth"].append({
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
                        'encap': None,
                        's__pri_policy': None,
                        'igmp__mode': None,
                        'igmp__vlan': None,
                        'igmp__pri': None,
                        'max_mac_count': 'Unlimited',
                    })
                elif port_type == "tdm":
                    ont_ports["tdm"].append({})
                elif port_type == "moca":
                    ont_ports["moca"].append({})
                elif port_type == "catv":
                    ont_ports["catv"].append({})
        srv_profile['ont_ports'] = ont_ports
        return ""
    
    def make_port_vlan(self, **kwargs):
        """ Configure the VLAN for the port. """
        pattern = r"^(eth)(\d+) (\d+)$"
        if not re.match(pattern, kwargs["args"]):
            return "Invalid args format"
        match = re.findall(pattern, kwargs["args"])
        ont_srvprofile_id = int(kwargs["current_prompt"].split("-")[-1].split(")")[0])
        srv_profile = next((srv_profile for srv_profile in self.changing_config["srv_profiles"] if srv_profile["profile_id"] == ont_srvprofile_id), None)
        srv_profile["ont_ports"][match[0][0]][int(match[0][1])-1].update({
            "service_type": "Translation",
            "index": int(match[0][1]),
            "s__vlan": int(ont_srvprofile_id),
            "s__pri": None,
            "c__vlan": int(match[0][2]),
            'c__pri': None,
            'encap': None,
            's__pri_policy': None,
        })
        return "Set ONT port(s) VLAN configuration, success: 1, failed: 0"

    def make_ont__lineprofile(self, **kwargs):
        """ Return the ONT line profile based on the profile id. """
        pattern = r'^(gpon|epon) profile-id \d+ profile-name \S+$'
        if not re.match(pattern, kwargs["args"]):
            return "Invalid args format"
        self.changing_config = copy.deepcopy(self.configurations)
        new_line_profile = {
            "profile_id": int(kwargs["args"].split(" ")[2]),
            "profile_name": kwargs["args"].split(" ")[-1],
            "access-type": kwargs["args"].split(" ")[0],
            "fec_upstream_switch": 'Disable',
            'omcc_encrypt_switch': 'On',
            'qos_mode': 'PQ',
            'mapping_mode': 'VLAN',
            'tr069_management': 'disable',
            'tr069_ip_index': 0,
            't_conts': [],
        }
        self.changing_config["line_profiles"].append(new_line_profile)
        ont_lineprofile_prompt = "{base_prompt}(config-gpon-lineprofile-{profile_id})#"
        prompt = ont_lineprofile_prompt.format(base_prompt=kwargs["base_prompt"], profile_id=new_line_profile["profile_id"])
        return {"output": "", "new_prompt": prompt}
    
    def make_tcont(self, **kwargs):
        """ Configure the T-CONT """
        pattern = r'^\d+ dba-profile-id \d+$'
        if not re.match(pattern, kwargs["args"]):
            return "Invalid args format"
        tcont_id = int(kwargs["args"].split(" ")[0])
        dba_profile_id = int(kwargs["args"].split(" ")[-1])
        if dba_profile_id not in [dba_profile["profile_id"] for dba_profile in self.changing_config["dba_profiles"]]:
            return "The DBA profile does not exist."
        ont_lineprofile_id = int(kwargs["current_prompt"].split("-")[-1].split(")")[0])
        line_profile = next((line_profile for line_profile in self.changing_config["line_profiles"] if line_profile["profile_id"] == ont_lineprofile_id), None)
        if not line_profile:
            return "The line profile does not exist."
        self.changing_config["t_conts"].append({
            "tcont_id": tcont_id,
            "dba_profile_id": dba_profile_id,
            "gems": [],
        })
        line_profile['t_conts'].append(tcont_id)
        return ""
    
    def make_display_ont__lineprofile(self, **kwargs):
        """ Display the ONT line profile """
        # changing_config = copy.deepcopy(self.configurations)
        # line_profiles = changing_config(line_profiles)
        line_profiles = copy.deepcopy(self.configurations["line_profiles"])
        if kwargs["args"] != "gpon all":
            return "not implementd yet."
        if not line_profiles:
            return "There are no line profiles."
        for line_profile in line_profiles:
            line_profile["binding_times"] = 0
        titles = ["Profile-ID", "Profile-name", "Binding times"]
        titles: dict = {title:keyword for title, keyword in zip(titles, self._get_keywords(titles))}
        for title, keyword in titles.items():
            line_profiles_column = [line_profile[keyword] for line_profile in line_profiles]
            results = self._add_whitespaces_column([title] + line_profiles_column, ONT__LINEPROFILE_SPACING)
            line_profiles_column = results[1:]
            titles[title] = results[0]
            for line_profile in line_profiles:
                line_profile[keyword] = line_profiles_column[line_profiles.index(line_profile)]
        return self.render("huawei_smartax/display_ont__lineprofile.j2", line_profiles=line_profiles)

    def make_gem_add(self, **kwargs):
        """ Add a GEM port """
        pattern = r'^\d+ eth tcont \d+'
        args = kwargs["args"]
        if not re.match(pattern, args):
            return "Invalid args format"
        args = args.split(" ")
        gem_id = int(args[0])
        if gem_id < 0 or gem_id > 1023:
            return "Port must be between 0 and 1023"
        tcont_id = int(args[-1])
        tcont = next((tcont for tcont in self.changing_config["t_conts"] if tcont["tcont_id"] == tcont_id), None)
        if not tcont:
            return "The T-CONT does not exist."
        self.changing_config["gems"].append({
            "gem_id": gem_id,
            'service_type': 'eth',
            'encrypt': 'off',
            'gem_car': '',
            'cascade': 'off',
            "tcont_id": tcont_id,
            'upstream_priority_queue': 0,
            'downstream_priority_queue': None,
            'mappings': [],
        })
        tcont["gems"].append(gem_id)
        return ""

    
    def make_gem_mapping(self, **kwargs):
        """ Map a GEM port """
        pattern = r'^\d+ \d+ vlan \d+'
        args = kwargs["args"]
        if not re.match(pattern, args):
            return "Invalid args format"
        args = args.split(" ")
        gem_id = int(args[0])
        if gem_id < 0 or gem_id > 1023:
            return "Port must be between 0 and 1023"
        mapping_index = int(args[1])
        if not 0 <= mapping_index <= 7:
            return "Mapping index must be between 0 and 7"
        vlan = int(args[-1])
        if not 1 <= vlan <= 4094:
            return "VLAN must be between 1 and 4094"
        gem = next((gem for gem in self.changing_config["gems"] if gem["gem_id"] == gem_id), None)
        if not gem:
            return "The GEM port does not exist."
        gem["mappings"].append({
            'mapping_index': mapping_index,
            'vlan': vlan,
            'priority': '',
            'port_type': '',
            'port_id': '',
            'bundle_id': '',
            'flow_car': '',
            'transparent': '',
        })
        return ""

    
    def make_interface_gpon(self, **kwargs):
        """ Configure the GPON interface """
        pattern = r'^\d+/\d+$'
        if not re.match(pattern, kwargs["args"]):
            return "Invalid args format"
        frame = int(kwargs["args"].split("/")[0])
        slot = int(kwargs["args"].split("/")[1])
        if frame not in range(0, 6) or slot not in range(0, 16):
            return "The frame or slot does not exist."
        if self.configurations["frames"][frame]["slots"][slot]["boardname"] not in GPON_BOARDS:
            return "The board is not a PON board."
        self.changing_config = copy.deepcopy(self.configurations)
        prompt = f"{kwargs['base_prompt']}(config-if-gpon-{frame}/{slot})#"
        return {"output": "", "new_prompt": prompt}

    def make_ont_add(self, **kwargs):
        """ Add an ONT to the system """
        args = kwargs.get("args", "")
        pattern = r'^\d+ sn-auth \S{16} omci ont-lineprofile-id \d+ ont-srvprofile-id \d+ desc .{0,64}$'
        if not re.match(pattern, args):
            return "Invalid args format"
        port = int(args.split(" ")[0])
        if port not in range(GPON_BOARDS[self.configurations["frames"][0]["slots"][0]["boardname"]]):
            return "The port does not exist."
        onts_autofind_gpon, _ = self._get_onts_autofind(port_number=port)
        ont = self._find_ont(onts_autofind_gpon, sn = args.split(" ")[2])
        if ont:
            onts = self.configurations["frames"][0]["slots"][0]["ports"][port]
            ont["ont_id"] = len([ont for ont in onts if ont.get("registered")])
            ont["registered"] = True
            ont["line_profile_id"] = int(args.split(" ")[5])
            ont["srv_profile_id"] = int(args.split(" ")[7])
            ont["description"] = args.split(" ")[-1]
            ont["control_flag"] = "active"
            ont["run_state"] = "online"
            ont["config_state"] = "normal"
            ont["match_state"] = "match"
            ont["management_mode"] = "OMCI"
            for o in onts:
                if o["sn"] == ont["sn"]:
                    self.configurations["frames"][0]["slots"][0]["ports"][port][onts.index(o)] = ont
                    break
            return self.render("huawei_smartax/ont_add_successful.j2", port=port, ont=ont)
        return ""

    def _find_ont(self, onts: List[Dict], sn: str) -> Dict:
        """ Find an ONT in the onts list """
        return next((item for item in onts if item.get('sn') == sn), None)

    def make_commit(self, **kwargs):
        """ Commit the changes """
        self.configurations = copy.deepcopy(self.changing_config)
        self.changing_config = None
        return ""

commands = {
    "enable": {
        "output": None,
        "new_prompt": ENABLE_PROMPT,
        "help": "enter exec prompt",
        "prompt": INITIAL_PROMPT,
    },
    "config": {
        "output": None,
        "new_prompt": CONFIG_PROMPT,
        "help": "enter configuration mode",
        "prompt": ENABLE_PROMPT,
    },
    "display sysuptime": {
        "output": HuaweiSmartAX.make_display_sysuptime,
        "regex": "di[[splay]] sys[[uptime]]",
        "help": "Display the system uptime",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT, CONFIG_PROMPT],
    },
    "display board": {
        "output": HuaweiSmartAX.make_display_board,
        "regex": "di[[splay]] boa[[rd]] \\S+",
        "help": "display board information",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT, CONFIG_PROMPT],
    },
    "display ont info": {
        "output": HuaweiSmartAX.make_display_onts,
        "regex": "di[[splay]] ont inf[[o]] \\S+",  # display ont info 0/2/0
        "help": "display ont information",
        "prompt": [
            INITIAL_PROMPT,
            ENABLE_PROMPT,
            CONFIG_PROMPT,
            CONFIG_IF_GPON,
        ],
    },
    "display sysman service state": {
        "output": HuaweiSmartAX.make_display_sysman_service_state,
        "help": "It shows the state of the running services",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT],
    },
    "display dba-profile": {
        "output": HuaweiSmartAX.make_display_dba__profile,
        "regex": "di[[splay]] db[[a-profile]] \\S+",
        "help": "Displays all the DBA profiles.",
        "prompt": [CONFIG_PROMPT],
    },
    "dba-profile add": {
        "output": HuaweiSmartAX.make_dba__profile_add,
        "regex": "dba-profile add \\S+",
        "help": "Adds a DBA profile with the corresponding parameters.",
        "prompt": [CONFIG_PROMPT],
    },
    "display ont autofind": {
        "output": HuaweiSmartAX.make_display_ont_autofind,
        "regex": "di[[splay]] ont autof[[ind]] \\S+",
        "help": "Displays the ONT autofind information.",
        "prompt": [CONFIG_PROMPT, CONFIG_IF_GPON],
    },
    "quit": {
        "output": HuaweiSmartAX.make_quit,
        "help": "Exit the current level of the CLI",
        "prompt": [
            INITIAL_PROMPT,
            ENABLE_PROMPT,
            CONFIG_PROMPT,
            CONFIG_IF_GPON,
            CONFIG_GPON_LINEPROFILE,
            CONFIG_GPON_SRVPROFILE,
        ],
    },
    "ont-srvprofile": {
        "output": HuaweiSmartAX.make_ont__srvprofile,
        "regex": "ont-srvprof[[ile]] \\S+",
        "help": "Return the ONT service profile based on the profile id.",
        "prompt": [CONFIG_PROMPT],
    },
    "ont-port": {
        "output": HuaweiSmartAX.make_ont__port,
        "regex": "ont-port \\S+",
        "help": "Configure the service profile for the ONT ports.",
        "prompt": CONFIG_GPON_SRVPROFILE,
    },
    "port vlan": {
        "output": HuaweiSmartAX.make_port_vlan,
        "regex": "port vlan \\S+",
        "help": "Configure the VLAN for the port.",
        "prompt": CONFIG_GPON_SRVPROFILE,
    },
    "ont-lineprofile": {
        "output": HuaweiSmartAX.make_ont__lineprofile,
        "regex": "ont-lineprof[[ile]] \\S+",
        "help": "Return the ONT line profile based on the profile id.",
        "prompt": CONFIG_PROMPT,
    },
    "tcont": {
        "output": HuaweiSmartAX.make_tcont,
        "regex": "tcont \\S+",
        "help": "Configure the T-CONT",
        "prompt": CONFIG_GPON_LINEPROFILE,
    },
    "gem add": {
        "output": HuaweiSmartAX.make_gem_add,
        "regex": "gem add \\S+",
        "help": "Add a GEM port",
        "prompt": CONFIG_GPON_LINEPROFILE,
    },
    "gem mapping": {
        "output": HuaweiSmartAX.make_gem_mapping,
        "regex": "gem mapping \\S+",
        "help": "Map a GEM port",
        "prompt": CONFIG_GPON_LINEPROFILE,
    },
    "commit": {
        "output": HuaweiSmartAX.make_commit,
        "help": "Commit the changes",
        "prompt": [CONFIG_IF_GPON, CONFIG_GPON_SRVPROFILE, CONFIG_GPON_LINEPROFILE],
    },
    "interface gpon": {
        "output": HuaweiSmartAX.make_interface_gpon,
        "regex": "interf[[ace]] g[[pon]] \\S+",
        "help": "Configure the GPON interface",
        "prompt": CONFIG_PROMPT,
    },
    "ont add": {
        "output": HuaweiSmartAX.make_ont_add,
        "regex": "ont add \\S+",
        "help": "Add an ONT",
        "prompt": CONFIG_IF_GPON,
    },
    "display ont-lineprofile": {
        "output": HuaweiSmartAX.make_display_ont__lineprofile,
        "regex": "di[[splay]] ont-lineprof[[ile]] \\S+",
        "help": "Display the ONT line profile",
        "prompt": [CONFIG_PROMPT]
    }
}
