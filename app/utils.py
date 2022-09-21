from typing import Any, Dict


def parse_user_attributes(client_response: Dict[Any, Any]) -> Dict[str, str]:
    response = {}
    if "UserAttributes" in client_response:
        for item_dict in client_response["UserAttributes"]:
            response[item_dict["Name"]] = item_dict["Value"]
    return response
