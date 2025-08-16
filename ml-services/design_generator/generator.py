# ml-services/design_generator/generator.py

import os
import json
from openai import OpenAI


class DesignGenerator:
    """
    Uses a large language model (like GPT) to generate upcycling design ideas
    based on predefined prompt templates.
    """

    def __init__(self, prompt_file_path=None):
        """
        Initializes the generator by setting up the OpenAI client and loading prompts.
        """
        # Load API key from environment variables for security
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.client = OpenAI(api_key=api_key)

        # Set default path for the prompts file if not provided
        if prompt_file_path is None:
            current_dir = os.path.dirname(__file__)
            prompt_file_path = os.path.join(current_dir, 'prompts/eco_prompts.txt')

        self.prompts = self._load_prompts(prompt_file_path)

    def _load_prompts(self, file_path: str) -> dict:
        """
        Loads and parses the prompt templates from a text file.
        It assumes prompts are separated by a line like '[PROMPT_ID]'.
        """
        prompts = {}
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Split prompts by their identifiers
            prompt_sections = content.split('[')[1:]  # Split and remove empty first element
            for section in prompt_sections:
                key, value = section.split(']', 1)
                prompts[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Warning: Prompt file not found at {file_path}")
            return {}
        return prompts

    def generate(self, waste_material: str, style: str = "modern", prompt_id: str = "PROMPT_1") -> dict:
        """
        Generates a design concept by calling the OpenAI API.

        Args:
            waste_material (str): The input waste material (e.g., "plastic bottles").
            style (str): The desired aesthetic style (e.g., "minimalist").
            prompt_id (str): The key of the prompt template to use.

        Returns:
            A dictionary containing the structured design idea.
        """
        prompt_template = self.prompts.get(prompt_id)
        if not prompt_template:
            return {"error": f"Prompt with ID '{prompt_id}' not found."}

        # Fill in the placeholders in the prompt template
        formatted_prompt = prompt_template.format(
            waste_material=waste_material,
            style=style
        )

        try:
            print("Sending request to OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "You are a creative and helpful assistant."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}  # Use JSON mode for reliable output
            )

            response_content = response.choices[0].message.content

            # The response content should be a JSON string, so we parse it
            design_idea = json.loads(response_content)
            return design_idea

        except Exception as e:
            print(f"An error occurred while calling OpenAI API: {e}")
            return {"error": "Failed to generate design from AI model."}


# Example usage:
if __name__ == "__main__":
    # Make sure to set your OPENAI_API_KEY as an environment variable
    # export OPENAI_API_KEY='your-key-here'
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set the OPENAI_API_KEY environment variable to run this example.")
    else:
        generator = DesignGenerator()
        design = generator.generate(waste_material="old denim jeans", style="rustic")

        # Pretty-print the JSON output
        print(json.dumps(design, indent=2))