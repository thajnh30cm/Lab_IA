import argparse
import requests
from bs4 import BeautifulSoup
import re

def print_ascii_art(): # mau` me`
    art = """
     ____                    _ _             
    / ___|_ __ __ ___      _| (_)_ __   __ _ 
   | |   | '__/ _` \ \ /\ / / | | '_ \ / _` |
   | |___| | | (_| |\ V  V /| | | | | | (_| |
    \____|_|  \__,_| \_/\_/ |_|_|_| |_|\__, |
                                         |___/ 
    """
    print(art)


def scan_target(url): # Nhận URL truyền vào và scan 
    try:
        print("[*] Scanning target...")
        response = requests.get(url)
        html_content = response.text
        components = extract_components(html_content)
        if components:
            print("[*] Found JS Component(s):")
            for component in components:
                print(f"[--] {component}")

            input("\nPress Enter to check vulnerabilities...")
            print("===========================================")
            print("[*] Checking vulnerabilities....")
            for component in components:
                lib, ver = split_lib(component)
                find_vulnerabilities(lib, ver)
        else:
            print("[-] No JS components found")
    except requests.exceptions.RequestException as e:
        print("[-] Error occurred while connecting to the target URL:", e)


def extract_components(html_content): # Thu thập các file JS
    components = []
    pattern = r'<script\s+.*?\bsrc=["\']([^"\'\s]*)["\'].*?>' 
    matches = re.findall(pattern, html_content)
    for match in matches:
        try:
            if match[:8] == "https://" or match[:7]=="http://":  
                response = requests.get(match)
            else:
                response = requests.get(url + match)
            html_contents = response.text
            pattern = r"\/\*\!\s*(.*?)\s*\s\|"
            matches = re.findall(pattern, html_contents)
            for component in matches:
                components.append(component)
        except requests.exceptions.RequestException as e:
            print(f"[-] Error occurred while connecting to URL: {match}. Skipping...")
            continue
    return components


def split_lib(component): # Xử lý file JS để tách thành chuỗi và tách tên thư viện, phiên bản
    array = []
    regex_pattern = r"(\w+).*?(\d+\.\d+\.\d+)"
    matches = re.findall(regex_pattern, component)
    for match in matches:
        array.append(match[0].lower())
        array.append(match[1])
    return array


def find_vulnerabilities(lib, ver):
    url = f"https://security.snyk.io/package/npm/{lib}/{ver}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vulnerability_elements = soup.find_all(class_='vue--table__tbody')
    try:
        vulnerabilities = []
        for vulnerability in vulnerability_elements:
            vulnerability_name = vulnerability.find_all('a', class_='vue--anchor')
            vulnerable_version = vulnerability.find_all('div', class_='vulnerable-versions')
            details = vulnerability.find_all('div', class_='vulns-table__description')

            for x, y, z in zip(vulnerability_name, vulnerable_version, details):
                vulnerability_info = {
                    'name': x.text.strip(),
                    'version': y.text.strip(),
                    'detail': z.text.strip()
                }
                vulnerabilities.append(vulnerability_info)

        if vulnerabilities:
            print("Vulnerabilities Found!\n")
            while True:
                print("========== Vulnerabilities Menu ==========")
                for i, vulnerability in enumerate(vulnerabilities):
                    print(f"{i+1}. Vulnerability: {vulnerability['name']}")
                print("0. Exit\n\n")
                choice = input("Choose the number corresponding to the vulnerability you want to view (0 to exit): ")

                if choice == '0':
                    print("Thanks For Use!")
                    exit()

                try:
                    index = int(choice) - 1
                    selected_vulnerability = vulnerabilities[index]

                    print("[+] Vulnerability:", selected_vulnerability['name'])
                    print("[+] Vulnerable Version:", selected_vulnerability['version'])

                    details_text = selected_vulnerability['detail']
                    detail = details_text.split("How", 1)[0].strip()
                    upgrade_index = details_text.index("Upgrade")
                    upgrade_message = details_text[upgrade_index:].strip()

                    print("[+] Detail:", detail)
                    print("[+] Recommendation:", upgrade_message)
                    print("\n")

                except (ValueError, IndexError):
                    print("Invalid choice. Please select again.")

            print("Exiting the program.")
        else:
            print("[-] No vulnerabilities found!")
    except Exception as e:
        print("[-] Error occurred while fetching vulnerabilities!")



def check_security_header(url):
    try:
        print("[*] Checking security headers...")
        response = requests.get(url)
        headers = response.headers
        security_headers = {
            'Content-Security-Policy': headers.get('Content-Security-Policy'),
            'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
            'X-Frame-Options': headers.get('X-Frame-Options'),
            'X-XSS-Protection': headers.get('X-XSS-Protection')
        }
        for header, value in security_headers.items():
            if value:
                print(f"[+] {header}: {value}")
            else:
                print(f"[-] {header} header is missing")
    except requests.exceptions.RequestException as e:
        print("[-] Error occurred while connecting to the target URL:", e)


if __name__ == "__main__":
    print_ascii_art()
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("-v", "--vulnerabilities", action="store_true", help="Check for vulnerabilities")
    parser.add_argument("-s", "--security-header", action="store_true", help="Check security headers")
    parser.add_argument("url", type=str, help="Target URL")

    args = parser.parse_args()
    url = args.url

    if url:
        if args.vulnerabilities:
            scan_target(url)
        if args.security_header:
            check_security_header(url)
    else:
        print("[-] No URL specified. Please provide a target URL.")
