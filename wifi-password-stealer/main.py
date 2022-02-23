import subprocess

networks_output = subprocess.getoutput("netsh wlan show profile")

networks_output = networks_output.split('\n')  # split by newlines


# cleaner function, sorts out only strings that have ':' in them
def cleaner_function(item):
    if ':' in item:
        return item


# applying the cleaner function
networks = list(map(cleaner_function, networks_output))
networks = [x for x in networks if x is not None]  # getting rid of None 
networks.pop(0)  # the first one we don't need.


def string_reduce(string):
    return string[string.rfind(":") + 2:]


networks = list(map(string_reduce, networks))

passwords = []

for network in networks:

    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', network, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
    results = [x for x in results if x is not None]
    pwd = string_reduce(results[-3])
    passwords.append(pwd)
    
for index in range(len(passwords)):
    print(networks[index], ': ', passwords[index])
    