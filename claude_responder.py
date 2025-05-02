#!/usr/bin/env python3
import sys
import os
import json
import requests
import anthropic

def get_claude_response(message, personality):
    # Dictionary of personality prompts
    personalities = {
        "pirate": "Respond like a silly pirate captain, using pirate slang, sea metaphors, and saying 'arr' frequently.",
        "shakespeare": "Respond in Shakespearean English with thees, thous, and poetic flair.",
        "cowboy": "Respond like a Wild West cowboy with lots of Western slang and frontier wisdom.",
        "surfer": "Respond like a laid-back surfer dude from California, very chill and using surf lingo.",
        "corporate": "Respond with excessive corporate jargon, buzzwords, and meaningless business speak.",
        "medieval": "Respond like a chivalrous medieval knight on a noble quest.",
        "wizard": "Respond like a wise, eccentric wizard from a fantasy realm.",
        "robot": "Respond like a literal-minded robot trying to understand human emotions.",
        "yoda": "Respond with wisdom but in reversed sentence structure like Yoda.",
        "victorian": "Respond like a proper Victorian-era gentleman or lady with extreme politeness."
    }

    # Get the prompt based on personality or use a default
    prompt_instruction = personalities.get(
        personality.lower(),
        "Respond in a fun, playful way."
    )

    # Claude API setup
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    try:
        message = f"""
        Respond to this Teams message in a playful way.

        Instructions: {prompt_instruction}

        Keep your response concise (1-3 sentences) and make sure it's appropriate for a workplace.

        Original message: {message}
        """

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            system="You are a helpful and playful assistant that responds to messages in the style specified.",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return response.content[0].text

    except Exception as e:
        return f"Error generating response: {str(e)}"

if __name__ == "__main__":
    # Get input from Alfred
    if len(sys.argv) < 3:
        print("Error: Missing arguments. Need message and personality type.")
        sys.exit(1)

    message = sys.argv[1]
    personality = sys.argv[2]

    response = get_claude_response(message, personality)
    print(response)