import csv
import subprocess
import requests
import tqdm

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


def get_all_vpn_locations():
    """
    extracts all the available vpn servers
    """
    vpn_list = run_command(VPN_LIST)
    locations = extract_aliases(vpn_list)

    for location in locations:
        yield location


def get_vpn_locations(location_aliases_list):
    """
    retrieves list of vpn servers in one of 3 ways:
    1.user's specific locations
    2.all the vpn locations
    3.TODO random locations (in case the user specified only the amount of locations)
    :param location_aliases_list: list of user's locations
    :return: generator of vpn servers' locations
    """
    if location_aliases_list:
        for location_alias in location_aliases_list:
            yield location_alias, ""
    else:
        for location in get_all_vpn_locations():
            yield location


def launch_globe_curl(url, requests_per_location=1, location_aliases_list=None):

    csv_headers = ["request number", "ip", "response"]
    results = []
    if location_aliases_list is None:
        location_aliases_list = []
    # TODO:
    # handle exceptions
    # add csv command line args
    # add headers extraction mechanism

    total_request_idx = 0
    # TODO: add total argument to tqdm
    for (alias, country) in tqdm.tqdm(get_vpn_locations(location_aliases_list)):
        disconnect()

        # print('Connecting to : {}({})'.format(country, alias))
        connect_alias(alias)  # might raise a ConnectException.

        for same_request_idx in range(requests_per_location):
            total_request_idx += 1
            myip_check = requests.get("https://myip.wtf/json")
            myip_content = myip_check.text

            url_res = requests.get(url, allow_redirects=False)
            url_res_content = url_res.text

            request_info = [total_request_idx, myip_content, url_res_content]
            results.append(request_info)

    with open("out.csv", "w") as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(csv_headers)
        csv_writer.writerows(results)


