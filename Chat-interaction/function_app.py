import azure.functions as func
import logging
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY"),
base_url=os.getenv("OPENAI_API_BASE"),
api_version=os.getenv("OPENAI_API_VERSION")

print(api_key)

# Azure OpenAI Credentials
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_version=os.getenv("OPENAI_API_VERSION")
)


deployment_name = os.getenv("DEPLOYMENT_NAME")

app = func.FunctionApp()

@app.function_name(name="ChatFunction")
@app.route(route="chat", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Chat request received.")

    try:
        req_body = req.get_json()
        user_input = req_body.get("message", "")

        if not user_input:
            return func.HttpResponse(
                json.dumps({"error": "Message input is required."}),
                mimetype="application/json",
                status_code=400
            )

        logging.info(f"Sending request to OpenAI with message: {user_input}")

        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": user_input}]
        )

        ai_response = completion.choices[0].message.content if completion.choices else "AI did not return a response."

        return func.HttpResponse(
            json.dumps({"response": ai_response}),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error encountered: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
