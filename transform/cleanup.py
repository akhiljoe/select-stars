import os
import re

# Folder containing your .txt files
folder_path = "/Users/ajoe01/Documents/tim/sql-practice/questions/"

# Regex patterns for lines to remove (add more if needed)
remove_patterns = [
    r"^Get the interview call:.*",
    r"^Join the community:.*",
    r"^𝐌𝐮𝐬𝐭 𝐓𝐫𝐲?.*",
    r"^hashtag?.*",
    r"^🔥 𝐈'𝗺 𝐩𝐨𝐬𝐭𝗶𝗻𝗴 𝐨𝐧𝐞 𝐒𝐐𝐋?.*",
    r".*https://lnkd\.in/.*$",
    r"^🤝Stay active?.*",
    r"^Previous days? SQL?.*",
    r"^▪️ .*",
    r"^𝐈'𝗺 𝐩𝐨𝐬𝐭𝗶𝗻𝗴 𝐨𝐧𝐞 𝐒𝐐𝐋 𝐢𝐧𝐭𝐞𝐫𝐯𝐢𝐞𝐰?.*",
    r".*[🔥💪✨⭐❣️🎯🚀].*"
]

compiled_patterns = [re.compile(p) for p in remove_patterns]

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        print(f"checking: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Keep only lines that don't match any unwanted pattern
        cleaned_lines = [
            line for line in lines
            if not any(p.match(line) for p in compiled_patterns)
        ]

        # Overwrite with cleaned content
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)

print("Regex-based cleaning completed!")
