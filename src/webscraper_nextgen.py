import requests
from bs4 import BeautifulSoup
import csv
import webbrowser
import time

def open_website(url):
    try:
        # Define custom headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': url
            # Add any other headers you may need
        }

        # Make a GET request to the website with custom headers
        response = requests.get(url, headers=headers, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the website in the default web browser
            webbrowser.open(url)
        else:
            print(f"Failed to open the website. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_save_data(url, output_csv):
    try:
        # Define custom headers for the scraping request
        scraping_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': url
            # Add any other headers you may need
        }

        # Make a GET request to the website, this time for scraping, ignoring SSL certificate verification
        response = requests.get(url, headers=scraping_headers, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table with the specified class
            table = soup.find('table', class_='table table-bordered table-condensed')

            # Extract data from the table
            data = []
            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                data.append([column.get_text(strip=True) for column in columns])

            # Print data to the console
            for row in data:
                print(row)

            # Save data to a CSV file
            with open(output_csv, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Commodity', 'Classification', 'Grade', 'Sex', 'Market', 'Wholesale', 'Retail', 'Supply Volume', 'County', 'Date'])
                csv_writer.writerows(data)

            print(f"Data saved to {output_csv}")
        else:
            print(f"Failed to scrape data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    website_url = "https://amis.co.ke/site/market?product=&per_page=3000"
    output_csv = "market_data.csv"

    open_website(website_url)

    # Wait for 10 seconds before scraping
    time.sleep(10)

    scrape_and_save_data(website_url, output_csv)
