import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

def tcp_test(url):
    """Check if a URL is reachable using a TCP connection."""
    try:
        # Parse the hostname and port
        parsed_url = urlparse(url.strip())
        hostname = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == "https" else 80)

        if not hostname:
            return {"url": url, "tcp": False, "error": "Invalid URL"}

        # Attempt a TCP connection
        with socket.create_connection((hostname, port), timeout=5):
            return {"url": url, "tcp": True}
    except (socket.timeout, socket.error) as e:
        return {"url": url, "tcp": False, "error": str(e)}

def check_urls_in_parallel(urls, max_workers=10):
    """Check the status of URLs in parallel using TCP tests."""
    inactive_results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(tcp_test, url): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            if not result["tcp"]:  # Keep only inactive URLs
                inactive_results.append(result)
    return inactive_results

def read_urls_from_html(file_path):
    """Extract all URLs from an HTML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            urls = [a["href"] for a in soup.find_all("a", href=True)]
        return urls
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return []

if __name__ == "__main__":
    # Specify the HTML file containing the URLs
    input_file = "urls.html"

    # Extract URLs from the HTML file
    urls_to_check = read_urls_from_html(input_file)

    if not urls_to_check:
        print("No URLs found in the HTML file. Exiting.")
    else:
        # Check the URLs in parallel
        inactive_results = check_urls_in_parallel(urls_to_check)

        # Print the results
        if not inactive_results:
            print("All URLs are active.")
        else:
            print("Inactive URLs:")
            for result in inactive_results:
                print(f"URL: {result['url']}")
                if "error" in result:
                    print(f"  Error: {result['error']}")
