import os
import pytest
from selenium import webdriver


# =========================================================
# BROWSER FIXTURE
# =========================================================

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

        # Accept localhost/self-signed certificate
        options.accept_insecure_certs = True

        # Explicitly enable downloads
        options.enable_downloads = True

        # =================================================
        # Disable proxy
        # =================================================

        options.set_preference(
            "network.proxy.type",
            0
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
        # IMPORTANT
        # Do not ask what to do with downloaded files
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

            # Generic download
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

        # =================================================
        # Prevent Firefox from opening files internally
        # =================================================

        options.set_preference(
            "browser.download.viewableInternally.enabledTypes",
            ""
        )

        # Disable PDF viewer
        options.set_preference(
            "pdfjs.disabled",
            True
        )

        # =================================================
        # START FIREFOX
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

        options.add_argument("--proxy-server=direct://")
        options.add_argument("--proxy-bypass-list=*")

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

    metadata.pop(
        "JAVA_HOME",
        None
    )

    metadata.pop(
        "Plugins",
        None
    )