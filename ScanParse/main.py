import os
import scanner, parser

if __name__ == "__main__":
    # get all txt files with "input" in the filename within the same dir
    input_files = [file_name for file_name in os.listdir() if file_name.endswith('.txt') and 'input' in file_name]

    for input_file_str in input_files:
        with open(input_file_str, 'r') as input_file:
            input_stream = "".join(input_file.readlines())

            scanError = False
            for token in scanner.gettoken(input_stream):
                if scanError: continue # still run gettoken even after error to populate scan_output
                
                parser.processtoken(token)
                if token == "Error":
                    scanError = True
                    
            # IO code
            with open(input_file_str.replace("input", "output_scan"), 'w') as f:
                f.writelines([line+'\n' for line in scanner.scan_output])
            
