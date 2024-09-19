import json
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

api = API()
 
# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON data from the file
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
    return None

# Function to iterate through JSON data
async def iterate_json(data):
    proper=""
    if isinstance(data, dict):  # If the data is a dictionary (JSON object)
        for key, value in data.items():
            addition = f"{value}:"
            if key == "csrfCookie":
                addition = f"{value}:"
                proper += addition     
            elif key == "totpSecret":
                addition = f"{value}"
                proper += addition
                await api.pool.add_account(proper.split(":")[0], proper.split(":")[1], proper.split(":")[2], proper.split(":")[3], temp=proper.split(":")[4], mfa_code=proper.split(":")[5])
            else:
                proper += addition

            # print(f"Key: {key}, Value: {value}")
            if isinstance(value, (dict, list)):  # Recursively process nested objects or lists
                await iterate_json(value)
    elif isinstance(data, list):  # If the data is a list (JSON array)
        for index, item in enumerate(data):
            # print(f"Index {index}: {item}")
            if isinstance(item, (dict, list)):  # Recursively process nested objects or lists
                await iterate_json(item)

async def main():
    file_path = 'accounts.json'  # Replace with the path to your JSON file
    json_data = read_json_file(file_path)

    if json_data:
        await iterate_json(json_data)
    
    await api.pool.login_all()

if __name__ == "__main__":
    asyncio.run(main())  # Iterate through the JSON data