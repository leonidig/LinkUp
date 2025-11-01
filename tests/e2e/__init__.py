def get_error_msgs(response):
    json_data = response.json()
    if response.status_code != 422 or "detail" not in json_data:
        raise ValueError(f"No validation errors in response: {json_data}")
    return [err["msg"] for err in json_data["detail"]]
