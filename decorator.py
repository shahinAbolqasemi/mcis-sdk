import functools


def request_url(url: str):
    def decorator(func: callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            formatted_url = url.format(**kwargs)
            return func(*args, **kwargs, url=formatted_url)

        return wrapper

    return decorator


# import requests
#
# url = "https://gw.ebcom.ir/service/auth/otp/otp/codeIncluded"
#
# payload = {"msisdn": "9123456789"}
# headers = {
#     "Accept": "application/json",
#     "prefer": "dynamic=false",
#     "Content-Type": "application/json",
#     "Authorization": "Bearer eyJ4NXQiOiJNell4TW1Ga09HWXdNV0kwWldObU5EY3hOR1l3WW1NNFpUQTNNV0kyTkRBelpHUXpOR00wWkdSbE5qSmtPREZrWkRSaU9URmtNV0ZoTXpVMlpHVmxOZyIsImtpZCI6Ik16WXhNbUZrT0dZd01XSTBaV05tTkRjeE5HWXdZbU00WlRBM01XSTJOREF6WkdRek5HTTBaR1JsTmpKa09ERmtaRFJpT1RGa01XRmhNelUyWkdWbE5nX1JTMjU2IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlZGFyaUBhbWVyYW5kaXNoLmNvbSIsImF1ZCI6ImtlMmp1bVNMdDY3VE5vWV9UVVFTN1d4MGZEZ2EiLCJuYmYiOjE2Mzg2MTcwMTgsImF6cCI6ImtlMmp1bVNMdDY3VE5vWV9UVVFTN1d4MGZEZ2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvbWNpLXN0YWdlMi5hcGljb25zb2xlLmlyOjQ0M1wvb2F1dGgyXC90b2tlbiIsImV4cCI6MTYzODYyMDYxOCwiaWF0IjoxNjM4NjE3MDE4LCJqdGkiOiI3ZTU3MzZlNi04M2QzLTRiZDYtOWFkOC1mZWI5MGU4Njc5MDAifQ.l3-kiDwtgzl_hxT0hGVSXTBjSGDNlefhVDGHq5OGHHEbWj5034tY4OCL6mMcdl7oCa3Wy7Qm8NzGlOF24jAHHpuuSnrQj-1aYzBzLu3xy1QG6BpYzfdTha5sndLoTCXpXCgYKsCQeEGzqiMIOjbEQ6t10mHVUiSYq8JNCzMpLYRy9nwn89YRcmDaGlGmV2rix4zMEUU3gZgZAl7cy6Sda5fuCsEx_WIrmLeRTnZCbTV9Wd8vqwVuAmmcVV8RqQArWgp1nM-aGVT02DadraZVaBm31KQzNwXlDOvzZ5RzJQs2HIY5DeygAwIFTGliWDlJjPIEJ3IR95EG6boDG5XFzA"
# }
#
# response = requests.request("POST", url, json=payload, headers=headers)
#
# print(response.text)
