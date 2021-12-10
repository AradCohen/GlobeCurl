import csv
import tqdm
from expressvpn_logic import *
import requests


def launch_globe_curl(url,
                      requests_per_location=1,
                      location_aliases_list=None,
                      random_locations_amount=None,
                      response_headers=None):

    csv_headers = ["request number", "ip", "response"]
    if response_headers is not None:
        csv_headers += response_headers
    results = []
    vpn_location_list = VpnList(location_aliases_list=location_aliases_list,
                                random_locations_amount=random_locations_amount)
    vpn_location_list_length = vpn_location_list.get_locations_amount()
    # TODO:
    # handle exceptions
    # add csv wrapper class
    # improve headers extraction mechanism

    total_request_idx = 0
    for (alias, country) in tqdm.tqdm(vpn_location_list.get_locations(), total=vpn_location_list_length):
        disconnect()

        connect_alias(alias)  # might raise a ConnectException.

        for same_request_idx in range(requests_per_location):
            total_request_idx += 1
            myip_check = requests.get("https://myip.wtf/json")
            myip_content = myip_check.text

            url_res = requests.get(url, allow_redirects=False)
            url_res_content = url_res.text

            request_info = [total_request_idx, myip_content, url_res_content]
            if response_headers is not None:
                important_response_headers = [url_res.headers[header] for header in response_headers]
                request_info += important_response_headers
            results.append(request_info)

    with open("out.csv", "w") as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(csv_headers)
        csv_writer.writerows(results)