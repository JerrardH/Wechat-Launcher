import os
import time
import psutil
from pywinauto.application import Application
from pywinauto.timings import TimeoutError
from pywinauto.findwindows import ElementNotFoundError


def find_wechat_pid(preferred_paths):
    """
    Scan running processes for one whose executable path matches any of
    the preferred paths.
    """
    for proc in psutil.process_iter(['exe']):
        try:
            exe_path = proc.info['exe']
            if exe_path:
                normalized_exe = os.path.normpath(exe_path).lower()
                for candidate in preferred_paths:
                    if normalized_exe == os.path.normpath(candidate).lower():
                        return proc.pid
        except Exception:
            continue
    return None


def open_wechat():
    """
    Starts or connects to WeChat.

    1. Determines the available WeChat executable(s) from the known paths.
    2. Scans running processes to see if a genuine WeChat instance is already running.
       (This avoids connecting to, say, a file explorer window for Weixin.exe.)
    3. If found, connects to that instance; otherwise, it starts a new one.
    4. Waits (up to 10 seconds) for the login window to exist (regardless of focus).
       Then forces focus on that window.
    5. Finally, waits up to 60 seconds for the main window (post-login) to appear.

    Returns:
        app: The Application object if the main window appears successfully,
             otherwise None.
    """
    # Define the two possible executable paths.
    new_version_path = r"C:\Program Files\Tencent\Weixin\Weixin.exe"
    old_version_path = r"C:\Program Files\Tencent\WeChat\WeChat.exe"

    # Build a list of valid paths.
    preferred_paths = []
    if os.path.exists(new_version_path):
        preferred_paths.append(new_version_path)
    if os.path.exists(old_version_path):
        preferred_paths.append(old_version_path)

    if not preferred_paths:
        print("WeChat executable not found in expected paths.")
        return None

    # Try to locate an existing genuine WeChat process using its executable path.
    pid = find_wechat_pid(preferred_paths)
    if pid is not None:
        print(f"Connected to existing WeChat instance, PID: {pid}.")
        app = Application(backend="uia").connect(process=pid)
    else:
        # Otherwise, start a new instance using the first available executable.
        wechat_path = preferred_paths[0]
        print(f"Starting new WeChat instance at: {wechat_path}")
        app = Application(backend="uia").start(wechat_path)

    # Reference the login window using a broad title search.
    login_window = app.window(title_re="WeChat|微信|Weixin")

    # Wait up to 10 seconds for the login window to exist (even if not focused).
    start_time = time.time()
    while time.time() - start_time < 10:
        if login_window.exists():
            break
        time.sleep(0.1)
    else:
        print("Login window did not appear within 10 seconds.")
        return None
    print("Login window exists.")

    # Bring the login window to the foreground.
    try:
        login_window.set_focus()
        print("Login window is now focused.")
    except Exception:
        print("Failed to set focus to the login window, continuing anyway.")

    # Define the possible login button titles (supporting multiple languages).
    login_button_titles = ["进入微信", "登录", "Log In", "登入"]
    button_clicked = False

    # Attempt an immediate click.
    for title in login_button_titles:
        try:
            btn = login_window.child_window(title=title, control_type="Button")
            if btn.exists() and btn.is_visible():
                btn.click_input()
                print(f"Clicked the '{title}' button immediately after 5 seconds.")
                button_clicked = True
                break
        except Exception:
            continue

    # If the immediate click did not succeed, poll for up to 2 seconds.
    if not button_clicked:
        print("Initial click attempt failed; polling for login button for up to 2 more seconds...")
        poll_start = time.time()
        while time.time() - poll_start < 2:
            for title in login_button_titles:
                try:
                    btn = login_window.child_window(title=title, control_type="Button")
                    if btn.exists() and btn.is_visible():
                        btn.click_input()
                        print(f"Clicked the '{title}' button during polling.")
                        button_clicked = True
                        break
                except Exception:
                    continue
            if button_clicked:
                break
            time.sleep(0.1)

    if not button_clicked:
        print("Could not find or click the login button after additional polling.")
        return None

    # Wait for the main window to appear after login (up to 60 seconds).
    print("Waiting for the main WeChat window to appear...")
    main_window = app.window(title_re="WeChat|微信|Weixin")
    try:
        main_window.wait("visible", timeout=60)
    except TimeoutError:
        print("Main WeChat window did not appear within 60 seconds. Exiting.")
        return None
    print("Main window is now visible.")
    return app


def close_wechat(app):
    """
    Attempts to close the open WeChat application.

    Args:
        app: The Application object representing WeChat.
    """
    main_window = app.window(title_re="WeChat|微信|Weixin")
    print("Attempting to close WeChat...")
    try:
        main_window.child_window(title="Close", control_type="Button").click_input()
    except Exception:
        print("Could not click the 'Close' button. Trying main_window.close() instead.")
        main_window.close()
    print("WeChat has been closed.")


if __name__ == "__main__":
    app = open_wechat()
    if app is not None:
        close_wechat(app)
