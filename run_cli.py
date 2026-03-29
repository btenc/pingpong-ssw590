from app.checker import check_all_active_endpoints
from app.database import (
    add_endpoint,
    create_tables,
    delete_endpoint,
    get_all_endpoints,
    get_endpoint_by_id,
    get_recent_checks,
    update_endpoint,
)


def main():
    create_tables()

    while True:
        print("\n1 add")
        print("2 list")
        print("3 edit")
        print("4 del")
        print("5 check")
        print("6 recent")
        print("7 quit")

        choice = input("> ").strip()

        if choice == "1":
            name = input("name: ").strip()
            url = input("url: ").strip()

            if not name or not url:
                print("missing")
                continue

            add_endpoint(name, url)
            print("ok")

        elif choice == "2":
            endpoints = get_all_endpoints()

            if not endpoints:
                print("none")
                continue

            for endpoint in endpoints:
                print(
                    endpoint["id"],
                    endpoint["name"],
                    endpoint["url"],
                    endpoint["is_active"],
                )

        elif choice == "3":
            endpoint_id_text = input("id: ").strip()

            if not endpoint_id_text:
                print("missing")
                continue

            try:
                endpoint_id = int(endpoint_id_text)
            except ValueError:
                print("bad id")
                continue

            endpoint = get_endpoint_by_id(endpoint_id)
            if endpoint is None:
                print("not found")
                continue

            name = input(f"name [{endpoint['name']}]: ").strip()
            url = input(f"url [{endpoint['url']}]: ").strip()

            if not name:
                name = endpoint["name"]
            if not url:
                url = endpoint["url"]

            update_endpoint(endpoint_id, name, url)
            print("ok")

        elif choice == "4":
            endpoint_id_text = input("id: ").strip()

            if not endpoint_id_text:
                print("missing")
                continue

            try:
                endpoint_id = int(endpoint_id_text)
            except ValueError:
                print("bad id")
                continue

            endpoint = get_endpoint_by_id(endpoint_id)
            if endpoint is None:
                print("not found")
                continue

            confirm = input(f"del {endpoint['name']}? y/n: ").strip().lower()

            if confirm == "y":
                delete_endpoint(endpoint_id)
                print("ok")
            else:
                print("no")

        elif choice == "5":
            results = check_all_active_endpoints()

            if not results:
                print("none")
                continue

            for result in results:
                print()
                print(result["endpoint_name"])
                print(result["endpoint_url"])
                print(result["status_code"])
                print(result["response_time_ms"])
                print(result["success"])
                print(result["error_message"])

        elif choice == "6":
            checks = get_recent_checks(limit=20)

            if not checks:
                print("none")
                continue

            for check in checks:
                print()
                print(check["id"])
                print(check["endpoint_name"])
                print(check["status_code"])
                print(check["response_time_ms"])
                print(check["success"])
                print(check["error_message"])
                print(check["checked_at"])

        elif choice == "7":
            break

        else:
            print("bad")


if __name__ == "__main__":
    main()
