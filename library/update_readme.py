import os
import sys


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python update_readme.py <component_type> <component_name> <component_desc>"
        )
        sys.exit(1)

    component_type = sys.argv[1]  # 'service' or 'library'
    component_name = sys.argv[2]
    component_desc = (
        sys.argv[3] if len(sys.argv) > 3 else f"Source code of the {component_name}."
    )

    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"Warning: {readme_path} not found. Cannot append to package list.")
        sys.exit(0)

    if component_type == "service":
        entry = f"* `{component_name}`: {component_desc}\n"
        marker = "<!-- COPIER_SERVICES_END -->"
        fallback_str = "List of our services:"
    else:
        # For libraries, we namespace them as shared.xxx typically but the user specifies name
        entry = f"* `shared.{component_name}`: {component_desc}\n"
        marker = "<!-- COPIER_LIBRARIES_END -->"
        fallback_str = "List of our libraries:"

    with open(readme_path, "r") as f:
        content = f.read()

    if entry in content:
        sys.exit(0)

    if marker in content:
        content = content.replace(marker, f"{entry}{marker}")
        with open(readme_path, "w") as f:
            f.write(content)
    else:
        # Fallback: append to the end of the List of our packages
        search_str = fallback_str
        if search_str in content:
            parts = content.split(search_str)
            lines = parts[1].split("\n\n")[0]  # The list block
            new_lines = lines + "\n" + entry
            parts[1] = parts[1].replace(lines, new_lines)
            with open(readme_path, "w") as f:
                f.write(search_str.join(parts))


if __name__ == "__main__":
    main()
