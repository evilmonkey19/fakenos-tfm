"""
NOS module for Huawei SmartAX
"""

# import time
# import os
import copy

import os
from typing import Dict, List
from fakenos.plugins.nos.platforms_py.base_template import BaseDevice


NAME: str = "huawei_smartax"
INITIAL_PROMPT: str = "{base_prompt}>"
ENABLE_PROMPT: str = "{base_prompt}#"
CONFIG_PROMPT: str = "{base_prompt}(config)#"
DEVICE_NAME: str = "HuaweiSmartAX"

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
    "Bind times": ("right", len(max("Bind", "times", "1" "10", key=len))),
}

class HuaweiSmartAX(BaseDevice):
    """
    Class that keeps track of the state of the Huawei SmartAX device.
    """
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
    
    def make_display_board(self, base_prompt, current_prompt, command):
        """
        Return String of board informationc
        
        Example:
            -------------------------------------------------------------------------
            SlotID  BoardName  Status          SubType0  SubType1  Online/Offline
            -------------------------------------------------------------------------
            0       A123ABCD   Normal                                            
            1                                                                    
            2       A123ABCD   Normal                                            
            3       A123ABCD   Active_normal   CPCF                              
            4       A123ABCD   Standby_failed  CPCF                Offline       
            5                                                                    
            -------------------------------------------------------------------------
        """
        titles = ["SlotID", "BoardName", "Status", "SubType0", "SubType1", "Online/Offline"]
        titles: dict = {title:keyword for title, keyword in zip(titles, self._get_keywords(titles))}
        boards = [*copy.deepcopy(self.configurations["frames"][0]["slots"])]
        for title, keyword in titles.items():
            board_column = [board[keyword] for board in boards]
            results = self._add_whitespaces_column([title] + board_column, FRAME_SPACING)
            board_column = results[1:]
            titles[title] = results[0]
            for board in boards:
                board[keyword] = board_column[boards.index(board)]
        return self.render("huawei_smartax/display_board.j2", titles=titles.values(), boards=boards)

    def make_display_onts(self, base_prompt, current_prompt, command):
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
        titles_table_1 = ["F/S/P", "ONT ID", "SN", "Control flag", "Run state", "Config state", "Match state", "Protect side"]
        titles_table_2 = ["F/S/P", "ONT-ID", "Description"]
        titles_table_1 = {title:keyword for title, keyword in zip(titles_table_1, self._get_keywords(titles_table_1))}
        titles_table_2 = {title:keyword for title, keyword in zip(titles_table_2, self._get_keywords(titles_table_2))}
        frame = copy.deepcopy(self.configurations["frames"][0])
        board = next((board for board in frame["slots"] if board["boardname"] == "H901GPSFE"), None)
        position = frame["slots"].index(board) if board else None
        onts = board["ports"][0]
        port = f"0/ {position}/0"
        for ont in onts:
            ont["f_s_p"] = port
            ont["ont-id"] = ont["ont_id"]
        for title, keyword in titles_table_1.items():
            onts_column = [ont[keyword] for ont in onts]
            results = self._add_whitespaces_column([title] + onts_column, FRAME_SPACING)
            onts_column = results[1:]
            titles_table_1[title] = results[0]
            for ont in onts:
                ont[keyword] = onts_column[onts.index(ont)]
        for title, keyword in titles_table_2.items():
            onts_column = [ont[keyword] for ont in onts]
            results = self._add_whitespaces_column([title] + onts_column, FRAME_SPACING)
            onts_column = results[1:]
            titles_table_2[title] = results[0]
            for ont in onts:
                ont[keyword] = onts_column[onts.index(ont)]
        return self.render("huawei_smartax/display_ont_info_list.j2", port=port, onts=onts)

    def make_display_sysman_service_state(self, base_prompt, current_prompt, command):
        """ Return the sysman service state information """
        services = copy.deepcopy(self.configurations["services"])
        titles = ["Network service", "Port", "State"]
        titles: dict = {title:keyword for title, keyword in zip(titles, self._get_keywords(titles))}
        for title, keyword in titles.items():
            services_column = [service[keyword] if service[keyword] is not None else "----" for service in services]
            results = self._add_whitespaces_column([title] + services_column, SERVICES_SPACING)
            services_column = results[1:]
            titles[title] = results[0]
            for service in services:
                service[keyword] = services_column[services.index(service)]
        return self.render("huawei_smartax/display_sysman_service_state.j2", titles=list(titles.values()), services=services)

    def make_dba__profile_add_profile__name(self, base_prompt, current_prompt, command):
        """ Adds a DBA profile with the corresponding parameters. """
        return self.render("huawei_smartax/dba__profile_add_profile__name.j2")
    
    def make_display_dba__profile_all(self, base_prompt, current_prompt, command):
        """ Displays all the DBA profiles. """
        dba_profiles = self.configurations["dba_profiles"]
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
    
    def make_display_dba__profile_profile__name(self, base_prompt, current_prompt, command):
        """ Displays one DBA profile based on the name. """
        dba_profile = self.configurations["dba_profiles"][-1]
        return self.render("huawei_smartax/display_dba__profile_profile__name.j2", **dba_profile)

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
    "display board": {
        "output": HuaweiSmartAX.make_display_board,
        "help": "display board information",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT],
    },
    "display ont info 0/2/0": {
        "output": HuaweiSmartAX.make_display_onts,
        "help": "display ont information",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT],
    },
    "display sysman service state": {
        "output": HuaweiSmartAX.make_display_sysman_service_state,
        "help": "It shows the state of the running services",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT],
    },
    "display dba-profile all": {
        "output": HuaweiSmartAX.make_display_dba__profile_all,
        "help": "Displays all the DBA profiles.",
        "prompt": [CONFIG_PROMPT],
    },
    "display dba-profile profile-name DBA_100M": {
        "output": HuaweiSmartAX.make_display_dba__profile_profile__name,
        "help": "Displays one DBA profile based on the name.",
        "prompt": [CONFIG_PROMPT],
    },
    "dba-profile add profile-name DBA_100M type3 assure 102400 max 102400": {
        "output": HuaweiSmartAX.make_dba__profile_add_profile__name,
        "help": "Adds a DBA profile with the corresponding parameters.",
        "prompt": [CONFIG_PROMPT],
    },
    "quit": {
        "output": True,
        "help": "Exit the current level of the CLI",
        "prompt": [INITIAL_PROMPT, ENABLE_PROMPT, CONFIG_PROMPT],
    },
}
