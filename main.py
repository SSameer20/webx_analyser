import requests
import socket
from bs4 import BeautifulSoup

url = "https://www.geeksforgeeks.org/"
hostname = url.split("//")[-1].split("/")[0]
ip_address = socket.gethostbyname(hostname)
isp = socket.gethostbyaddr(ip_address)[0]
domain = hostname.split(".")[-1]
subdomain = hostname.split(".")[0] if len(hostname.split(".")) > 1 else ""

 
# Make a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
  # Parse the HTML content
  soup = BeautifulSoup(response.content, "html.parser")

  # Find the meta tags
  meta_tags = soup.find_all("meta")

  # Extract the details from the meta tags
  for tag in meta_tags:
    if tag.has_attr("name") or tag.has_attr("property"):
      print(f"{tag['name'] if tag.has_attr('name') else tag['property']}: {tag['content']}")
  print(hostname)
  print(ip_address)
  print("ISP : " + isp)
  print(domain)
  print(subdomain)
else:
  print("Failed to get the website content")
