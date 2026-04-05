import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000/api"


def send(method, url, data=None):
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            text = resp.read().decode()
            return status, json.loads(text) if text else None
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        return e.code, json.loads(text) if text else None


def show(label, status, body):
    print(f"\n--- {label} ---")
    print(f"Status: {status}")
    if body:
        print(json.dumps(body, indent=2))
    else:
        print("(no body)")


print("=" * 50)
print("  Django REST API — Manual Endpoint Tests")
print("=" * 50)


s, r = send("POST", f"{BASE}/users/", {"name":"Rahul Sharma","email":"rahul@demo.com","bio":"Developer","location":"Mumbai","age":25})
show("POST /api/users/ — Create user 1", s, r)
user1_id = r['id'] if r else 1

s, r = send("POST", f"{BASE}/users/", {"name":"Priya Patel","email":"priya@demo.com","bio":"Designer","location":"Delhi","age":28})
show("POST /api/users/ — Create user 2", s, r)

s, r = send("POST", f"{BASE}/users/", {"name":"Amit Kumar","email":"amit@demo.com","bio":"Student","location":"Mumbai","age":22})
show("POST /api/users/ — Create user 3", s, r)
user3_id = r['id'] if r else 3


s, r = send("GET", f"{BASE}/users/")
show("GET /api/users/ — List all", s, r)


s, r = send("GET", f"{BASE}/users/?location=Mumbai")
show("GET /api/users/?location=Mumbai — Filter", s, r)

s, r = send("GET", f"{BASE}/users/?name=Priya")
show("GET /api/users/?name=Priya — Filter by name", s, r)


s, r = send("GET", f"{BASE}/users/{user1_id}/")
show(f"GET /api/users/{user1_id}/ — Retrieve single", s, r)


s, r = send("PUT", f"{BASE}/users/{user1_id}/", {"name":"Rahul Sharma","email":"rahul@demo.com","bio":"Senior developer now","location":"Pune","age":26})
show(f"PUT /api/users/{user1_id}/ — Full update", s, r)

# PARTIAL UPDATE (PATCH)
s, r = send("PATCH", f"{BASE}/users/{user1_id}/", {"bio":"Lead engineer"})
show(f"PATCH /api/users/{user1_id}/ — Partial update", s, r)


s, r = send("POST", f"{BASE}/users/", {"name":"Bad","email":"bad@demo.com","age":-10})
show("POST /api/users/ — Validation error (age=-10)", s, r)


s, r = send("DELETE", f"{BASE}/users/{user3_id}/")
show(f"DELETE /api/users/{user3_id}/ — Delete user", s, r)


s, r = send("GET", f"{BASE}/users/")
show("GET /api/users/ — After delete", s, r)


s, r = send("GET", f"{BASE}/users/9999/")
show("GET /api/users/9999/ — Not found", s, r)

print("\n" + "=" * 50)
print("  All tests complete")
print("=" * 50)
