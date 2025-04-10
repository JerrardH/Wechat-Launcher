import time
from pywinauto.application import Application
from pywinauto.timings import TimeoutError


def open_and_close_wechat():
    # Replace with your actual WeChat executable path
    wechat_path = r"C:\Program Files\Tencent\WeChat\WeChat.exe"

    # Start WeChat
    app = Application(backend="uia").start(wechat_path)

    # Wait for the login window to appear
    login_window = app.window(title_re="WeChat|微信")
    login_window.wait("visible", timeout=20)

    # Click the green "进入微信" button (if found)
    try:
        login_window.child_window(
            title="进入微信", control_type="Button"
        ).click_input()
    except:
        print("Could not find the '进入微信' button. Check control identifiers.")
        return

    # Now we want to actively wait for the main WeChat window to appear
    # after the user logs in (scan QR code, etc.).
    print("Waiting for the main WeChat window to appear...")
    main_window = app.window(title_re="WeChat|微信")

    try:
        # Wait up to 60 seconds for the main window to become visible
        main_window.wait("visible", timeout=60)
    except TimeoutError:
        print("Main WeChat window did not appear within 60 seconds. Exiting.")
        return

    print("Main window is now visible. Attempting to close WeChat...")

    # Attempt to click the "X" button
    try:
        main_window.child_window(title="Close", control_type="Button").click_input()
    except:
        print("Could not 'X' (Close) button. Trying main_window.close() instead.")
        main_window.close()

    print("WeChat has been closed.")


if __name__ == "__main__":
    open_and_close_wechat()
