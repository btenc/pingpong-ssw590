from app.database import add_endpoint, get_active_endpoints

add_endpoint("Example", "https://example.com")

for row in get_active_endpoints():
    print(dict(row))
