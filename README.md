# JS Component Vulnerability Scanner

This script scans a target website for JavaScript components and checks for vulnerabilities associated with those components. It can also check the security headers of the target website.

## Prerequisites

- Python 3.x
- Required Python packages: `argparse`, `requests`, `beautifulsoup4`

## Installation

1. Clone the repository or download the script file (`Crawling_Web.py`) to your local machine.

2. Install the required Python packages by running the following command:

   ```shell
   pip install argparse requests beautifulsoup4

## Usage
1. Open a terminal or command prompt.

2. Navigate to the directory where the script file is located.

3. Run the following command to scan a target website for vulnerabilities:
   ```shell
   python Crawling_Web.py -v <target_url>
   ```
 Replace <target_url> with the URL of the website you want to scan.
 
4. Optionally, you can check the security headers of the target website by running the following command:
   ```shell
   python Crawling_Web.py -s <target_url>
   ```
5. Replace <target_url> with the URL of the website you want to check.

Follow the prompts and view the scan results for vulnerabilities or security headers.


## Example
To scan a website for vulnerabilities and check security headers, run the following command:
   ```shell
   python Crawling_Web.py -v -s https://example.com
   ```
 Replace https://example.com with the URL of the website you want to scan.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
....



# DEMO
Scaning vulnerabilities 1 website:
![image](https://github.com/thajnh30cm/Lab_IA/assets/107602878/e5d85178-6286-416c-8972-f0725722f5df)

![image](https://github.com/thajnh30cm/Lab_IA/assets/107602878/8b8225b6-d4d2-4828-9f3e-8b5a3b71798c)

![image](https://github.com/thajnh30cm/Lab_IA/assets/107602878/9bfbc0bf-3a22-49e9-a536-936493dced4a)

Check security headers:
![image](https://github.com/thajnh30cm/Lab_IA/assets/107602878/447308f1-4f0c-493a-a7b4-4e53eafe12e1)

