import re
import base64

def find_base64_for_variables(lines):
    decoded_values = []

    for line in reversed(lines):
        # Find variables starting with $
        variable_matches = re.findall(r'\$(\w+)', line)

        for variable in variable_matches:
            # Construct regex pattern for Base64 in PowerShell format
            base64_pattern = re.compile(rf'{variable}\s*=\s*\[System\.Text\.Encoding\]::ASCII\.GetString\(\[System\.Convert\]::FromBase64String\("([A-Za-z0-9+/=]+)"\)\);')

            # Search for Base64 pattern in the line
            base64_match = base64_pattern.search(line)

            if base64_match:
                base64_value = base64_match.group(1)

                # Decode Base64 value
                decoded_value = base64.b64decode(base64_value).decode('utf-8')

                # Store decoded value
                decoded_values.append(decoded_value)

    # Concatenate values with commas between every two lines
    concatenated_values = ", ".join(decoded_values[i] + ", " + decoded_values[i + 1] for i in range(0, len(decoded_values), 2))

    # Print concatenated values
    print("Concatenated Values (bottom to top with commas between every two lines):")
    print(concatenated_values)

# Example usage:
lines = ['''
    $zywpappkth=[System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String("ZG5wbWhsNV94WXpmMHVMLWNsa0p6Z2dYQ1N3IC0xMDAxMzIyMzI5NDU2IHF1eWV0"));,
    $var2 = [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String("SGVsbG8gd29ybGQ="));
''']

find_base64_for_variables(lines)