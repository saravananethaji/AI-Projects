import csv
import json
import sys

def csv_to_json(csv_file_path, json_file_path):
    """
    Convert CSV file to JSON format using the first line as headers
    """
    try:
        # Read CSV file with different encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                    # Create CSV reader
                    csv_reader = csv.DictReader(csv_file)
                    
                    # Convert to list of dictionaries
                    data = list(csv_reader)
                    
                    # Write to JSON file
                    with open(json_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(data, json_file, indent=4, ensure_ascii=False)
                        
                print(f"Successfully converted {csv_file_path} to {json_file_path} using {encoding} encoding")
                return
                
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"An error occurred with {encoding} encoding: {str(e)}")
                continue
        
        print("Failed to read the file with any of the attempted encodings")
        
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_json.py <input_csv_file> <output_json_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    csv_to_json(input_file, output_file) 