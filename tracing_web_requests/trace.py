"""
A script to obtain the path of web requests
"""

import json
import re
import subprocess

WEBSITES = [
    'www.google.co.uk',
    'www.google.com',
    'www.youtube.com',
    'en.wikipedia.org',
    'www.yahoo.com',
    'www.reddit.com',
    'www.amazon.com',
    'www.amazon.co.uk',
    'twitter.com',
    'www.instagram.com',
    'www.facebook.com',
    'uk.linkedin.com',
    'www.netflix.com',
    'imgur.com',
    'www.ebay.co.uk',
    'www.ebay.com',
    'www.pornhub.com',
    'wordpress.com',
    'stackoverflow.com',
    'www.twitch.tv',
    'xhamster.com',
    'www.blogger.com',
    'www.imdb.com',
    'github.com',
    'www.pinterest.com',
    'www.paypal.com',
    'www.bbc.co.uk',
    'london.craigslist.co.uk',
    'www.craigslist.com',
    'www.quora.com',
    'www.dailymail.co.uk',
    'www.samsung.com',
    'www.apple.com',
    'www.bing.com',
    'www.msn.com',
    'www.gmail.com',
    'outlook.live.com',
    'www.baidu.com',
]

trace_list = []
regex = re.compile('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')

for website in WEBSITES:
    print(website)
    result = subprocess.run(['tracert', f'{website}'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').replace('\r', '')
    lines = result.split('\n')
    ip_list = []
    for line in lines:
        if line:
            ip = regex.findall(line)
            if ip:
                if len(ip) == 1:
                    print(ip)
                    ip_list.append(ip[0])
                else:
                    print(f'{website} had multiple IPs: {ip}')
    if ip_list:
        trace_list.append(
            {
                'website': website,
                'ips': ip_list
            }
        )
    else:
        print(f'No IPs extracted for site: {website}')

with open('website_ip_trace.json', 'w') as out_json:
    json.dump(trace_list, out_json)
