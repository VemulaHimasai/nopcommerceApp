### Modified `utilities/download_utils.py`


import os
import time


def clear_downloads(download_dir):

    os.makedirs(download_dir, exist_ok=True)

    for file in os.listdir(download_dir):

        file_path = os.path.join(
            download_dir,
            file
        )

        if os.path.isfile(file_path):

            try:
                os.remove(file_path)

            except PermissionError:
                print(
                    f"Could not delete file: {file}"
                )


def wait_for_download(
        download_dir,
        extension,
        timeout=30
):

    end_time = time.time() + timeout

    while time.time() < end_time:

        files = os.listdir(download_dir)

        print(
            "Download folder:",
            files
        )

        # -------------------------------------------------
        # Look for completed file
        # -------------------------------------------------

        matching_files = [
            file
            for file in files
            if file.lower().endswith(
                extension.lower()
            )
        ]

        # -------------------------------------------------
        # Firefox temporary download files
        # -------------------------------------------------

        temporary_files = [
            file
            for file in files
            if file.lower().endswith(
                (
                    ".part",
                    ".crdownload",
                    ".tmp"
                )
            )
        ]

        # -------------------------------------------------
        # Download completed
        # -------------------------------------------------

        if matching_files:

            # If temporary file still exists,
            # download may still be in progress.

            if not temporary_files:

                return matching_files[0]

        time.sleep(1)

    # -----------------------------------------------------
    # Debug information
    # -----------------------------------------------------

    final_files = os.listdir(download_dir)

    raise TimeoutError(
        f"Download of {extension} file was not completed "
        f"within {timeout} seconds.\n"
        f"Files currently in download directory: "
        f"{final_files}"
    )

