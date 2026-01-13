
import os

output_file = "debug_result.txt"
env_path = os.path.join(os.getcwd(), ".env")

with open(output_file, "w") as out:
    out.write(f"Current Working Directory: {os.getcwd()}\n")
    
    if os.path.exists(env_path):
        out.write(f"Scanning .env file at {env_path}...\n")
        with open(env_path, 'r') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    parts = line.split('=', 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    if key == "GOOGLE_CLIENT_ID":
                        out.write(f"FOUND: GOOGLE_CLIENT_ID\n")
                        out.write(f"Value length: {len(value)}\n")
                        is_empty = (value == "")
                        out.write(f"Is Empty?: {is_empty}\n")
                        has_quotes = value.startswith('"') or value.startswith("'")
                        out.write(f"Starts with quote?: {has_quotes}\n")
                    elif key == "GOOGLE_CLIENT_SECRET":
                        out.write(f"FOUND: GOOGLE_CLIENT_SECRET\n")
                        out.write(f"Value length: {len(value)}\n")
    else:
        out.write("CRITICAL: .env file NOT found!\n")
