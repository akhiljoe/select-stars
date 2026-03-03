import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
# load_dotenv()
# client = OpenAI()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not set in Mac environment variables.")

client = OpenAI(api_key=api_key)


def extract_sql_and_save(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".jpg"):
            input_path = os.path.join(input_folder, file_name)

            with open(input_path, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Extract only the valid SQL query from the image. "
                            "Ignore company names, titles, explanations, "
                            "and any non-SQL text. Return only SQL."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract only the SQL query."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0
            )

            sql_text = response.choices[0].message.content.strip()

            # Create output filename with .txt extension
            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(output_folder, f"{base_name}.txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(sql_text)

            print(f"Saved: {output_path}")


# if __name__ == "__main__":
#     input_folder = "/Users/ajoe01/Documents/tim/select-stars/images"
#     output_folder = "/Users/ajoe01/Documents/tim/select-stars/solution"

#     extract_sql_and_save(input_folder, output_folder)