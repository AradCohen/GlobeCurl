import pyfiglet
from expressvpn_logic import *
import argparse
from globe_curl import launch_globe_curl


def parse_arguments():
    parser = argparse.ArgumentParser(description='launch get request from around the world using expressvpn')
    parser.add_argument("url", metavar="URL", type=str, help="The URL you want to access")
    parser.add_argument("-n", "--number-of-requests-per-location", type=int, help="number of requests per location",
                        action="store", default=1)
    parser.add_argument("-l", "--locations-aliases", help="aliases of server to use", action="append")
    parser.add_argument("-r", "--random_locations_amount", help="amount of random vpn server to connect to", type=int)
    parser.add_argument("-H", "--headers", help="focus on specific header in the response", action="append")
    args = parser.parse_args()
    return args


def print_cool_ascii():
    pyfiglet.print_figlet("GlobeCurl")
    print("Welcome to GlobeCurl - the tool that let you launch requests from around the world using expressvpn!")


def main():
    print_cool_ascii()

    cmd_args = parse_arguments()
    cmd_args_dict = vars(cmd_args)

    if cmd_args_dict["locations_aliases"] is not None and cmd_args_dict["random_locations_amount"] is not None:
        print("You can't set both of random_locations_amount and locations_aliases!")
        exit(1)
        
    launch_globe_curl(cmd_args_dict["url"],
                      requests_per_location=cmd_args_dict["number_of_requests_per_location"],
                      location_aliases_list=cmd_args_dict["locations_aliases"],
                      random_locations_amount=cmd_args_dict["random_locations_amount"],
                      response_headers=cmd_args_dict["headers"])


if __name__ == '__main__':
    main()