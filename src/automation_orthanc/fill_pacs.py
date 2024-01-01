import random
from os import environ
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=environ.get("HEADLESS", "true") == "true"
    )
    context = browser.new_context(
        http_credentials={"username": "orthanc", "password": "orthanc"},
        record_video_dir="./videos/",
    )

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    try:
        page = context.new_page()
        page.goto("http://pacs_provider:8042/app/explorer.html")

        page.get_by_role("link", name="Upload").click()
        project_root_folder_path = Path(__file__).parent.parent.parent
        # Loop over all .dcm files under sample_data folder and collect their paths
        dcm_files = []
        for dcm_file_path in project_root_folder_path.joinpath(
            "sample_data"
        ).glob("**/*.dcm"):
            dcm_files.append(str(dcm_file_path))

        with page.expect_file_chooser() as fc_info:
            page.get_by_role("link", name="Select files to upload").click()
        file_chooser = fc_info.value
        file_chooser.set_files(dcm_files)

        page.get_by_role("link", name="Start the upload").click()

        # Wait for the upload to finish
        page.wait_for_selector("text=Done")
        page.get_by_role("link", name="Lookup").click()
        page.get_by_role("link", name="All studies").click()

        # Collect all list item elements
        studies_list = page.query_selector_all("#all-studies li")
        picked_study = random.choice(studies_list)
        picked_study.click()

        # Collect all options for series
        series_list = page.query_selector_all("#list-series li")
        picked_series = random.choice(series_list)
        picked_series.click()
        page.wait_for_selector("text='Delete this series'")

        page.get_by_role("link", name="Send to DICOM modality").click()
        page.get_by_role("link", name="Tech_Challenge").click()
    finally:
        context.tracing.stop(path="./trace.zip")
        browser.close()


if __name__ == "__main__":
    # Check if PACS_HOST:8042 is reachable
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("pacs_provider", 8042))
    if result != 0:
        print("Orthanc is not running on pacs_provider:8042")  # noqa: T001
        exit(1)
    else:
        print("Orthanc is running on pacs_provider:8042")  # noqa: T001

    with sync_playwright() as playwright:
        run(playwright)
