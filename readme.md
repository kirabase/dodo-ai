# HyperShell 🤖 - Your AI Command Line Assistant

HyperShell is a smart command-line tool that effortlessly generates and executes shell commands for you, using natural language descriptions. It harnesses the power of moderl AI tools (OpenAI's ChatGPT and Anthropic's Claude) to understand your requirements and provides you with the appropriate Shell command and explanation.

![HyperShell demo](assets/dodo-demo.gif)

🌟 Features

| Intuitive                                                                                                                                | Knowledge Hub                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 💬 _Conversational UI_: Effortlessly generate complex commands from simple conversational requests, with multi-language support.         | 🎓 _Tutoring_: Improve your command-line knowledge, with opportunities to explore in-depth learning and understand configurations. |
| 🔄 _Refinement_: Feel like you're having a conversation with your terminal as you refine and tweak commands to perfection.               | 🛠️ _Support for Popular Tools_: Master complex commands for Git, Docker, Npm, and a wide range of popular command-line tools.      |
| ✅ _Transparent_: Each command comes with a clear explanation, enabling you to validate the results ensuring it matches your intentions. | 🌐 _Universal_: Effortlessly adapt commands for any OS (Linux, macOS, Windows, and more) and shell (Bash, PowerShell, and more).   |
| 🌈 _Mutli-language_: Seamlessly switch between languages, making the command generation process an enjoyable multilingual experience.    | 😄 _Fun & Engaging_: Transform your command line experience into a more interactive, enjoyable, and productive endeavor!           |

HyperShell is designed to be compatible with a wide range of AI models, ensuring AI agnosticism. It seamlessly integrates with various ChatGPT models such as 3.5Turbo and GPT4. Additionally, it supports Claude from Anthropic, and it will continue to expand its compatibility as more models release their APIs to the public.

## Installation 📦

1 - Clone the repository, change to the project directory, and install the required dependencies:

```
git clone https://github.com/kirabase/hyper-shell.git && \
cd hyper-shell && \
pip install -r requirements.txt
```

Note: This installation guide assumes you're using macOS, Linux, or Windows with WSL (Windows Subsystem for Linux). For Windows without WSL, you may need to adjust the commands accordingly.

2 - Get your OpenAI API key:
_Note: The following procedure is specifically tailored for OpenAI's ChatGPT. However, as HyperShell is designed to support models from multiple vendors, you can follow a similar approach to enable Claude from Anthropic and other models as they release their APIs to the public._

HyperShell uses OpenAI to create its advanced behaviors, and it requires you to create an API key. To obtain an OpenAI API key, sign up for an account at [OpenAI](https://beta.openai.com/signup/) and navigate to the [API key](https://platform.openai.com/account/api-keys) section on your account page.

OpenAI API Costs and Free Usage: When you register an account, OpenAI provides a free tier with limited usage, requiring a credit card for verification. After exhausting the free tier, you'll need to choose a paid plan.
HyperShell uses GPT3.5, which will cost you a few cents a day. Monitor your API usage to avoid unexpected charges. For detailed pricing information, visit the [OpenAI Pricing page](https://openai.com/pricing).

3 - Set up your OpenAI API key:

If you want to try HyperShell just run it, the first time it will ask you for the key; if you don't want to do it at each session, HyperShell supports multiple ways to set the key:

_Option 1:_ Set the OPENAI_API_KEY environment variable with your OpenAI API key:

Add the following line at the end of your shell configuration file (.bashrc, .zshrc, or .bash_profile), replacing YOUR_OPENAI_API_KEY with your actual OpenAI API key:

```
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

After adding the line, restart your terminal or run source ~/.bashrc (or your shell config file), depending on the file you edited. The environment variable will now be available each time you open a new terminal session.

_Option 2:_ Create a config.ini file in the project directory, you can clone the teplate curated for you:

```
config_template.ini > config.ini
```

Open the config.ini file and search the line below; replace YOUR-OPENAI-KEY with your actual OpenAI API key:

```
[openai]
service_key = YOUR-OPENAI-KEY
```

This works under Linux and MacOS, adpat it if you use Windows or another OS.

4 - Create an alias for quick access

HyperShell becomes even more useful when it's easily accessible right when you need to generate or launch a command. To make it more convenient to run, create an alias.

To set up an alias, open your shell configuration file (.bashrc, .zshrc, or .bash_profile) and add the following line at the end, replacing /path/to/dodo-ai/dodo.py with the actual path to the project directory:

```
alias dodo="python /path/to/hyper-shell/dodo.py"
```

After adding the alias, restart your terminal or run source ~/.bashrc (or the appropriate shell config file).
Now you can use the HyperShell command directly:

```
$ dodo "List the names of files containing the words 'Artificial Intelligence'"

grep -l "Artificial Intelligence" *
This command uses the grep command to search for the string "Artificial Intelligence" in all files in the current directory. The -l option tells grep to only print the names of the files containing the match.
```

## Usage 📖

```
dodo "A verbal description of the command you'd like to run"
```

Replace your prompt with a natural language description of the task you want to perform.

### Command-line options

- -s, --short: Show only the generated command, without the explanation.
- -c, --coach: Show a very detailed explanation to learn and master your commands.
- -x, --execute: Execute the suggested command, the last one suggested if no prompt is provided.
- -r, --refine: Refine the command using a conversational flow.

## Examples 🧭

### Example 1: 🐣 Working with simple commands

A simple use case is to write what you want to achive if you don't remember the command;
Here for example is a way to ask to list all the directory in the current location.

```
$ dodo "list all the directories"
ls -d */

Explanation:

This command lists all the directories in the current working directory.

The arguments used work this way:
- ls is the command to list directory contents.
- -d option is used to list only directories.
- */ is a pattern that matches all directories in the current directory. The * is a wildcard that matches any character - and the / specifies that only directories should be matched.
```

You can then refine the command with the continue mode,
just pretend to continue the conversation with the terminal.

```
$ dodo -c "only the hidden ones"
ls -d .*/
This command lists all the hidden directories in the current working directory. The arguments used work this way:

 • ls is the command to list directory contents.
 • d option is used to list only directories.
 • .*/ is a pattern that matches all hidden directories in the current directory. The dot
   (.) matches hidden files or directories, and the * is a wildcard that matches any
   character. The / specifies that only directories should be matched.
```

### Example 2: 🐥 More advanced examples

The AI service behind is really smart and is able to work with many different components,
here is an example where it uses variable and math to address your request.

```
$ dodo "generate a random number between 1 and 1000"
echo $((RANDOM % 1000 + 1))

Explanation:

- The $(( )) syntax is used for arithmetic expansion in bash.
- $RANDOM is a built-in bash variable that generates a random integer between 0 and 32767.
- We use the modulo operator % to limit the range of the random number between 0 and 999.
- We add 1 to the result to shift the range to 1-1000.
- Finally, echo is used to print the random number to the terminal.
```

### Example 3: 🛠️ Generate command for any popular tool

The knowledge of the tools expands outside the core bash commands,
and is able to generate complex commands from any popular command-line tool as well.

Here are a few examples:

```
$ dodo "git command to print the date of the last modification saved in the local repository"
git log -1 --format=%cd
This command will print the date of the last commit made in the local repository.

The arguments used work this way:

 • git log is a command that shows the commit logs.
 • -1 option tells git to show only the latest commit.
 • --format=%cd option specifies the format of the output to be the commit date. %cd is a
   placeholder that represents the commit date in a specified format.
```

```
$ python dodo.py "use npm to install the last version of React"
npm install react@latest
This command uses npm, the package manager for Node.js, to install the latest version of
React. The install command is used to install a package, and react@latest specifies that we
want to install the latest version of the React package.
```

## The Roadmap head 🌈

We are committed to bringing monthly updates to HyperShell to explore the possibilities of AI-powered tools further. In our roadmap, we have several exciting features planned, including:

- **Support for Multiple LLMS**: We are working on expanding HyperShell's compatibility to include other popular Language Models like Bard and Cloude, offering you a wider range of options for generating commands.

- **Troubleshooting Mode**: We understand the frustration of encountering terminal errors and issues. That's why we are developing a dedicated troubleshooting mode to assist you in resolving problems faster and with more accuracy, providing step-by-step guidance.

- **Academy Mode**: We believe in continuous learning, and we're doubling down on it. The upcoming Academy mode will provide a comprehensive learning experience, with tutorials, exercises, and real-world examples to help you master the command-line and enhance your technical skills.

We're excited to evolve and improve HyperShell to meet your needs and make your command-line experience even more powerful and enjoyable.

## Disclaimer 🫢

HyperShell relies on AI services - like LLM from OpenAI and Anthropic - to generate shell commands from natural language descriptions. Please consider the following points when using this tool:

- The generated code might not always be accurate or run as intended. Always review the suggested commands before executing them, especially if they involve system-level operations or sensitive data.
- The natural language descriptions used to generate or refine commands are sent to these services. By using this tool, you acknowledge that your input data will be processed by API from OpenAI, Anthropic or any model you enabled. Please refer to services's data usage policy for more information about data privacy and retention.
- HyperShell uses 3rd party AI services, which will cost a very little for each command genearated: be aware on using this command on automations and monitor your API usage to avoid unexpected charges. For detailed pricing information visit the corresponding pricing pages of [OpenAI](https://openai.com/pricing), and [Anthropic](https://console.anthropic.com/account/pricing).
- This tool is provided "as is" without any warranties or guarantees of any kind. The author of this tool is not responsible for any damages or issues that may arise from using the generated commands.
- Always exercise caution and apply best practices when using generated commands in production or critical environments. Verify the functionality and security of the commands before deploying them.
- By using this tool, you agree to these terms and acknowledge the risks associated with using the generated commands.

## License 📄

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing 🥰

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to discuss any improvements or suggestions.

---

## Frequently Asked Questions 👨‍🏫

#### Q: 1. How does HyperShell work?

HyperShell utilizes a class for AI models called LLM: this allows the tool to understand natural language descriptions and generate shell commands. Note that LLMs are trained with knowledge up until a given date (I.e OpenAI's GPT-3.5 until mid-2021). So HyperShell generates assitance for tools and configurations built until that time.

#### Q: 3. Can HyperShell work with different operating systems and shells?

Yes, HyperShell understands the context and generates commands tailored to the specific shell and operating system. It adapts the commands to work seamlessly with different shells and OS environments.

#### Q: 4. How can HyperShell improve my command-line knowledge?

HyperShell is designed for continuous learning. It provides straightforward explanations with each command. Additionally, you can activate the "--coach mode" to ask for detailed tips and in-depth explanations, enhancing your understanding of command-line operations.

#### Q: 5. Is HyperShell able to refine and tweak commands?

Absolutely! HyperShell offers the "--refine mode," enabling you to iterate and modify commands through a conversational approach. You can refine and tweak commands until they meet your specific requirements.

#### Q: 6. Can HyperShell generate commands in multiple languages?

Yes, HyperShell supports multiple languages. You can seamlessly switch between languages during the command generation process, making it a multilingual and enjoyable experience.

#### Q: 7. Can I use HyperShell for very complex commands or command configurations?

Certainly! HyperShell is capable of generating commands and command configurations that range from simple to highly complex. It can handle intricate tasks and provide detailed command solutions.

#### Q: 8. Is HyperShell a free tool?

HyperShell itself is available for free usage. However, please note that you will be responsible for any charges incurred from the OpenAI API calls associated with using GPT-3.5 Turbo (or any other AI services and models supported by HyperShell).

#### Q: 9. Which AI Services are supported?

HyperShell currently supports a range of AI services, including various OpenAI LLM models such as ChatGPT, GPT4, and Claude-v1 from Anthropic. As new models and AI services are publicly released, HyperShell will continue to expand its support to accommodate them.
