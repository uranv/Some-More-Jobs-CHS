import xml.etree.ElementTree as ET
import pandas as pd

def extract_settings_from_xml(file_path):
    results = []
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Iterate over all <li> elements with Class="XmlExtensions.Action.SetSetting"
    for li in root.findall(".//li[@Class='XmlExtensions.Action.SetSetting']"):
        may_require = li.get("MayRequire", "0")  # Default to '0' if MayRequire is not present
        # Extract the <key> and <value> elements
        key_elem = li.find("key")
        value_elem = li.find("value")
        if key_elem is not None and key_elem.text and value_elem is not None and value_elem.text:
            key_text = key_elem.text.strip()
            value_text = value_elem.text.strip()
            # Attempt to split the key into two main parts
            key_parts = key_text.split(".", 1)  # Split into two parts: prefix and the rest
            if len(key_parts) == 2:
                key_part1, key_part2 = key_parts
                results.append([key_part1, key_part2, value_text, may_require])
    return results

if __name__ == "__main__":
    file_path = "scr_action.xml"  # Replace with your XML file path
    extracted_data = extract_settings_from_xml(file_path)
    df = pd.DataFrame(extracted_data)
    df.to_csv('scr_action.csv', index=False, encoding='utf-8')