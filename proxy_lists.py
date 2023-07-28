# pip install requests
import requests

proxy_url = "http://x7U6TavjC6ICEeeQerlEXQ:@smartproxy.crawlbase.com:8012"
proxies = {"http": proxy_url, "https": proxy_url}

response = requests.get(url="http://httpbin.org/ip", proxies=proxies, verify=False)


# print the ip address and port of proxy using text and get only the ip address not include the origin using json
print(response.json()['origin'])
# copy the ip address and port to proxychains.conf
# with open('proxychains.conf', 'a') as config_file:
#     config_file.write(f"http {response.json()['origin']}\n")
#     print(f"Proxy: http://{response.json()['origin']}")







