# GlobeCurl

  ____ _       _           ____           _ 
 / ___| | ___ | |__   ___ / ___|   _ _ __| |
| |  _| |/ _ \| '_ \ / _ \ |  | | | | '__| |
| |_| | | (_) | |_) |  __/ |__| |_| | |  | |
 \____|_|\___/|_.__/ \___|\____\__,_|_|  |_|


GlobeCurl lets you run curl from around the globe with expressvpn

## Examples:
Running GlobeCurl from 5 random locations:
 
 ```sh
 python3.8 main.py http://google.com -r 5
```

Running GlobeCurl with specific locations - concatinating -l flags (aliases given by "expressvpn list"):

```sh
python3.8 main.py https://youtube.com -n 1 -l smart -l by -l ad -l mt -l usny
```

GlobeCurl creates a csv file for the results


