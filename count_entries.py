import json

def count_entries(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            count = len(data)
            print(f"Number of entries in {json_file}: {count}")
            
            # Print first entry as sample
            if count > 0:
                print("\nSample entry:")
                print(json.dumps(data[0], indent=2))
                
    except Exception as e:
        print(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    count_entries("tneallotment.json") 