import pyfiglet
from expressvpn_logic import *
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='launch get request from around the world using expressvpn')
    parser.add_argument("url", metavar="URL", type=str, help="The URL you want to access")
    parser.add_argument("-n", "--number-of-requests-per-location", type=int, help="number of requests per location",
                        action="store", default=1)
    parser.add_argument("-l", "--locations-aliases", help="aliases of server to use", action="append")
    args = parser.parse_args()
    return args


def print_cool_ascii():
    pyfiglet.print_figlet("GlobeCurl")


def main():
    print_cool_ascii()

    cmd_args = parse_arguments()
    cmd_args_dict = vars(cmd_args)

    launch_globe_curl(cmd_args_dict["url"],
                      requests_per_location=cmd_args_dict["number_of_requests_per_location"],
                      location_aliases_list=cmd_args_dict["locations_aliases"])


if __name__ == '__main__':
    main()