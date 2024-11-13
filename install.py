import os

if os.getuid() != 0:
    print("Please use sudo.")

tools = [
    "nmap",
    "aircrack-ng",
    "metasploit",
    "sqlmap",
    "hydra",
    "hashcat",
    "john the ripper",
    "netcat",
    "bettercap",
]

wordlists = ''

def packages():
    print("This will install the following packags:")
    print("""
        1) Nmap
        2) Aircrack-ng
        3) Metasploit
        4) Sqlmap
        5) Hydra
        6) Hashcat
        7) John the Ripper
        8) Netcat
        9) Bettercap
        10) Seclists
        11) Payloads all the things
        """)
    

    

def main():
    try:
        packages()
        choice = input("Do you want to continue? Y/N: ").lower()

        while choice != 'y' or choice != 'n':
            print("Please select a valid character.")
            packages()
        
        print("Starting installation...")
        for tool in tools:
            print(f"Installing {tool}")
            os.system(f'apt install {tool} -y')
    except:
        pass