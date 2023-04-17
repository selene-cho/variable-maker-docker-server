from django.conf import settings
import openai

# openai.api_key = settings.OPENAI_API_KEY
openai.api_key = "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"


response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Give me the abbreviation of the word 'teacher' as a multi-numbered list",
    temperature=0,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

print(response)
print(response["choices"][0]["text"])
