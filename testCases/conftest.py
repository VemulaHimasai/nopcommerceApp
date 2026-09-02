import os
import subprocess
import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# =========================================================
# FIND FIREFOX MSIX EXECUTABLE
# =========================================================

def get_firefox_binary():

    # -----------------------------------------------------
    # Normal Firefox installation paths
    # -----------------------------------------------------

    normal_paths = [
        os.path.join(
            os.environ.get("PROGRAMFILES", ""),
            "Mozilla Firefox",
            "firefox.exe"
        ),

        os.path.join(
            os.environ.get("PROGRAMFILES(X86)", ""),
            "Mozilla Firefox",
            "firefox.exe"
        ),

        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs",
            "Mozilla Firefox",
            "firefox.exe"
        )
    ]

    for path in normal_paths:

        if os.path.isfile(path):

            print("Firefox executable found:")
            print(path)

            return path

    # -----------------------------------------------------
    # Microsoft Store / MSIX Firefox
    # -----------------------------------------------------

    try:

        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            (
                "$p=(Get-AppxPackage Mozilla.Firefox).InstallLocation; "
                "if ($p) { "
                "Get-ChildItem -Path $p -Recurse "
                "-Filter firefox.exe "
                "-ErrorAction SilentlyContinue | "
                "Select-Object -First 1 -ExpandProperty FullName "
                "}"
            )
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        firefox_path = result.stdout.strip()

        if firefox_path and os.path.isfile(firefox_path):

            print("Firefox MSIX executable found:")
            print(firefox_path)

            return firefox_path

    except Exception as e:

        print("Firefox MSIX detection failed:")
        print(
            type(e).__name__,
            str(e)
        )

    # -----------------------------------------------------
    # Firefox not found
    # -----------------------------------------------------

    raise FileNotFoundError(
        "Firefox executable was not found. "
        "Install Mozilla Firefox or verify the Firefox installation."
    )


# =========================================================
# BROWSER FIXTURE
# =========================================================

@pytest.fixture()
def setup(browser):

    # =====================================================
    # DOWNLOAD DIRECTORY
    # =====================================================

    download_dir = os.path.abspath(
        os.path.join(
            os.getcwd(),
            "downloads"
        )
    )

    os.makedirs(
        download_dir,
        exist_ok=True
    )

    print(
        "Download directory:",
        download_dir
    )

    # =====================================================
    # CHROME
    # =====================================================

    if browser == "chrome":

        options = webdriver.ChromeOptions()

        options.accept_insecure_certs = True

        # -------------------------------------------------
        # Disable proxy
        # -------------------------------------------------

        options.add_argument(
            "--proxy-server=direct://"
        )

        options.add_argument(
            "--proxy-bypass-list=*"
        )

        # -------------------------------------------------
        # Download settings
        # -------------------------------------------------

        prefs = {

            "download.default_directory":
                download_dir,

            "download.prompt_for_download":
                False,

            "download.directory_upgrade":
                True,

            "safebrowsing.enabled":
                True
        }

        options.add_experimental_option(
            "prefs",
            prefs
        )

        driver = None

        try:

            print(
                "Starting Chrome WebDriver......"
            )

            driver = webdriver.Chrome(
                options=options
            )

            print(
                "Launching Chrome Browser......"
            )

            print(
                "Chrome Download directory:",
                download_dir
            )

            yield driver

        except Exception as e:

            print(
                "========================================"
            )

            print(
                "CHROME WEBDRIVER ERROR"
            )

            print(
                "========================================"
            )

            print(
                "Exception Type:",
                type(e).__name__
            )

            print(
                "Exception:",
                str(e)
            )

            print(
                "========================================"
            )

            raise

        finally:

            if driver is not None:

                try:

                    driver.quit()

                except Exception:
                    pass

    # =====================================================
    # FIREFOX
    # =====================================================

    elif browser == "firefox":

        options = webdriver.FirefoxOptions()

        # -------------------------------------------------
        # Find Firefox executable automatically
        # -------------------------------------------------

        firefox_binary = get_firefox_binary()

        options.binary_location = firefox_binary

        print(
            "Firefox binary:",
            firefox_binary
        )

        # -------------------------------------------------
        # Accept localhost/self-signed certificate
        # -------------------------------------------------

        options.accept_insecure_certs = True

        # -------------------------------------------------
        # Enable downloads
        # -------------------------------------------------

        options.enable_downloads = True

        # -------------------------------------------------
        # Disable proxy
        # -------------------------------------------------

        options.set_preference(
            "network.proxy.type",
            0
        )

        # -------------------------------------------------
        # Firefox startup settings
        # -------------------------------------------------

        options.set_preference(
            "browser.startup.page",
            0
        )

        options.set_preference(
            "browser.startup.homepage",
            "about:blank"
        )

        options.set_preference(
            "browser.shell.checkDefaultBrowser",
            False
        )

        # -------------------------------------------------
        # Download directory
        # -------------------------------------------------

        options.set_preference(
            "browser.download.folderList",
            2
        )

        options.set_preference(
            "browser.download.dir",
            download_dir
        )

        options.set_preference(
            "browser.download.useDownloadDir",
            True
        )

        # -------------------------------------------------
        # Download behavior
        # -------------------------------------------------

        options.set_preference(
            "browser.download.manager.showWhenStarting",
            False
        )

        options.set_preference(
            "browser.download.manager.focusWhenStarting",
            False
        )

        options.set_preference(
            "browser.download.manager.showAlertOnComplete",
            False
        )

        options.set_preference(
            "browser.download.manager.closeWhenDone",
            True
        )

        # -------------------------------------------------
        # Do not ask about downloaded files
        # -------------------------------------------------

        options.set_preference(
            "browser.helperApps.alwaysAsk.force",
            False
        )

        options.set_preference(
            "browser.download.always_ask_before_handling_new_types",
            False
        )

        # -------------------------------------------------
        # MIME types
        # -------------------------------------------------

        mime_types = ",".join([

            # XML
            "application/xml",
            "text/xml",
            "application/xhtml+xml",

            # Excel
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            # Generic downloads
            "application/octet-stream",
            "application/force-download",
            "binary/octet-stream",
            "application/download",
            "application/x-download",

            # CSV
            "text/csv",
            "application/csv"
        ])

        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            mime_types
        )

        # -------------------------------------------------
        # Prevent Firefox from opening files internally
        # -------------------------------------------------

        options.set_preference(
            "browser.download.viewableInternally.enabledTypes",
            ""
        )

        # -------------------------------------------------
        # Disable PDF viewer
        # -------------------------------------------------

        options.set_preference(
            "pdfjs.disabled",
            True
        )

        # =================================================
        # START FIREFOX
        # =================================================

        driver = None
        max_attempts = 3

        print(
            "========================================"
        )

        print(
            "Starting Firefox WebDriver......"
        )

        print(
            "========================================"
        )

        # -------------------------------------------------
        # Firefox startup retry
        # -------------------------------------------------

        for attempt in range(
            1,
            max_attempts + 1
        ):

            try:

                print(
                    f"Starting Firefox attempt "
                    f"{attempt}/{max_attempts}"
                )

                driver = webdriver.Firefox(
                    options=options
                )

                print(
                    "Launching Firefox Browser......"
                )

                print(
                    "Firefox Download directory:",
                    download_dir
                )

                # -------------------------------------------------
                # Verify browsing context
                # -------------------------------------------------

                WebDriverWait(
                    driver,
                    10
                ).until(
                    lambda d: len(
                        d.window_handles
                    ) > 0
                )

                current_window = (
                    driver.current_window_handle
                )

                print(
                    "Firefox window handle:",
                    current_window
                )

                print(
                    "Firefox browsing context is alive"
                )

                break

            except Exception as e:

                print(
                    "========================================"
                )

                print(
                    f"Firefox startup attempt "
                    f"{attempt} failed"
                )

                print(
                    "Exception Type:",
                    type(e).__name__
                )

                print(
                    "Exception:",
                    str(e)
                )

                print(
                    "========================================"
                )

                # -------------------------------------------------
                # Close failed Firefox session
                # -------------------------------------------------

                if driver is not None:

                    try:

                        driver.quit()

                    except Exception:
                        pass

                    driver = None

                # -------------------------------------------------
                # Retry
                # -------------------------------------------------

                if attempt == max_attempts:

                    print(
                        "Firefox could not be started "
                        "after 3 attempts."
                    )

                    raise

        # =================================================
        # GIVE DRIVER TO TEST
        # =================================================

        try:

            yield driver

        except Exception as e:

            print(
                "========================================"
            )

            print(
                "FIREFOX TEST ERROR"
            )

            print(
                "========================================"
            )

            print(
                "Exception Type:",
                type(e).__name__
            )

            print(
                "Error Message:",
                str(e)
            )

            print(
                "========================================"
            )

            raise

        finally:

            # -------------------------------------------------
            # Close Firefox
            # -------------------------------------------------

            if driver is not None:

                try:

                    print(
                        "Closing Firefox WebDriver......"
                    )

                    driver.quit()

                    print(
                        "Firefox WebDriver closed successfully"
                    )

                except Exception as e:

                    print(
                        "Firefox driver quit warning:",
                        type(e).__name__,
                        str(e)
                    )

    # =====================================================
    # EDGE
    # =====================================================

    elif browser == "edge":

        options = webdriver.EdgeOptions()

        options.accept_insecure_certs = True

        # -------------------------------------------------
        # Disable proxy
        # -------------------------------------------------

        options.add_argument(
            "--proxy-server=direct://"
        )

        options.add_argument(
            "--proxy-bypass-list=*"
        )

        # -------------------------------------------------
        # Download settings
        # -------------------------------------------------

        prefs = {

            "download.default_directory":
                download_dir,

            "download.prompt_for_download":
                False,

            "download.directory_upgrade":
                True,

            "safebrowsing.enabled":
                True
        }

        options.add_experimental_option(
            "prefs",
            prefs
        )

        driver = None

        try:

            print(
                "Starting Edge WebDriver......"
            )

            driver = webdriver.Edge(
                options=options
            )

            print(
                "Launching Edge Browser......"
            )

            print(
                "Edge Download directory:",
                download_dir
            )

            yield driver

        except Exception as e:

            print(
                "========================================"
            )

            print(
                "EDGE WEBDRIVER ERROR"
            )

            print(
                "========================================"
            )

            print(
                "Exception Type:",
                type(e).__name__
            )

            print(
                "Exception:",
                str(e)
            )

            print(
                "========================================"
            )

            raise

        finally:

            if driver is not None:

                try:

                    driver.quit()

                except Exception:
                    pass

    # =====================================================
    # INVALID BROWSER
    # =====================================================

    else:

        raise ValueError(
            f"Unsupported browser: {browser}. "
            f"Use chrome, firefox, or edge."
        )


# =========================================================
# BROWSER COMMAND-LINE OPTION
# =========================================================

def pytest_addoption(parser):

    parser.addoption(
        "--browser",
        action="store",
        default="chrome"
    )


# =========================================================
# BROWSER FIXTURE
# =========================================================

@pytest.fixture()
def browser(request):

    return request.config.getoption(
        "--browser"
    )


# =========================================================
# HTML REPORT METADATA
# =========================================================

def pytest_configure(config):
    pass


@pytest.fixture(
    scope="session",
    autouse=True
)
def metadata(request):
    pass


def pytest_metadata(metadata):

    metadata["Project Name"] = "nopCommerce"

    metadata["Module Name"] = "Customers"

    metadata["Tester"] = "Himasai"

    metadata.pop(
        "JAVA_HOME",
        None
    )

    metadata.pop(
        "Plugins",
        None
    )