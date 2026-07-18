import sys 
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m sentinel.main <folder_path>")
        return
    
    folder_path = Path(sys.argv[1])
    
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    log_files = list(folder_path.rglob("*.log"))
    
    if not log_files:
        print("No .log files found in the specified folder.")
        return
    
    total_lines = 0
    error_count = 0
    warning_count = 0
    info_count = 0
    
    print(f"Found {len(log_files)} log files:")
    for file in log_files:
        print(f"  - {file.name}")
    
    print()
    
    for file in log_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    total_lines += 1
                    line_upper = line.upper()  # Store for reuse
                    if "ERROR" in line_upper:
                        error_count += 1
                    elif "WARNING" in line_upper:
                        warning_count += 1
                    elif "INFO" in line_upper:
                        info_count += 1
        except FileNotFoundError:
            print(f"Skipping: {file.name} does not exist.")
        except PermissionError:
            print(f"Access Denied: You don't have permissions for {file.name}.")
        except Exception as e:
            print(f"Unexpected error on {file.name}: {e}")
    
    print("\n=== Summary ===")
    print(f"Total lines scanned: {total_lines}")
    print(f"Errors: {error_count}")
    print(f"Warnings: {warning_count}")
    print(f"Info: {info_count}")

if __name__ == "__main__":
    main()