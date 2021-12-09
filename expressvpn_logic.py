import subprocess
import requests


VPN_CONNECT = 'expressvpn connect'

VPN_LIST = 'expressvpn list all'

VPN_DISCONNECT = 'expressvpn disconnect'


class ConnectException(Exception):
    pass


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return list([str(v).replace('\\t', ' ').replace('\\n', ' ').replace('b\'', '').replace('\'', '')
                .replace('b"', '')
                 for v in iter(p.stdout.readline, b'')])


def activation_check():
    print('Checking if the client is activated... (Please wait)')
    out = connect()
    if not is_activated(out):
        print('Please run <expressvpn activate> and provide your activation key. Program will exit.')
        exit(1)
    print('Client is successfully logged in.')
    disconnect()


def connect():

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
    :param connect_output: the ouput of the command "expressvpn connect"
    :return: Ture if the user has activated his account, False otherwise
    """
    return not check_if_string_is_in_output(connect_output, 'Please activate your account')


def check_if_string_is_in_output(out, string):
    for item in out:
        if string in item:
            return True
    return False


def connect_alias(alias):
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
    print('Successfully connected to {}'.format(alias))


def extract_aliases(vpn_list):
    """
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    """
    aliases = []
    for vpn_item in vpn_list[2:]:
        splitted_location_line = vpn_item.split()
        alias = splitted_location_line[0]
        country = splitted_location_line[1]
        aliases.append((alias, country))
    return aliases


def get_all_vpn_locations():
    vpn_list = run_command(VPN_LIST)
    locations = extract_aliases(vpn_list)

    for location in locations:
        yield location


def get_vpn_locations(location_aliases_list):
    if location_aliases_list:
        for location_alias in location_aliases_list:
            yield (location_alias, "")
    else:
        for location in get_all_vpn_locations():
            yield location


def launch_globe_curl(url, requests_per_location=1, location_aliases_list=[]):

    for (alias, country) in get_vpn_locations(location_aliases_list):
        disconnect()
        print('Connecting to : {}({})'.format(country, alias))
        connect_alias(alias)  # might raise a ConnectException.
        for request_idx in range(requests_per_location):
            url_res = requests.get(url)

            print(url_res.text)

