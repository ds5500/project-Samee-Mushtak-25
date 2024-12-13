#!/usr/bin/env python3

# FIRST-PARTY IMPORTS
import glob
import functools
import logging
import pathlib
import warnings

# THIRD-PARTY IMPORTS
import bs4 as bs
import requests

# SECOND-PARTY AND LOCAL IMPORTS


# PROGRAM SIDE-EFFECTS, DIRECT CONFIGURATION, AND LOGGING
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

warnings.filterwarnings(action="ignore")


# UTIL FUNCTIONS, DECORATORS
def return_if_file_exists(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        filename = args[0]
        if pathlib.Path(filename).exists():
            logger.info(f"File {filename} already exists. Skipping download")
            return filename
        return func(*args, **kwargs)

    return wrapper


def skip_if_file_exists(filename):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if pathlib.Path(filename).exists():
                logger.info(f"File {filename} already exists. Skipping execution")
                return filename
            return func(*args, **kwargs)

        return wrapper

    return decorator


@return_if_file_exists
def download_file(filename_to_save_to, url):

    logger.info(f"Downloading file from {url} to {filename_to_save_to}")
    response = requests.get(url, verify=False)

    with open(filename_to_save_to, "wb") as file:
        file.write(response.content)

    logger.info(f"Downloaded file from {url} to {filename_to_save_to}")

    return filename_to_save_to


def get_soup_from_url(url):
    response = requests.get(url, verify=False)
    return bs.BeautifulSoup(response.content, "html.parser")


# PROGRAM VARIABLES AND CONSTANTS
ROOT_URL = "https://gtrnadb.ucsc.edu/"
SPECIES_URL = "https://gtrnadb.ucsc.edu/browse.html"
ROOT_DIR = pathlib.Path(__file__).parent
# INPUT_DIRECTORY = ROOT_DIR / "tRNALeu-analysis"
# INPUT_TRNAS = INPUT_DIRECTORY / "fasta_urls_all_archaea.txt"
INPUT_TRNAS = "tRNALeu-analysis/fasta_urls_all_archaea.txt"
# PRIMORDIAL_TRNAS = INPUT_DIRECTORY / "primordial_trnas.fa"

# PROGRAM SUB-FUNCTIONS
@skip_if_file_exists(INPUT_TRNAS)
def generate_and_save_fasta_urls():
    urls_to_write = []
    try:
        response = requests.get(SPECIES_URL, verify=False)
        genomes_soup = bs.BeautifulSoup(response.content, "html.parser")
        accordions = genomes_soup.select("h4 + dl.accordion")
        archaea = accordions[1]
        genome_a_tags = archaea.select("tbody > tr > td > a")
        genome_urls = [ROOT_URL + tag.get("href") for tag in genome_a_tags]
        logging.info(f"Obtained genome URLs")

        for i in range(len(genome_urls)):
            if (i+1) % 10 == 0:
                    logging.info(f"Processing genome {i+1}/{len(genome_urls)}")
            base_url = genome_urls[i]
            summary_soup = get_soup_from_url(base_url)
            fastas_url = base_url + summary_soup.find("a", string="FASTA Seqs").get(
                "href"
            )
            fastas_soup = get_soup_from_url(fastas_url)
            fasta_urls = fastas_soup.select("h5 + a")
            urls_to_write.append(base_url + fasta_urls[1].get("href"))
            # for url in fasta_urls:
                # if "mature" in url.get("href"):
                    # final_url = base_url + url.get("href")
                    # urls_to_write.append(final_url)

        logging.info(f"Writing {len(urls_to_write)} URLs to {INPUT_TRNAS}")
        with open(INPUT_TRNAS, "w") as file:
            file.write("\n".join(urls_to_write))
            file.write("\n")
        logging.info(f"Wrote {len(urls_to_write)} URLs to {INPUT_TRNAS}")

        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching the species URL: {e}")
        return False
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return False


def download_fasta_files():
    download_folder = INPUT_DIRECTORY / "downloaded_fasta_files"

    if not download_folder.exists():
        download_folder.mkdir(parents=True)

    with open(INPUT_TRNAS, "r") as file:
        for line in file:
            url = line.strip()
            filename = url.split("/")[-1]
            download_file(INPUT_DIRECTORY / "downloaded_fasta_files" / filename, url)


def append_primordial_trnas():
    logging.info("Appending primordial tRNAs to each downloaded file")

    # read the primordial_trnas.fa file
    with open(PRIMORDIAL_TRNAS, "r") as file:
        primordial_trnas = file.read()

    # for each fa file in the input directory, append its content to the primordial_trnas.fa file
    fa_files = glob.glob(str(INPUT_DIRECTORY / "downloaded_fasta_files/*.fa"))

    for fa_file in fa_files:
        if fa_file == PRIMORDIAL_TRNAS:
            continue

        with open(fa_file, "r") as file:
            fa_file_data = file.read()

        with open(fa_file, "w") as file:
            file.write(primordial_trnas)
            file.write(fa_file_data)

    logging.info("Finished appending primordial tRNAs to each downloaded file")


# PROGRAM MAIN FUNCTIONS
def stage_scrape():
    generate_and_save_fasta_urls()
    # download_fasta_files()
    # append_primordial_trnas()


def stage_process():
    pass


# MAIN FUNCTION
def main():
    logger.info("Starting the process")

    logger.info("Starting Stage: Scrape")
    stage_scrape()
    logger.info("Finished Stage: Scrape")

    logger.info("Starting Stage: Process")
    stage_process()
    logger.info("Finished Stage: Process")

    logger.info("Finished the process")


if __name__ == "__main__":
    main()
