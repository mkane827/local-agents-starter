import ollama

def main():
    print("🤖 Prompting local Gemma 2 (9B) via Ollama...")
    response = ollama.chat(
        model="gemma2:9b",
        messages=[
            {
                "role": "user",
                "content": "Give a 1-sentence welcome message for a developer building a local AI agent ecosystem on macOS."
            }
        ]
    )
    print("\nResponse from Gemma 2:")
    print("-" * 50)
    print(response['message']['content'])
    print("-" * 50)

if __name__ == "__main__":
    main()
