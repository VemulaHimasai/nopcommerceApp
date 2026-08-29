
import pytest
import os
from selenium import webdriver


@pytest.fixture()
def setup(browser):

    # =====================================================
    # DOWNLOAD DIRECTORY
    # =====================================================

    download_dir = os.path.abspath(
        os.path.join(os.getcwd(), "downloads")
    )

    os.makedirs(download_dir, exist_ok=True)

    print("Download directory:", download_dir)

    # =====================================================
    # CHROME
    # =====================================================

    if browser == "chrome":

        options = webdriver.ChromeOptions()

        options.accept_insecure_certs = True

        # Disable proxy
        options.add_argument("--proxy-server=direct://")
        options.add_argument("--proxy-bypass-list=*")

        # Chrome download settings
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        options.add_experimental_option(
            "prefs",
            prefs
        )

        # Start Chrome
        driver = webdriver.Chrome(
            options=options
        )

        print("Launching Chrome Browser......")
        print(
            "Chrome Download directory:",
            download_dir
        )

        yield driver

        driver.quit()

    # =====================================================
    # FIREFOX
    # =====================================================

    elif browser == "firefox":

        options = webdriver.FirefoxOptions()

        options.accept_insecure_certs = True

        # =================================================
        # Disable proxy
        # =================================================

        options.set_preference(
            "network.proxy.type",
            0
        )

        # =================================================
        # Download directory
        # =================================================

        options.set_preference(
            "browser.download.folderlist",
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
        # Disable download dialogs
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
            "browser.download.always_ask_before_handling_new_types",
            False
        )

        options.set_preference(
            "browser.helperApps.alwaysAsk.force",
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
        # MIME TYPES
        # =================================================

        mime_types = [

            # ---------------------------------------------
            # XML
            # ---------------------------------------------

            "application/xml",
            "text/xml",
            "application/xhtml+xml",

            # ---------------------------------------------
            # Excel
            # ---------------------------------------------

            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            # ---------------------------------------------
            # Generic download
            # ---------------------------------------------

            "application/octet-stream",
            "application/force-download",
            "binary/octet-stream",
            "application/download",
            "application/x-download",

            # ---------------------------------------------
            # CSV
            # ---------------------------------------------

            "text/csv",
            "application/csv"
        ]

        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            ",".join(mime_types)
        )

        # =================================================
        # Do not open downloaded files inside Firefox
        # =================================================

        options.set_preference(
            "browser.download.viewableInternally.enabledTypes",
            ""
        )

        # =================================================
        # Disable PDF viewer
        # =================================================

        options.set_preference(
            "pdfjs.disabled",
            True
        )

        # =================================================
        # Start Firefox
        # =================================================

        driver = webdriver.Firefox(
            options=options
        )

        print("Launching Firefox Browser......")
        print(
            "Firefox Download directory:",
            download_dir
        )

        yield driver

        driver.quit()



# =====================================================
    # EDGE
    # =====================================================

    else:

        options = webdriver.EdgeOptions()

        options.accept_insecure_certs = True

        # Disable proxy
        options.add_argument("--proxy-server=direct://")
        options.add_argument("--proxy-bypass-list=*")

        # Edge download settings
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        options.add_experimental_option(
            "prefs",
            prefs
        )

        # Start Edge
        driver = webdriver.Edge(
            options=options
        )

        print("Launching Edge Browser......")
        print(
            "Edge Download directory:",
            download_dir
        )

        yield driver

        driver.quit()


# =========================================================
# BROWSER COMMAND-LINE OPTION
# =========================================================

def pytest_addoption(parser):

    parser.addoption(
        "--browser",
        action="store",
        default="chrome"
    )


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

    # Remove unnecessary information
    metadata.pop(
        "JAVA_HOME",
        None
    )

    metadata.pop(
        "Plugins",
        None
    )
