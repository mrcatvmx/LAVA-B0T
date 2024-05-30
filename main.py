import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pyfiglet
import sys

def print_banner():
    banner = pyfiglet.figlet_format("CIPHER_AIRDROP", font="slant")
    print(banner)
    print('════════════════════════════════════════════════════════════')
    print('║       Welcome to LAVA 🔥 BOT!                             ║')
    print('║                                                            ║')
    print('║     Follow us on Twitter:                                  ║')
    print('║     https://twitter.com/cipher_airdrop                     ║')
    print('║                                                            ║')
    print('║     Join us on Telegram:                                   ║')
    print('║     - https://t.me/+tFmYJSANTD81MzE1                       ║')
    print('╚════════════════════════════════════════════════════════════')
    answer = input('Will you FC* Magma Points by creating accounts? (Y/N): ')
    if answer.lower() != 'y':
        print('Aborting installation.')
        sys.exit(1)

def launch_selenium_webdriver(driver_path, chrome_profile_path, profile_directory):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
    chrome_options.add_argument(f"profile-directory={profile_directory}")
    # Add arguments to disable LavaMoat's scuttling mode
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--disable-site-isolation-trials")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(5)
    print("Chrome with pre-configured MetaMask profile has been loaded")
    return driver

def wait_and_click(driver, by, value, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    element.click()

def wait_for_element(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def get_rpc_link(driver, button_xpath, input_xpath):
    try:
        # Click on the button to display the input field
        wait_and_click(driver, By.XPATH, button_xpath)
        time.sleep(2)
        # Find the input field and get its value
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, input_xpath))
        )
        value = element.get_attribute('value')
        return value
    except Exception as e:
        print(f"Failed to find element with XPath: {input_xpath}. Exception: {e}")
        return "Not found"

def main():
    print_banner()

    # Ask the user for the paths and signup link
    chrome_profile_path = input("Enter the path to your Chrome profile: ")
    profile_directory = input("Enter the profile directory: ")
    driver_path = input("Enter the path to your Chrome driver: ")
    signup_link = input("Enter the signup link: ")

    # Ask the user for the number of accounts to sign up
    num_accounts = int(input("How many accounts do you want to sign up? "))
    
    driver = launch_selenium_webdriver(driver_path, chrome_profile_path, profile_directory)
    driver.implicitly_wait(30)
    
    base_url = signup_link.split('/register')[0]
    
    # Open the file in write mode to store the RPC links
    with open('rpcresult.txt', 'w') as f:
        for i in range(num_accounts):
            print(f"Processing account {i+1}/{num_accounts}")
            
            driver.get(signup_link)
            time.sleep(2)
            
            # Refresh the page twice to ensure it loads correctly
            driver.refresh()
            time.sleep(1)
            driver.refresh()
            time.sleep(1)

            wait_and_click(driver, By.LINK_TEXT, "Proceed")
            time.sleep(2)
            
            driver.get(f"{base_url}/connection-progress")
            time.sleep(2)
            wait_and_click(driver, By.XPATH, "(.//*[normalize-space(text()) and normalize-space(.)='Connect your wallet'])[1]/following::button[1]")
            time.sleep(2)
            wait_and_click(driver, By.XPATH, "//button[@type='submit']")
            time.sleep(2)
            
            # Notify user to switch to MetaMask window and complete actions
            print("Please complete the MetaMask interactions manually.")
            time.sleep(5)  # Wait for user to switch to MetaMask
            
            # Notify user to unlock MetaMask
            print("Please unlock MetaMask and press 'Next'.")
            time.sleep(5)  # Wait for user to unlock MetaMask

            # Notify user to confirm connection
            print("Please confirm the connection in MetaMask.")
            time.sleep(5)  # Wait for user to confirm connection

            # Notify user to sign the message
            print("Please sign the message in MetaMask.")
            time.sleep(5)  # Wait for user to sign the message
            
            # Switch back to the main window
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(17)
            
            wait_and_click(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[2]/a")
            time.sleep(2)
            
            driver.get(f"{base_url}/profile")
            time.sleep(2)
            
            # Extract RPC links
            rpc_results = []

            eth_rpc = get_rpc_link(driver, "//*[@id='radix-:rf:-trigger-ETH']", "//*[@id='radix-:rf:-content-ETH']/div[1]/div[1]/div[1]/input[1]")
            near_rpc = get_rpc_link(driver, "//*[@id='radix-:rf:-trigger-NEAR']", "//*[@id='radix-:rf:-content-NEAR']/div[1]/div[1]/div[1]/input[1]")
            starknet_rpc = get_rpc_link(driver, "//*[@id='radix-:rf:-trigger-STRK']", "//*[@id='radix-:rf:-content-STRK']/div[1]/div[1]/div[1]/input[1]")
            axelar_rpc = get_rpc_link(driver, "//*[@id='radix-:rf:-trigger-AXELAR']", "//*[@id='radix-:rf:-content-AXELAR']/div[1]/div[1]/div[1]/input[1]")
            
            rpc_results.extend([eth_rpc, near_rpc, starknet_rpc, axelar_rpc])

            # Write RPC links to the file
            f.write(f"Account {i+1}\n")
            for result in rpc_results:
                f.write(result + '\n')
            f.write("\n")

            print(f"RPC links for account {i+1} have been saved to rpcresult.txt")
            
            if i < num_accounts - 1:
                # Navigate to profile page
                driver.get("https://points.lavanet.xyz/profile")
                time.sleep(2)

                # Click on "Leaderboard" and then "Logout"
                try:
                    print("Clicking Leaderboard")
                    leaderboard_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Leaderboard')]")
                    leaderboard_button.click()
                    time.sleep(2)
                    
                    print("Clicking Logout")
                    logout_button = driver.find_element(By.XPATH, "//*[text() = 'Logout']")
                    logout_button.click()
                    time.sleep(30)  # Wait for user to disconnect and switch MetaMask account
                except Exception as e:
                    print(f"Error logging out: {e}")

                # Navigate back to the signup page
                driver.get(signup_link)
                time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    main()
