import os
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_compose.py <service_name>")
        sys.exit(1)

    service_name = sys.argv[1]
    compose_path = "docker-compose.yaml"

    if not os.path.exists(compose_path):
        print(
            f"Warning: {compose_path} not found in current directory. Cannot append include."
        )
        sys.exit(0)

    include_entry = f"  - projects/{service_name}/docker-compose.yml\n"

    with open(compose_path, "r") as f:
        content = f.read()

    if include_entry in content:
        sys.exit(0)

    with open(compose_path, "a") as f:
        if "\ninclude:" not in content and not content.startswith("include:"):
            f.write("\ninclude:\n")
        f.write(include_entry)


if __name__ == "__main__":
    main()
