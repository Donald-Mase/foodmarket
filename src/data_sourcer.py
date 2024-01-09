import webbrowser
import requests
import time
import schedule
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

def open_link():
    url = "https://amis.co.ke/site/market?product=&per_page=3000&export=excel"

    # Disable SSL verification for the requests
    response = requests.get(url, verify=False)
    print("Link opened successfully.")

    # Open the link in a web browser
    webbrowser.open(url)
    print("Link opened in the web browser.")

    # Wait for 30 seconds before scheduling file mover
    time.sleep(30)

    # Schedule file mover after 30 seconds
    move_file()




def transfer_records():
    market_prices_path = "C:\\Users\\Dell\\Documents\\GitHub\\python project\\farm data\\Market Prices.xls"
    data_combined_path = "C:\\Users\\Dell\\Documents\\GitHub\\python project\\farm data\\data_combined.xlsx"

    try:
        # Read the Excel files into DataFrames
        market_prices_df = pd.read_excel(market_prices_path)
        
        # If data_combined.xlsx doesn't exist, create a new one with Market Prices data
        if not os.path.exists(data_combined_path):
            market_prices_df.to_excel(data_combined_path, index=False)
            print(f"Initial data_combined.xlsx created with {len(market_prices_df)} records from Market Prices.")
            return

        data_combined_df = pd.read_excel(data_combined_path)

        # Transfer records from Market Prices to data_combined
        data_combined_df = pd.concat([data_combined_df, market_prices_df], ignore_index=True)

        # Write the updated DataFrame back to data_combined file
        data_combined_df.to_excel(data_combined_path, index=False)

        num_transferred_records = len(market_prices_df)
        print(f"{num_transferred_records} records from Market Prices transferred to data_combined.xlsx.")
    except pd.errors.EmptyDataError:
        print("No data found in one of the files. Please check the file formats.")
    except Exception as e:
        print(f"Error transferring data: {e}")

# Call the function to combine all data



def move_file():
    src_path = "C:\\Users\\Dell\\Downloads\\Market Prices.xls"
    dest_path = "C:\\Users\\Dell\\Documents\\GitHub\\python project\\farm data\\Market Prices.xls"
    try:
        # Check if the file already exists in the destination folder
        if os.path.exists(dest_path):
            # Delete the existing file in the destination folder
            os.remove(dest_path)
            print(f"Existing file deleted from {dest_path}")

        # Move the file to the destination folder
        os.rename(src_path, dest_path)
        print(f"File moved from {src_path} to {dest_path}")

        # Compare and pass missing records after moving the file
        transfer_records()

        # Wait for 30 seconds before attempting to delete the file
        time.sleep(30)

        # Delete the file from the Downloads folder
        os.remove(dest_path)
        print(f"File deleted from {src_path}")
    except Exception as e:
        print(f"Error moving/deleting file: {e}")

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith("Market Prices.xls"):
            print(f"File detected: {event.src_path}")
            # Do nothing here; the file mover is scheduled after the link is opened

# Watch Downloads folder for changes
downloads_path = "C:\\Users\\Dell\\Downloads"
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=downloads_path, recursive=False)
observer.start()

# Open link immediately upon starting
open_link()

# Schedule to open link every 6 hours
schedule.every(6).hours.do(open_link)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
