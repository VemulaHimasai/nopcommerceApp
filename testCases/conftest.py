
import os
import subprocess
import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# =========================================================
# FIND FIREFOX EXECUTABLE
# =========================================================
def get_firefox_binary():

    # =====================================================
    # NORMAL FIREFOX INSTALLATION
    # =====================================================

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
            "Mozilla Firefox",
            "firefox.exe"
        )
    ]

    for path in normal_paths:

        if os.path.isfile(path):

            print(
                f"Firefox normal installation found: {path}"
            )

            return path

    # =====================================================
    # MICROSOFT STORE / MSIX FIREFOX
    # =====================================================

    ps_script = r'''
$package = Get-AppxPackage -Name "Mozilla.Firefox" |
           Select-Object -First 1

if (-not $package) {
    exit 10
}

Write-Output $package.InstallLocation
'''

    try:

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                ps_script
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        install_location = result.stdout.strip()

        print(
            "Firefox MSIX InstallLocation:"
        )
        print(install_location)

        if install_location:

            # =================================================
            # Known Firefox MSIX executable location
            # =================================================

            firefox_path = os.path.join(
                install_location,
                "VFS",
                "ProgramFiles",
                "Firefox Package Root",
                "firefox.exe"
            )

            print(
                "Checking Firefox executable:"
            )
            print(firefox_path)

            if os.path.isfile(firefox_path):

                print(
                    "Firefox MSIX executable found:"
                )
                print(firefox_path)

                return firefox_path

    except subprocess.TimeoutExpired:

        print(
            "Firefox MSIX detection timed out."
        )

    except Exception as e:

        print(
            "Firefox MSIX detection failed:",
            type(e).__name__,
            str(e)
        )

    # =====================================================
    # FALLBACK: SEARCH WINDOWSAPPS
    # =====================================================

    windows_apps = os.path.join(
        os.environ.get("PROGRAMFILES", ""),
        "WindowsApps"
    )

    if os.path.isdir(windows_apps):

        try:

            for folder in os.listdir(windows_apps):

                if folder.lower().startswith(
                    "mozilla.firefox_"
                ):

                    firefox_path = os.path.join(
                        windows_apps,
                        folder,
                        "VFS",
                        "ProgramFiles",
                        "Firefox Package Root",
                        "firefox.exe"
                    )

                    if os.path.isfile(firefox_path):

                        print(
                            "Firefox executable found using fallback:"
                        )
                        print(firefox_path)

                        return firefox_path

        except Exception as e:

            print(
                "WindowsApps search failed:",
                type(e).__name__,
                str(e)
            )

    # =====================================================
    # FIREFOX NOT FOUND
    # =====================================================

    raise FileNotFoundError(
        "Firefox executable was not found. "
        "Firefox may be installed through Microsoft Store "
        "but the firefox.exe executable could not be located."
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
        "========================================"
    )

    print(
        "Download directory:"
    )

    print(
        download_dir
    )

    print(
        "========================================"
    )

    # =====================================================
    # CHROME
    # =====================================================

    if browser == "chrome":

        options = webdriver.ChromeOptions()

        # -------------------------------------------------
        # Accept localhost/self-signed certificate
        # -------------------------------------------------

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
                "========================================"
            )

            print(
                "Starting Chrome WebDriver......"
            )

            print(
                "========================================"
            )

            driver = webdriver.Chrome(
                options=options
            )

            print(
                "Chrome Browser launched successfully."
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

                    print(
                        "Closing Chrome WebDriver......"
                    )

                    driver.quit()

                    print(
                        "Chrome WebDriver closed successfully."
                    )

                except Exception as e:

                    print(
                        "Chrome driver quit warning:",
                        type(e).__name__,
                        str(e)
                    )

    # =====================================================
    # FIREFOX
    # =====================================================

    elif browser == "firefox":

        options = webdriver.FirefoxOptions()

        # =================================================
        # FIND REAL FIREFOX EXECUTABLE
        # =================================================

        firefox_binary = get_firefox_binary()

        options.binary_location = firefox_binary

        print(
            "Firefox binary:",
            firefox_binary
        )

        # =================================================
        # CERTIFICATE
        # =================================================

        options.accept_insecure_certs = True

        # =================================================
        # DOWNLOADS
        # =================================================

        options.enable_downloads = True

        # =================================================
        # DISABLE PROXY
        # =================================================

        options.set_preference(
            "network.proxy.type",
            0
        )

        # =================================================
        # FIREFOX STARTUP SETTINGS
        # =================================================

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

        # =================================================
        # DOWNLOAD DIRECTORY
        # =================================================

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

        # =================================================
        # DOWNLOAD BEHAVIOR
        # =================================================

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

        # =================================================
        # DO NOT ASK ABOUT DOWNLOADS
        # =================================================

        options.set_preference(
            "browser.helperApps.alwaysAsk.force",
            False
        )

        options.set_preference(
            "browser.download.always_ask_before_handling_new_types",
            False
        )

        # =================================================
        # MIME TYPES
        # =================================================

        mime_types = ",".join([

            # XML
            "application/xml",
            "text/xml",
            "application/xhtml+xml",

            # Excel
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            # CSV
            "text/csv",
            "application/csv",

            # Generic downloads
            "application/octet-stream",
            "application/force-download",
            "binary/octet-stream",
            "application/download",
            "application/x-download"
        ])

        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            mime_types
        )

        # =================================================
        # PREVENT INTERNAL FILE VIEWING
        # =================================================

        options.set_preference(
            "browser.download.viewableInternally.enabledTypes",
            ""
        )

        # =================================================
        # DISABLE PDF VIEWER
        # =================================================

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

        # =================================================
        # FIREFOX STARTUP RETRY
        # =================================================

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
                    "Firefox Browser launched successfully."
                )

                print(
                    "Firefox Download directory:",
                    download_dir
                )

                # -----------------------------------------
                # Verify browser window
                # -----------------------------------------

                WebDriverWait(
                    driver,
                    10
                ).until(

                    lambda d:
                    len(
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
                    "Firefox browsing context is alive."
                )

                # -----------------------------------------
                # Firefox started successfully
                # -----------------------------------------

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

                # -----------------------------------------
                # Close failed session
                # -----------------------------------------

                if driver is not None:

                    try:

                        driver.quit()

                    except Exception:

                        pass

                    driver = None

                # -----------------------------------------
                # Final attempt
                # -----------------------------------------

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

            # ---------------------------------------------
            # CLOSE FIREFOX
            # ---------------------------------------------

            if driver is not None:

                try:

                    print(
                        "Closing Firefox WebDriver......"
                    )

                    driver.quit()

                    print(
                        "Firefox WebDriver closed successfully."
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

        # -------------------------------------------------
        # Accept localhost/self-signed certificate
        # -------------------------------------------------

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
                "========================================"
            )

            print(
                "Starting Edge WebDriver......"
            )

            print(
                "========================================"
            )

            driver = webdriver.Edge(
                options=options
            )

            print(
                "Edge Browser launched successfully."
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

                    print(
                        "Closing Edge WebDriver......"
                    )

                    driver.quit()

                    print(
                        "Edge WebDriver closed successfully."
                    )

                except Exception as e:

                    print(
                        "Edge driver quit warning:",
                        type(e).__name__,
                        str(e)
                    )

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


# =========================================================
# SESSION METADATA FIXTURE
# =========================================================

@pytest.fixture(
    scope="session",
    autouse=True
)
def metadata(request):
    pass


# =========================================================
# PYTEST HTML REPORT METADATA
# =========================================================

def pytest_metadata(metadata):

    metadata["Project Name"] = "nopCommerce"

    metadata["Module Name"] = "Customers, Catalog"

    metadata["Tester"] = "Himasai"

    # -----------------------------------------------------
    # Remove unnecessary metadata
    # -----------------------------------------------------

    metadata.pop(
        "JAVA_HOME",
        None
    )

    metadata.pop(
        "Plugins",
        None
    )

