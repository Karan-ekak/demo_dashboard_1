def gen_repo():
    import requests
    import json

    # Set the authorization header
    headers = {"Authorization":  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6Im51bWFuIn0.heaQilFsyWuk4rrljvtkc7wYR8PzvQKMfCjZJFZXRP0"}

    # Set the request body


    # Make the request
    # response = requests.post("http://127.0.0.1:5000/protected", headers=headers, data=data)
    response =  requests.get("http://127.0.0.1:5000/report_generate/1002/365", headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful.
        print(response.content)
        return 'true'
        # print(json.loads(response.content))
    else:
        # The request failed.
        print("Status Code Failed")
        print(response.status_code)
        return 'false'