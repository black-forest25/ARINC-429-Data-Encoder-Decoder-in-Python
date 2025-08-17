import numpy as np

def encode_arinc429(label, data, ssm=0, sdi=0):
    """
    Encodes ARINC 429 data into a 32-bit word.
    """
    print(f"\n Encoding Process")
    print(f"Input Parameters:")
    print(f"label ={label}, (octal) + {oct(label)} ={label} decimal ")
    print(f" data ={data} ")
    print(f" ssm  ={ssm} ")
    print(f" sdi  ={sdi} ")
    # Validate inputs
    if not (0 <= label <= 3777):
        raise ValueError("Label must be between 0 and 3777 (octal).")
    if not (0 <= data <= 2**19 - 1):
        raise ValueError("Data must fit in 19 bits")
    if not (0 <= ssm <= 3):
        raise ValueError("SSM must be 0-3")
    if not (0 <= sdi <= 3):
        raise ValueError("SDI must be 0-3")
    
    # Convert to binary strings
    label_bin = format(label, '08b')
    print(f"\nStep 1 - Convert to binary:")
    print(f"  label {label} -> '{label_bin}' (8 bits)")
    
    label_bin_reversed = label_bin[::-1]  # Reverse label (ARINC 429 quirk)
    print(f"  label reversed -> '{label_bin_reversed}' (ARINC 429 LSB first)")
    
    data_bin = format(data, '019b')  # 19-bit data
    print(f"  data {data} -> '{data_bin}' (19 bits)")
    
    ssm_bin = format(ssm, '02b')  # 2-bit status
    print(f"  ssm {ssm} -> '{ssm_bin}' (2 bits)")
    
    sdi_bin = format(sdi, '02b')  # 2-bit source/destination
    print(f"  sdi {sdi} -> '{sdi_bin}' (2 bits)")
    
    # Combine: Label (1-8), Data (9-27), SSM (28-29), SDI (30-31), Parity (32)
    word_bin_no_parity = label_bin_reversed + data_bin + ssm_bin + sdi_bin
    print(f"\nStep 2 - Combine fields:")
    print(f"  Combined (no parity): '{word_bin_no_parity}' ({len(word_bin_no_parity)} bits)")
    print(f"    Bits 1-8  (Label): '{word_bin_no_parity[0:8]}'")
    print(f"    Bits 9-27 (Data):  '{word_bin_no_parity[8:27]}'")
    print(f"    Bits 28-29 (SSM):  '{word_bin_no_parity[27:29]}'")
    print(f"    Bits 30-31 (SDI):  '{word_bin_no_parity[29:31]}'")
    
    # Calculate odd parity (total 1s must be odd)
    ones_count = word_bin_no_parity.count('1')
    print(f"\nStep 3 - Calculate parity:")
    print(f"  Number of 1s in first 31 bits: {ones_count}")
    print(f"  {ones_count} is {'even' if ones_count % 2 == 0 else 'odd'}")
    
    parity = '1' if ones_count % 2 == 0 else '0'
    print(f"  For odd parity, need to add: '{parity}'")
    
    word_bin = word_bin_no_parity + parity
    print(f"  Final 32-bit word: '{word_bin}'")
    
    result = int(word_bin, 2)  # Return as 32-bit integer
    print(f"\nStep 4 - Convert to integer:")
    print(f"  Binary: {bin(result)}")
    print(f"  Decimal: {result}")
    print(f"  Hexadecimal: {hex(result)}")
    
    return result

def decode_arinc429(word):
    """
    Decode a 32-bit ARINC 429 word into components.
    Input: 32-bit integer.
    Returns: Dictionary with label, data, ssm, sdi, parity.
    """
    print(f"\n=== DECODING PROCESS ===")
    print(f"Input: {word} (decimal) = {hex(word)} (hex)")
    
    word_bin = format(word, '032b')  # Ensure 32-bit binary string
    print(f"32-bit binary: '{word_bin}'")
    
    print(f"\nStep 1 - Extract fields:")
    label_bin_reversed = word_bin[:8]
    print(f"  Bits 1-8  (Label reversed): '{label_bin_reversed}'")
    
    label_bin = label_bin_reversed[::-1]  # Reverse label back
    label = int(label_bin, 2)
    print(f"  Label normal order: '{label_bin}' = {label} decimal = {oct(label)} octal")
    
    data_bin = word_bin[8:27]
    data = int(data_bin, 2)  # 19-bit data
    print(f"  Bits 9-27 (Data): '{data_bin}' = {data} decimal")
    
    ssm_bin = word_bin[27:29]
    ssm = int(ssm_bin, 2)  # 2-bit status
    print(f"  Bits 28-29 (SSM): '{ssm_bin}' = {ssm} decimal")
    
    sdi_bin = word_bin[29:31]
    sdi = int(sdi_bin, 2)  # 2-bit source/destination
    print(f"  Bits 30-31 (SDI): '{sdi_bin}' = {sdi} decimal")
    
    parity_bin = word_bin[31]
    parity = int(parity_bin, 2)  # 1-bit parity
    print(f"  Bit 32 (Parity): '{parity_bin}' = {parity} decimal")
    
    # Verify parity (optional, for demo)
    ones_in_data = word_bin[:-1].count('1')
    expected_parity = 1 if ones_in_data % 2 == 0 else 0
    parity_valid = parity == expected_parity
    
    print(f"\nStep 2 - Verify parity:")
    print(f"  1s in first 31 bits: {ones_in_data}")
    print(f"  Expected parity: {expected_parity}")
    print(f"  Actual parity: {parity}")
    print(f"  Parity valid: {parity_valid}")
    
    result = {
        'label': label,
        'data': data,
        'ssm': ssm,
        'sdi': sdi,
        'parity': parity,
        'parity_valid': parity_valid
    }
    
    print(f"\nDecoded result: {result}")
    return result

# Test the encoder/decoder
if __name__ == "__main__":
    print("ARINC 429 Encoder/Decoder Example")
    print("=" * 50)
    
    # Simulate CNS data: Encode altitude 1000 ft with label 010 (octal)
    label = 0o010  # Common label for altitude
    altitude = 1000  # Simple data value (fits in 19 bits)
    
    print(f"Test Case: Encoding altitude data")
    print(f"Label 0o010 (octal 010) represents altitude data")
    print(f"Altitude value: {altitude} feet")
    
    # Encode
    encoded_word = encode_arinc429(label, altitude)
    
    print(f"\n" + "="*50)
    
    # Decode
    decoded = decode_arinc429(encoded_word)
    
    print(f"\n" + "="*50)
    print(f"SUMMARY:")
    print(f"Original input: label={oct(label)}, data={altitude}")
    print(f"Encoded word: {encoded_word} (decimal), {hex(encoded_word)} (hex)")
    print(f"Decoded output: label={oct(decoded['label'])}, data={decoded['data']}")
    print(f"Round-trip successful: {label == decoded['label'] and altitude == decoded['data']}")