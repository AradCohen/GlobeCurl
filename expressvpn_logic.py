import subprocess
import random
from typing import List

VPN_CONNECT = 'expressvpn connect'

VPN_LIST = 'expressvpn list all'

VPN_DISCONNECT = 'expressvpn disconnect'


class ConnectException(Exception):
    pass


def run_command(command: str):
    """
    Runs the given command, opens a new process in order to achieve that
    :param command: the command to run
    :return: returns the output of the given command
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return list([str(v).replace('\\t', ' ').replace('\\n', ' ').replace('b\'', '').replace('\'', '')
                .replace('b"', '')
                 for v in iter(p.stdout.readline, b'')])


def activation_check():
    """
    Checks if the user has already activated his account
    :return: exits if the user didn't activate his expressvpn account
    """
    print('Checking if the client is activated... (Please wait)')
    out = connect()
    if not is_activated(out):
        print('Please run <expressvpn activate> and provide your activation key. Program will exit.')
        exit(1)
    print('Client is successfully logged in.')
    disconnect()


def connect():
    """
    runs the "expressvon connect" command, used to check if the user has activated his expressvpn account.
    :return: the output of the "expressvpn" command
    """
    return run_command(VPN_CONNECT)


def disconnect():
    """
    disconnects from a server
    :return:
    """
    return run_command(VPN_DISCONNECT)


def is_activated(connect_output):
    """
    checks if the user has already activated his expressvpn account
    :param connect_output: the output of the command "expressvpn connect"
    :return: Ture if the user has activated his account, False otherwise
    """
    return not check_if_string_is_in_output(connect_output, 'Please activate your account')


def check_if_string_is_in_output(out, string) -> bool:
    """
    performs a substring check, in order to parse a command output
    :param out: list of strings, represents a command's output
    :param string: the functions checks if this string appears in one of the the strings in the given list
    :return: boolean
    """
    for item in out:
        if string in item:
            return True
    return False


def connect_alias(alias: str):
    """
    connects to a given vpn server's location
    :param alias: string that represents the vpn server location
    """
    command = VPN_CONNECT + ' ' + str(alias)
    out = run_command(command)
    if check_if_string_is_in_output(out, 'We were unable to connect to this VPN location'):
        raise ConnectException()
    if check_if_string_is_in_output(out, 'not found'):
        raise ConnectException()
    # print('Successfully connected to {}'.format(alias))


def extract_aliases(vpn_list):
    """
    extracts the aliases from the 'vpn list' command, the output from this command is in the following form:
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    :param vpn_list: output of the "vpn list" command
    :return:
    """
    aliases = []
    for vpn_item in vpn_list[2:]:
        location_line_after_split = vpn_item.split()
        alias = location_line_after_split[0]
        country = location_line_after_split[1]
        aliases.append((alias, country))
    return aliases


class VpnList:
    """
    represents a vpn servers' locations for the user
    """
    # static constructor (anything in the class definition will be executed once):
    vpn_list = run_command(VPN_LIST)
    _all_locations = extract_aliases(vpn_list)
    _alias_to_country_dct = {k: v for (k, v) in _all_locations}

    def __init__(self, location_aliases_list: List[str] = None,
                 random_locations_amount: int = None) -> None:
        super().__init__()

        if location_aliases_list is not None:
            self._locations_for_user = [(alias, self._alias_to_country_dct[alias]) for alias in location_aliases_list]

        elif random_locations_amount is not None:
            all_locations_copy = self._all_locations[:]
            random.shuffle(all_locations_copy)
            self._locations_for_user = all_locations_copy[:random_locations_amount]

        else:
            self._locations_for_user = self._all_locations[:]

    def get_locations_amount(self):
        return len(self._locations_for_user)

    def get_locations(self):
        for alias, country in self._locations_for_user:
            yield alias, country
