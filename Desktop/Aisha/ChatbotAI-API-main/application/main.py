from RAG.bot import ask

for i in ask(user_input="Who are you", session_id='222',company_name="Osnova"):
  print(i)