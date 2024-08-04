def parse_name_path(name_path: str) -> str:
    if not name_path.startswith("root:"):
        return name_path
    return "/root" + name_path.removeprefix("root:")
