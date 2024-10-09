import yaml

with open("network.yaml") as f:
    data = yaml.safe_load(f.read())
    users = data["users"]
    hosts = data["hosts"]


def authenticate_user(username, password):
    if username in users.keys():
        if users[username]["password"] == password:
            return "Success"
        else:
            return "Fail"
    else:
        return "User not found"
