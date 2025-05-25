# Open input and output files
with open("input.txt", "r") as infile, open("Instructions.hex", "w") as outfile:
    for line in infile:
        hex_str = line.strip()
        if len(hex_str) != 8:
            continue  # Skip invalid lines
        
        # Convert hex string to integer
        instruction = int(hex_str, 16)

        # Convert to bytes in little-endian format
        instruction_bytes = instruction.to_bytes(4, byteorder='little')

        # Format and write to output file
        formatted_bytes = ' '.join(f'{byte:02X}' for byte in instruction_bytes)
        outfile.write(formatted_bytes + '\n')
