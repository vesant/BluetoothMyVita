import os
import sys


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    from bluetoothmyvita.main import main as app_main

    app_main()


if __name__ == "__main__":
    main()
