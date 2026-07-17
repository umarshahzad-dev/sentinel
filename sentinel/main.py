import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python sentinel.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        print(f"Scanning folder: {folder_path}")
    
if __name__ == "__main__":
    main()