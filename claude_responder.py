#!/usr/bin/env python3
import sys
import os
import re
import random
import json
import requests
import anthropic

short_response = False
force_short_response = True

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
        if short_response:
            requirements = "CRITICAL REQUIREMENT: Your response MUST be EXACTLY ONE SENTENCE. No exceptions."
        else:
            requirements = "Keep your response concise (1-3 sentences) and make sure it's appropriate for a workplace."

        message = f"""
        Respond to this Teams message in a playful way.

        Instructions: {prompt_instruction}

        {requirements}

        Original message: {message}
        """

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,  # Limit the length of the response
            system="You are a playful assistant that ALWAYS responds with EXACTLY ONE SENTENCE. No matter what, you must condense your entire response into a single sentence. If you respond with more than one sentence, you have failed.",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        if force_short_response:
            response_text = response.content[0].text.strip()
            # Split by period, exclamation, or question mark followed by space
            sentences = re.split(r'[.!?] ', response_text)
            # Return only one sentence with its punctuation
            return sentences[random.randint(0, len(sentences) - 1)] + ('.' if not sentences[0][-1] in '.!?' else '')
        else:
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