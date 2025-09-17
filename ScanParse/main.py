import os
import scanner

if __name__ == "__main__":
    # get all txt files with "input" in the filename within the same dir
    input_files = [file_name for file_name in os.listdir() if file_name.endswith('.txt') and 'input' in file_name]

    for input_file_str in input_files:
        with open(input_file_str, 'r') as input_file:
            # scanner
            scanner_output = scanner.run(input_file) # output_scanner is list of strings ()
            
            # IO code
            with open(input_file_str.replace("input", "output_scan"), 'w') as f:
                f.writelines(scanner_output)
            
