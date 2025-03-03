import requests

def get_jsonplaceholder_data(endpoint="posts/1"):
    url = f"https://jsonplaceholder.typicode.com/{endpoint}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

# Example usage
data = get_jsonplaceholder_data()
print(data)
