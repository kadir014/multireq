# multireq ✈️
multireq is a Python module for sending multiple requests simultaneously. See [dependencies](#Dependencies) and [reference](#Reference) if you will use this module.

## Usage
```py
from multireq import Request, RequestPool

requests = [
            Request("https://site1.com"),
            Request("https://site2.com"),
            ...
           ]

rp = RequestPool(requests)

responses = rp.start_and_wait()
```

## Reference
### Request
`class Request(url, method, headers=None, data=None)`
- **Arguments:**
  - `url    -> str`  : The URL request will be sent to
  - `method -> str`  : Method of request, `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD` or `OPTIONS`
  - `data   -> dict` : Dictionary or list of tuples to send in the body of the request

### Response
`class Response()`\
Found in [`ResponseList`](#ResponseList) returned by [`RequestPool`](#RequestPool)
- **Attributes:**
  - `succesful -> bool` : Whether the request was succesful or not
  - `code      -> int`  : Code of HTTP status
  - `reason    -> str`  : Textual reason of responded HTTP status
  - `content   -> bytes`: Content of the response
  - `text      -> str`  : Content of the response
  - `headers   -> dict` : Dictionary of response headers
  - `cookies   -> CookieJar` : `requests.cookies.RequestsCookieJar` object of Cookies

### ResponseList
`class ResponseList()`\
Returned by [`RequestPool`](#RequestPool). You can use `len()` to see length of the list and get elements by index.
- **Attributes:**
  - `elapsed -> ElapsedTime` : [`ElapsedTime`](#ElapsedTime)object of elapsed time during sending requests
  - `get_successful(first=False)` : Returns succesful responses. Returns the first encountered one if `first` is True
  - `get_failed(first=False)` : Returns failed responses. Returns the first encountered one if `first` is True
  - `get_by_code(first=False)` : Returns responses with matched codes. Returns the first encountered one if `first` is True
  - `get_by_url(first=False)` : Returns responses with matched URLs. Returns the first encountered one if `first` is True

### RequestPool
`class RequestPool(request_list, group_limit=10, timeout_limit=5)`
- **Arguments:**
  - `request_list  -> list` : List of [Request](#Request) objects
  - `group_limit   -> int` : Limit of grouping
  - `timeout_limit -> float`: Timeout limit for requests\
- **Attributes**
  - `start_and_wait()` : Starts sending requests and returns [ResponseList](#ResponeList)
  - `running -> bool` : If pool is currently sending requests

### ElapsedTime
`class ElapsedTime()`
- **Attributes**
  - `micros -> int` : Elapsed time in microseconds
  - `millis -> int` : Elapsed time in milliseconds
  - `secs -> float` : Elapsed time in seconds
  - `mins -> float` : Elapsed time in minutes
  - `hours -> float` : Elapsed time in hours
  - `days -> float` : Elapsed time in days

---

## Dependencies
- [requests](https://pypi.org/project/requests/)

## Todo
- [ ] Proxy support
- [ ] Better request coverage (cookies, auth, etc...)
- [ ] Test for optimizations

## License
[MIT](LICENSE) © Kadir Aksoy
