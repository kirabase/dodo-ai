import json
import os
import re

import openai

from settings import config, OPEN_AI_KEY, LAST_CONVERSATION_FILE


def save_last_conversation(conversation: list):
    with open(LAST_CONVERSATION_FILE, "w") as f:
        json.dump(conversation, f)


def load_last_conversation():
    if os.path.exists(LAST_CONVERSATION_FILE):
        with open(LAST_CONVERSATION_FILE, "r") as f:
            return json.load(f)
    else:
        return []


# Set up your OpenAI API key
openai.api_key = OPEN_AI_KEY


# a class that is confifured with an ai prompt and can generate text
class HSInvalidRequest(Exception):
    pass

class Role:

    PANEL_TITLE = ''

    ROLE_PROMPT = []

    def __init__(self, refine: bool = False):
        self.refine = refine
        self.system_prompt = self._compile_prompt()[0]
        self._gen_command = None
        self._gen_explanations = []

    def _compile_prompt(self) -> list[str]:
        return [p.format(config=config) for p in self.ROLE_PROMPT]

    def _get_max_tokens(self) -> int:
        return 500

    def _get_generation_script(self, prompt: str) -> list:
        conversation = []

        if self.refine:
            conversation = load_last_conversation()
        else:
            conversation = [{"role": "system", "content": self.system_prompt}]

        conversation.append({"role": "user", "content": prompt})

        return conversation

    def _execute_script(self, script: list) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=config['openai']['service_model'],
                messages=script,
                max_tokens=self._get_max_tokens(),
                temperature=0.5,
            )
        except openai.error.RateLimitError:
            response_text = "Open AI service overloaded, try in a few minutes"
        else:
            response_text = response.choices[0].message['content'].strip()
        script.append({"role": "assistant", "content": response_text})

        return response_text
    
    def _parse(self, explanation: str):
        # Structured mode
        sections = re.split(r'(^|\n)\w+:', explanation)
        sections = [s.strip() for s in sections if s.strip()]

        if len(sections) == 2:
            self._gen_command = sections[0].replace('`', "").strip()
            self._gen_explanations = sections[1].strip()
            return

        # Resilient mode
        match = re.search(r'`([^`]+)`', explanation)
        if match:
            self._gen_command = match.group(1).strip()
            self._gen_explanations = explanation.strip()
            return

        # Skip mode
        raise HSInvalidRequest(explanation)    

    def execute(self, prompt: str):
        if prompt:
            script = self._get_generation_script(prompt)
            content = self._execute_script(script)
            save_last_conversation(script)
        else:
            content = load_last_conversation()[-1]["content"]
        
        self._parse(content)

    def get_command(self) -> str:
        return self._gen_command
    
    def get_explanations(self) -> list[dict]:
        #check if self._gen_explanations is a string
        if isinstance(self._gen_explanations, str):
            return [(self.PANEL_TITLE, self._gen_explanations)]
        return self._gen_explanations
    
class CompanionRole(Role):

    PANEL_TITLE = "Explanation"

    ROLE_PROMPT = [
    
    # System prompt
    '''You are a helpful assistant that translates human language descriptions to {config[env][shell_type]} commands on {config[env][os_type]}. Make sure to follow these guidelines:
 - Add an explanations in markdown to your commands: start with a generic description of the command, and add detalis in a bullet list if needed.
 - If a request doesn't make sense, still suggest a command and include guidance on how to fix it in the explanation.
 - Be capable of understanding and responding in multiple languages. Whenever the language of a request changes, change the language of your reply accordingly.

Examples: 
- Input: "List in a readable format all files in a directory"
- Output: "Command: ```ls -lh```\nExplanation: This command lists all files and directories in the current directory."

Input: "Search for 'artificial intelligence' words in all files in the current directory"
Output: "Command: ```grep -r "ciao" .```\nExplanation: grep is a command that searches for a given pattern in a file or directory.\n - r option tells grep to search recursively in all files and directories under the current directory.\n - "artificial intelligence" is the pattern we are searching for.\n - . specifies the current directory as the starting point of the search."

Input: "list all files here in a readable way" 
Output: "Command: ```ls -lh``\nExplanation: This command list all the files and directories in the current directory making the output more readable and informative.\n - ls is the command to list files and directories in the current directory.\n - The option -l (lowercase L) enables long format, which displays additional information such as file permissions, owner, size, and modification date.\n - The option -h (human-readable) makes the file sizes easier to read by displaying them in a format that uses units such as KB, MB, and GB."

Input: "Elenca in maniera leggibile tutti i file in questa directory"
Output: "Comando: ```ls```\nSpiegazione: Questo comando elenca tutti i file e le directory nella directory corrente."
''']

    def _get_max_tokens(self) -> int:
        return 250

class CoachRole(Role):
    
    PANEL_TITLE = "Advanced Explanation"

    ROLE_PROMPT =[
    
    # System prompt
    '''You are a helpful instructor that translates human language descriptions to {config[env][shell_type]} commands on {config[env][os_type]} and teach me how to use them in detail. 
about the output:
 - Format everything in markdown, each section starts with a title in h3 (###).
 - Be capable of understanding and responding in multiple languages. Whenever the language of a request changes, change the language of your reply accordingly.

In your reply, make sure to include these sections with corresponding title:
 - Explanation: Add a detailed explanation in markdown how what the command does. If a request doesn't make sense, help me what's wrong with it and how to fix it.
 - Detail: Break down the command into its individual components, such as flags, arguments, and subcommands, and provide explanations for each of them.
 - Common Mistakes: Highlight common mistakes or pitfalls associated with the command, and provide guidance on how to avoid them. This will help users execute the command correctly and prevent potential issues.
 - Examples: Include examples of how the command can be used in different contexts or scenarios. 
''',

    # Follow up prompt
    '''Ok! now write these sections:
 - Performance and Security", "Explain any performance or security implications associated with the command, such as potential resource usage or potential vulnerabilities.
 - Alternatives: Include different ways to performe the same task, with different commands or command configuration.
 - FAQs: Include a list of frequently asked questions and answers that address common concerns, misconceptions, or challenges faced by new command line users.
'''
]


    def _get_max_tokens(self) -> int:
        return 400


    def _parse(self, explanation: str):
        super()._parse(explanation)
        
        sections = []
        explanations = [s for s in explanation.split('###') if s.strip()]
        for e in explanations:
            title, content = e.split('\n', 1)
            sections.append((title.strip(), content))

        self._gen_explanations = sections


    def get_explanations(self) -> list[dict]:
        sections = super().get_explanations()
        explanations = ""
        for title, content in sections:
            explanations += f"\n\n{title.upper()}:\n\n{content.strip()}"
        
        return [(self.PANEL_TITLE, explanations)]
    