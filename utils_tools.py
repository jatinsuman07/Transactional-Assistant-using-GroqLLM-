from utils import create_new_account, check_balance, credit_amount, debit_amount, user_complaint, pay_insurance, get_payment_history
import json
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
client = Groq()
MODEL = 'meta-llama/llama-4-scout-17b-16e-instruct'

prompt = """
    you are BankMitra, an assistant that helps users to perform transactions tasks
    user can ask for 6 tasks - create account, credit, debit, check balance, pay insurance, register complaint, get payment history.
    be nice, polite and friendly. keep the sentence around 2-3 sentences as needed.
    they might ask you for any of these task, 
    Give a friendly response with the options if they have not picked any of these. 

"""


def call_llm(user_prompt):
    messages = [
        {
            "role":"system",
            "content":prompt
        },
        {
            "role":"user",
            "content":user_prompt
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_new_account",
                "description": "Takes an user's name and create a new account.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of new account holder."
                        }
                    },
                    "required": ["name"]
                },
            },
        },
        {
            "type":"function",
            "function":{
                "name":"check_balance",
                "description":"Takes an account number and returns the account balance.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "account_number":{
                            "type":"integer",
                            "description":"The account number to check balance for."
                        }
                    },
                    "required":["account_number"]
                },
            },
        },
        {
            "type":"function",
            "function":{
                "name":"credit_amount",
                "description":"Takes an account number and amount then add that amount to the balance of that account",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "account_number":{
                            "type":"integer",
                            "description":"The account number to add amount to."
                        },
                        "amount":{
                            "type":"integer",
                            "description":"The amount we want to credit."
                        }
                    },
                    "required": ["account_number", "amount"]
                }
            },
        },
        {
            "type":"function",
            "function":{
                "name":"debit_amount",
                "description":"Takes an account number and amount then debit that amount from the balance of that account",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "account_number":{
                            "type":"integer",
                            "description":"The account number to debit amount from"
                        },
                        "amount":{
                            "type":"integer",
                            "description":"The amount we want to debit"
                        }
                    },
                    "required":["account_number","amount"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "user_complaint",
                "description": "Takes an account number and issue from user and add that issue in complaint file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {
                            "type": "integer",
                            "description": "The account number to debit amount from"
                        },
                        "issue": {
                            "type": "string",
                            "description": "The issue user complaint about"
                        }
                    },
                    "required": ["account_number", "issue"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "pay_insurance",
                "description": "Takes an account number and pay insurance amount from balance of that account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {
                            "type": "integer",
                            "description": "The account number to debit amount from"
                        },
                    },
                    "required": ["account_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_payment_history",
                "description": "Takes an account number return payment history of that account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {
                            "type": "integer",
                            "description": "The account number to debit amount from"
                        }
                    },
                    "required": ["account_number"]
                }
            }
        }
    ]

    # This is how you make a chat request to the model. You're telling the LLM:
        # “Here’s a conversation (messages) and a list of tools it can use. Respond accordingly.”

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice= "auto",
        max_tokens = 4096
    )

    response_message = response.choices[0].message
    print(response_message)

    tool_calls = response_message.tool_calls  # finds if there is a tool call
    if tool_calls:
        available_functions = {
            "create_new_account": create_new_account,
            "check_balance": check_balance,
            "credit_amount": credit_amount,
            "debit_amount": debit_amount,
            "user_complaint": user_complaint,
            "pay_insurance":pay_insurance,
            "get_payment_history":get_payment_history
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(f"Tool call: {function_name}, Arguments: {function_args}")
            if function_name == "create_new_account":
                function_response = function_to_call(
                    name= function_args.get("name")
                )
            elif function_name == "check_balance":
                function_response = function_to_call(
                    account_number= function_args.get("account_number")
                )
            elif function_name == "credit_amount":
                function_response = function_to_call(
                    account_number= function_args.get("account_number"),
                    amount = function_args.get("amount")
                )
            elif function_name == "debit_amount":
                function_response = function_to_call(
                    account_number=function_args.get("account_number"),
                    amount=function_args.get("amount")
                )
            elif function_name == "user_complaint":
                function_response = function_to_call(
                    account_number=function_args.get("account_number"),
                    issue = function_args.get("issue")
                )
            elif function_name == "pay_insurance":
                function_response = function_to_call(
                    account_number=function_args.get("account_number")
                )
            elif function_name == "get_payment_history":
                function_response = function_to_call(
                    account_number=function_args.get("account_number")
                )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content



