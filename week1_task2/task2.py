
import csv
import json
import os
import requests
from dotenv import load_dotenv

# 1. Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# 2. Read employees.csv
employees = []

with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        employees.append(row)

# 3. Save employee data to employees.json
with open("employees.json", "w") as file:
    json.dump(employees, file, indent=4)

# 4. Find high earners
high_earners = []

for employee in employees:
    if int(employee["salary"]) > 50000:
        high_earners.append(employee)

# 5. Save high earners to high_earners.csv
with open("high_earners.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=employees[0].keys()
    )
    writer.writeheader()
    writer.writerows(high_earners)

print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")


# 6. GET API users
url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(
        url,
        headers={"X-API-Key": API_KEY} if API_KEY else {},
        timeout=5
    )
    response.raise_for_status()

    users = response.json()

    # Print only the first user
    user = users[0]
    print(f'{user["id"]} - {user["name"]} - {user["email"]}')

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass


# 7. Check 404 status
url = "https://jsonplaceholder.typicode.com/users/9999"

try:
    response = requests.get(url, timeout=5)

    if response.status_code == 404:
        print("/users/9999 -> 404 Not found")
    else:
        response.raise_for_status()

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass


# 8. Extract nested JSON data and save users.json
url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    users = response.json()
    user_details = []

    for user in users:
        details = {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city"),
            "company": user.get("company", {}).get("name")
        }

        user_details.append(details)

    with open("users.json", "w") as file:
        json.dump(user_details, file, indent=4)

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass


# 9. Test timeout handling
url = "https://httpbin.org/delay/10"

try:
    response = requests.get(url, timeout=3)
    response.raise_for_status()

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass
