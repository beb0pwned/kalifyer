import os

GREEN = "\033[92m"
RESET = "\033[0m"

if os.getuid() != 0:
    print("Please use sudo.")

tools = [
    "nmap",
    "aircrack-ng",
    "sqlmap",
    "hydra",
    "hashcat",
    "john",
    "bettercap",
]

raw_wordlists = [
    "seclists",
    "PayloadsAllTheThings"
]

git_wordlists = [
            'git clone https://github.com/danielmiessler/SecLists.git',
            'git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git',
             ]

def packages():
    print("This will install the following packages:")
    total = 0

    # Print Tools
    for i, tool in enumerate(tools):
        print(f"{i}) {tool}")
        total += 1

    #Print Wordlists
    for i, wordlist in enumerate(raw_wordlists):
        print(f"{i+total}) {wordlist}")
    
    print("")
    choice = input("Do you want to continue? Y/N: ").lower()

    return choice

def main():
    try:
        decision = packages()
        loop = True
        while loop == True:
            if decision == 'y':
                print(F"{GREEN}Starting installation...{RESET}")
                for tool in tools:
                    print(f"{GREEN}Installing {tool}{RESET}")
                    os.system(f'apt install {tool} -y')
                
                print(f"{GREEN}Installing Wordlists...{RESET}")
                
                os.system("mkdir /opt/wordlists")

                for wordlist in git_wordlists:
                    print(f"{GREEN}Installing {raw_wordlists[wordlist]} at /opt/wordlists{RESET}")
                    os.system(f"cd /opt/wordlists; {wordlist}")
                
                print("Done!")
                loop = False


            elif decision == 'n':
                print("Exitting...")
                os.system("exit")
                loop = False
            else:
                print("Please enter a valid character.")
                decision = packages()
                loop = True
    except:
        pass

if __name__ == main():
    main()