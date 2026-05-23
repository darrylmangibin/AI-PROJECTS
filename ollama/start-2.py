import ollama

# response = ollama.list()

# print(response)

# CHAT
# res = ollama.chat(
#   model='gpt-oss:120b-cloud',
#   messages=[
#     {
#       'role': 'user',
#       'content': 'Why is the ocean salty?',
#     },
#   ],
#   stream=True,
# )

# for chunk in res:
#     print(chunk.message.content, end='', flush=True)