import random
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

from src.settings import config


def run(pw: Playwright) -> None:
    browser = pw.chromium.launch(
        headless=config.HEADLESS,
    )
    context = browser.new_context(
        http_credentials={
            "username": config.ORTHANC_USERNAME,
            "password": config.ORTHANC_PASSWORD,
        },
    )

    try:
        page = context.new_page()
        page.goto(
            f"http://{config.PACS_PROVIDER_HOST}:{config.PACS_PROVIDER_PORT}/app/explorer.html"
        )

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
        print("Upload finished")

        page.get_by_role("link", name="Lookup").click()
        page.get_by_role("link", name="All studies").click()
        print("All studies")

        # Collect all list item elements
        page.wait_for_selector("#all-studies li")
        studies_list = page.query_selector_all("#all-studies li")
        print("Studies collected ", len(studies_list))
        picked_study = random.choice(studies_list)
        print("Selected study: ", picked_study.text_content())
        picked_study.click(force=True)
        print("Study selected")

        # Collect all options for series
        page.wait_for_selector("#list-series li div")
        series_list = page.query_selector_all("#list-series li div")
        print("Series collected ", len(series_list))
        picked_series = random.choice(series_list)
        print("Selected series: ", picked_series.text_content())
        picked_series.click(force=True)
        print("Series selected")

        page.wait_for_selector("text='Delete this series'")

        page.get_by_role("link", name="Send to DICOM modality").click()
        page.get_by_role("link", name="Tech_Challenge").click()
        print("Sent to DICOM modality")
    finally:
        browser.close()


def check_connectivity():
    print(
        "Checking connectivity, ",
        {config.PACS_PROVIDER_HOST, config.PACS_PROVIDER_PORT},
    )

    # Check if pacs provider is running
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(
        (config.PACS_PROVIDER_HOST, config.PACS_PROVIDER_PORT)
    )
    if result != 0:
        print(
            f"Orthanc is not running on {config.PACS_PROVIDER_HOST}:{config.PACS_PROVIDER_PORT}"
        )  # noqa: T001
        exit(1)
    else:
        print(
            f"Orthanc is running on {config.PACS_PROVIDER_HOST}:{config.PACS_PROVIDER_PORT}"
        )  # noqa: T001


if __name__ == "__main__":
    check_connectivity()

    with sync_playwright() as playwright:
        run(playwright)

    print("Successfully finished")
