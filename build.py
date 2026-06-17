import datetime
import os
import re
import sys

def update_blocklist(file_path):
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' not found.")
        return

    header_lines = []
    rules = set()
    in_header = True

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            
            if in_header and (not stripped or stripped.startswith('!') or stripped.startswith('[')):
                if stripped != "!":
                    header_lines.append(line)
            else:
                in_header = False
                if stripped:
                    rules.add(stripped)

    sorted_rules = sorted(list(rules))
    entries_count = len(sorted_rules)

    timezone_moscow = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(timezone_moscow)
    
    last_modified_str = now.strftime("%d %b %Y %H:%M GMT+3")
    version_str = now.strftime("%Y%m%d.%H:%M")

    updated_header = []
    for line in header_lines:
        if line.startswith('! Version:'):
            line = f"! Version: {version_str}\n"

        elif line.startswith('! Last modified:'):
            line = f"! Last modified: {last_modified_str}\n"
            
        elif line.startswith('! Number of entries:'):
            line = f"! Number of entries: {entries_count}\n"
            
        updated_header.append(line)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(updated_header)

        f.write("!\n")
   
        for rule in sorted_rules:
            f.write(f"{rule}\n")

    print(f"Blocklist '{file_path}' updated")
    print(f"Rules: {entries_count}")
    print(f"Version: {version_str}")
    print(f"Last modified: {last_modified_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python build.py blocklist.txt")
        sys.exit(1)
        
    update_blocklist(sys.argv[1])
