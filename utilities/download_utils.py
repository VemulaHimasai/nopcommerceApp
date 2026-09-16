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

                print(
                    f"Removed old download: {file}"
                )

            except PermissionError:

                print(
                    f"Could not delete file: {file}"
                )


def wait_for_download(
        download_dir,
        extension,
        timeout=60
):

    os.makedirs(download_dir, exist_ok=True)

    extension = extension.lower()

    end_time = time.time() + timeout

    print(
        f"\nWaiting for {extension} download..."
    )

    print(
        f"Download timeout: {timeout} seconds"
    )

    while time.time() < end_time:

        try:

            files = os.listdir(download_dir)

        except FileNotFoundError:

            time.sleep(1)
            continue

        print(
            "Download folder:",
            files
        )

        # -------------------------------------------------
        # Find completed files
        # -------------------------------------------------

        matching_files = [
            file
            for file in files
            if file.lower().endswith(extension)
            and os.path.isfile(
                os.path.join(download_dir, file)
            )
        ]

        # -------------------------------------------------
        # Check matching files
        # -------------------------------------------------

        if matching_files:

            # Sort newest first
            matching_files.sort(
                key=lambda file: os.path.getmtime(
                    os.path.join(
                        download_dir,
                        file
                    )
                ),
                reverse=True
            )

            latest_file = matching_files[0]

            latest_file_path = os.path.join(
                download_dir,
                latest_file
            )

            try:

                file_size = os.path.getsize(
                    latest_file_path
                )

            except OSError:

                time.sleep(1)
                continue

            # -------------------------------------------------
            # Make sure file is not empty
            # -------------------------------------------------

            if file_size == 0:

                print(
                    f"Excel file exists but is empty: "
                    f"{latest_file}"
                )

                time.sleep(1)
                continue

            # -------------------------------------------------
            # Check file size stability
            #
            # This is better than checking whether ANY
            # temporary file exists in the directory.
            # -------------------------------------------------

            time.sleep(1)

            try:

                new_file_size = os.path.getsize(
                    latest_file_path
                )

            except OSError:

                time.sleep(1)
                continue

            if new_file_size == file_size:

                print(
                    "\nDownload completed successfully."
                )

                print(
                    "Downloaded file:",
                    latest_file
                )

                print(
                    "File size:",
                    new_file_size,
                    "bytes"
                )

                return latest_file

            print(
                f"Download still in progress: "
                f"{file_size} -> {new_file_size} bytes"
            )

        # -------------------------------------------------
        # Display temporary files for debugging
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

        if temporary_files:

            print(
                "Temporary download files:",
                temporary_files
            )

        time.sleep(1)

    # -----------------------------------------------------
    # Final diagnostic information
    # -----------------------------------------------------

    try:

        final_files = os.listdir(
            download_dir
        )

    except Exception:

        final_files = []

    raise TimeoutError(
        f"\nDownload of {extension} file was not completed "
        f"within {timeout} seconds.\n"
        f"Files currently in download directory: "
        f"{final_files}"
    )