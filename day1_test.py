import requests

# Fetch the main Remote OK page
url = "https://remoteok.com/remote-jobs"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Success! Downloaded the page.")
else:
    print(f"Error: {response.status_code}")
    
# Print first 500 characters of the HTML
print(response.text[:500])
