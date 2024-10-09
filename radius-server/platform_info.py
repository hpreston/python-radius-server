authentication_attributes = {
    "cisco-ios": {
        "Cisco-AVPair": "shell:priv-lvl={role}",
    }, 
    "cisco-nexus": {
        "Cisco-AVPair": 'shell:roles="{role}"',
    }
}

role_mapping = {
    "cisco-ios": {
        "administrator": "15", 
        "operator": "1",
    },
    "cisco-nexus": {
        "administrator": "network-admin", 
        "operator": "network-operator",
    }
}
