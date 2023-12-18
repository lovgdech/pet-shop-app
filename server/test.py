from http import cookies

# Create a cookie
cookie = cookies.SimpleCookie()
cookie["username"] = "john_doe"
cookie["username"]["expires"] = 3600  # Cookie will expire in 1 hour

# Set the cookie in the response headers
print(cookie)

# Get the cookies from the request headers
cookie_string = "username=john_doe; session_id=abc123"
received_cookies = cookies.SimpleCookie()
received_cookies.load(cookie_string)

# Access individual cookies
if "username" in received_cookies:
    username = received_cookies["username"].value
    print("Username:", username)
