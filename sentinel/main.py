import sys 
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m sentinel.main <folder_path>")
    else:
        folder_path = Path(sys.argv[1])
        
        if not folder_path.exists():
            print(f"Error: Folder '{folder_path}' does not exist.")
            return

        log_files = list(folder_path.rglob("*.log"))
        
        if log_files:
            print(f"Found{len(log_files)} log files")
            for file in log_files:
                print(file.name)
        else:
            print("No .log files found in the specified folder.")
    
if __name__ == "__main__":
    main()