# TODO: Install go, and add support for assetfinder, subjack, waybackurls

import os
import subprocess

# COLORS
GREEN = "\033[92m"
RED = "\033[91m"
TEAL = "\033[96m"
MAGENTA = "\033[95m"
ORANGE = "\033[93m"
BOLD_ORANGE = "\033[1;93m"
RESET = "\033[0m"
BOLD_GREEN = "\033[1;92m"
BOLD_RED = "\033[1;91m"

banner = f"""{RED}
 _ __      _  _  ___               
| / / ___ | |<_>| | '_ _  ___  _ _ 
|  \\ <_> || || || |-| | |/ ._>| '_>
|_\\_\\<___||_||_||_| `_. |\\___.|_|  
                    <___'          {RESET}
        {TEAL}by beb0pwned{RESET}
"""

# Tools and wordlists to be installed
tools = [
    "nmap",
    "curl",
    "aircrack-ng",
    "sqlmap",
    "hydra",
    "medusa",
    "hashcat",
    "john",
    "bettercap",
    "ffuf",
    "dirb",
    "nikto",
    "dnsenum",
    "sublist3r",
    'whois',
    'traceroute',
    'openvpn',
    'proxychains4',
    'zsh',
    'golang-go',

]

snap_tools = [
    'metasploit-framework',
    'feroxbuster',
    'searchsploit',
    'amass',
]

prerequisites = [
    'libpcap-dev'
]

go_tools = [
    ['httpx','github.com/projectdiscovery/httpx/cmd/httpx@latest'],
    ['subfinder','github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest'],
    ['cvemap','github.com/projectdiscovery/cvemap/cmd/cvemap@latest'],
    ['katana','github.com/projectdiscovery/katana/cmd/katana@latest'],
    ['naabu', 'github.com/projectdiscovery/naabu/v2/cmd/naabu@latest']
]

#0 = package name; 1=download link; 2=new file name
web_downloads = [
    ["Burp Suite (CE)", "https://portswigger.net/burp/releases/startdownload?product=community&version=2024.9.5&type=Linux", 'burpsuite_community.sh'],
]

git_wordlists = [
            ['SecLists', 'git clone https://github.com/danielmiessler/SecLists.git'],
            ['PayloadsAllTheThings','git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git'],
             ]

def display_packages():
    """
    Displays the list of tools and wordlists to be installed
    returns a string
    """
    print("This will install the following packages:\n")
    tool_total = 0

    # Print Tools
    print(f"{BOLD_GREEN}Tools:{RESET}\n")
    for i, tool in enumerate(tools):
        print(f"{i + 1}) {tool}")
        tool_total += 1

    # Print tools that need to be downloaded with snap
    for i, tool in enumerate(snap_tools):
        print(f"{i + 1 + tool_total}) {tool}")
        tool_total += 1

    # Tools that need to be downloaded using go
    for i, tool in enumerate(go_tools):
        print(f"{i + 1 + tool_total}) {tool[0]}")
        tool_total += 1

    # Tools that need to be downloaded from the web
    for i, tool in enumerate(web_downloads):
        print(f"{i + 1 + tool_total}) {tool[0]}")
        tool_total += 1

    # Print Wordlists
    print(f"\n{BOLD_GREEN}Wordlists:{RESET}\n")
    for wordlist in git_wordlists:
        wordlist_name = wordlist[0]
        print(f"{i + 1}) {wordlist_name}")
    
    print("")
    choice = input("Do you want to continue? Y/N: ").lower()

    return choice

def check_directories(path=''):
    """
    Iterates through the names of directories in the specified path and checks to see if they already exist
    """
    existing_dir = set()
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                existing_dir.add(item.lower())

    except Exception as e:
        print(f"Error: {e}")

    except PermissionError:
        print(f"{RED}Permission denied to access {path}.{RESET}")

    return existing_dir

def lowercase_directories(path=''):
    """
    Iterates through the names of directories in the specified path and changes them to lowercase.
    """
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)

            # Check if the item is a directory
            if os.path.isdir(full_path):
                # Convert the directory name to lowercase
                new_name = item.lower()

                # Rename the directory if the name is different
                if item != new_name:
                    new_full_path = os.path.join(path, new_name)
                    os.rename(full_path, new_full_path)
                    print(f"{TEAL}Rename: {item} -> {new_name}{RESET}")
    
    except Exception as e:
        print(f"Error: {e}")

def install_prerequisites():
    # Install prerequisites for some tools
    print(f'\n{BOLD_GREEN}Installing prerequisites...{RESET}\n')
    for prereq in prerequisites:
        print(f'{GREEN}Installing {prereq}...{RESET}')
        os.system(f'apt install {prereq} -y')
        

def install_tools():
    # Update + Upgrade first
    print(f"\n{BOLD_GREEN}Updating and Upgrading...{RESET}\n")
    os.system("apt update -y && apt upgrade -y && apt full-upgrade -y")

    #Install tools
    print(f"\n{BOLD_GREEN}Starting installation...\n{RESET}")
    for tool in tools:
        print(f"{GREEN}Installing {tool}{RESET}")
        os.system(f'apt install {tool} -y')

    # Install snap tools
    for tool in snap_tools:
        print(f"{GREEN}Installing {tool} with snap.{RESET}")
        os.system(f'snap install {tool}')

def install_wordlists():
    #Create directory for wordlists and check for existing wordlists
    os.makedirs("/opt/wordlists", exist_ok=True)
    existing_wordlists = check_directories("/opt/wordlists")

    print(f"\n{BOLD_GREEN}Installing Wordlists...{RESET}\n")
    
    for wordlist in git_wordlists:
        wordlist_name = wordlist[0].lower()
        download_url = wordlist[1]

        if wordlist_name in existing_wordlists:
            print(f"{TEAL}Skipping {wordlist_name} (already installed).{RESET}")

        else:
            print(f"{GREEN}Installing {wordlist_name} at /opt/wordlists{RESET}")
            os.system(f"cd /opt/wordlists; {download_url}")

    # Rename directories to lowercase after cloning
    lowercase_directories("/opt/wordlists")


def go_install_tools():
    # Download tools that need Go to download
    print(f"\n{BOLD_GREEN}Download tools using go...{RESET}\n")
    for tool in go_tools:
        tool_name = tool[0]
        download_url  = tool[1]

        print(f'{MAGENTA}Installing {tool_name}...{RESET}')
        result = subprocess.run(
            ['go', 'install', '-v', download_url],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f'{GREEN}{tool_name} downloaded successfully.{RESET}\n')
        else:
            print(f'{BOLD_RED}Failed to download {tool_name}: {result.stderr}{RESET}\n')


def download_web_tools():
    # Download and install apps from the web
    os.makedirs('web_downloads', exist_ok=True)
    
    print(f"\n{BOLD_GREEN}Downloading tools from the web...{RESET}\n")
    for tool in web_downloads:
        tool_name = tool[0]
        download_url = tool[1]
        filename = tool[2]
        file_path= f'web_downloads/{filename}'

        if os.path.exists(file_path):
            print(f"{TEAL}{tool_name} already exists. Skipping download.{RESET}")
        else:    
            print(f"{GREEN}Installing {tool_name}...{RESET}")

            result = subprocess.run(
                ['wget', '-O', file_path, download_url],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"\n{GREEN}{tool_name} downloaded successfully.{RESET}")
            else:
                print(f"{BOLD_RED}Failed to download {tool_name}: {result.stderr}{RESET}")            
            

def main():
    try:
        # Check if the script is being run with sudo/root privileges
        if os.getuid() != 0:
            print(f"{BOLD_RED}Please use sudo.{RESET}")
        else:
            print(banner)
            decision = display_packages()
            if decision == 'y':
                install_prerequisites()
                install_tools()
                go_install_tools()
                install_wordlists()
                download_web_tools()
                print(f"\n{BOLD_ORANGE}Installation completed successfully!{RESET}")
                
            elif decision == 'n':
                print(f"{RED}Exitting...{RESET}")
                os.system("exit")
                
            else:
                print(f"{RED}Invalid. Please enter 'Y' or 'N'.{RESET}")
                main()

    except KeyboardInterrupt:
        print(f"\n{RED}Installation interrupted by user.{RESET}")
    
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")


if __name__ == "__main__":
    main()
