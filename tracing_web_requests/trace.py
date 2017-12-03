import re
import subprocess

WEBSITES = [
    'www.google.co.uk',
    'www.reddit.com'
]

regex = re.compile('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')

for website in WEBSITES:
    print(website)
    result = subprocess.run(['tracert', f'{website}'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').replace('\r', '')
    lines = result.split('\n')
    for line in lines:
        # print(line)
        if line:
            print(regex.findall(line))