import logging
# import azure.functions as func
# import re
import os
import base64
import requests
from openai import OpenAI


def generate_framed_notes(notes: str):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    prompt = f"""
    You are a release note assistant. Based strictly on the changelog input provided below, generate structured release notes in markdown.

    Do not add any assumptions, extrapolations, or additional content. Only use the information explicitly stated in the input.

    **Changelog Input:**
    {notes}

    Format your response as JSON with the following fields:
    - **version**: Extract the version number exactly as stated in the input.
    - **environment**: Extract the target environment (e.g., Production, Staging) exactly as mentioned.
    - **framed_notes**: A clear and concise markdown-formatted note that describes what is being changed, including any pre- or post-deployment considerations, **strictly based on the input provided**.
    """


    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick:free",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return completion.choices[0].message.content.strip()


def update_azure_wiki(version, environment, framed_notes):
    organization = os.getenv("AZURE_ORG")
    project = os.getenv("AZURE_PROJECT")
    wiki = os.getenv("AZURE_WIKI")
    pat = os.getenv("AZURE_PAT")

    encoded_pat = base64.b64encode(f":{pat}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_pat}",
        "Content-Type": "application/json"
    }

    markdown = f"# Release {version} to {environment}\n\n{framed_notes}"
    path = f"/Releases/{version}"

    url = f"https://dev.azure.com/{organization}/{project}/_apis/wiki/wikis/{wiki}/pages?path={path}&api-version=7.0"

    response = requests.put(url, headers=headers, json={"content": markdown})
    return response.status_code, response.text

# # def main(req: func.HttpRequest) -> func.HttpResponse:
# def main():
#     logging.info("Release note function triggered.")

#     try:
#         data = req.get_json()
#         message = data.get("text", "")

#         #version, environment, raw_notes = parse_message(message)
#         framed_notes = generate_framed_notes(message)
#         status, result = update_azure_wiki(version, environment, framed_notes)

#         if status == 200:
#             return func.HttpResponse(f"✅ Wiki updated for version {version}", status_code=200)
#         else:
#             return func.HttpResponse(f"❌ Failed to update wiki: {result}", status_code=500)

#     except Exception as e:
#         logging.error(str(e))
#         return func.HttpResponse(f"❌ Error: {str(e)}", status_code=500)


# to check the above code give me the starter code to run it in locally without functions

result = generate_framed_notes("""Deployed v5.3.0 to production.
This build brings the new notification system, improves audit logging, and updates the billing engine.
Hotfixes from the last sprint are also rolled in.""")
print(result)