<p><a target="_blank" href="https://app.eraser.io/workspace/DZvq2s69MfoqKOuegzD0" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

# Telegram url scraper

This repository provides a set of tools to analyze your Telegram chat history. You can use this tool to export your Telegram user, group, or chat history in JSON format, extract text messages, and create a word cloud. Additionally, it can help you extract all available URLs in Telegram and generate a CSV file for further analysis.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Exporting Telegram Data](#exporting-telegram-data)
  - [Analyzing Telegram Data](#analyzing-telegram-data)
- [Usage](#usage)
  - [Extracting Text Messages and Creating Word Cloud](#extracting-text-messages-and-creating-word-cloud)
  - [Extracting URLs and Creating a CSV](#extracting-urls-and-creating-a-csv)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before using this tool, ensure you have the following installed on your system:

- [Telegram Desktop](https://desktop.telegram.org/)
- [Python](https://www.python.org/) (version 3.7 or higher)
- The required Python packages (you can install them using `pip`):
  - `telethon` for accessing Telegram data.
  - `wordcloud` for generating word clouds.
  - `pandas` for handling data and creating CSV files.

You can install the Python packages using the following command:

```bash
pip install telethon wordcloud pandas
```

## Getting Started

### Exporting Telegram Data

To export your Telegram chat history, follow these steps:

1. Install Telegram Desktop on your computer if you haven't already.

2. Open Telegram Desktop and log in with your account.

3. Go to the chat or group you want to export and click on the profile picture.

4. In the chat/group profile, click on the three vertical dots (⋮) in the top-right corner and select "Export chat history."

5. Choose the "JSON" format for exporting the chat history. Save the resulting `.json` file to a location on your computer.

### Analyzing Telegram Data

Clone this repository to your local machine and navigate to the repository directory.

```bash
git clone https://github.com/Yash-Kavaiya/telegram-url-scraper
cd telegram-url-scraper
```

## Usage

### Extracting Text Messages and Creating Word Cloud

To extract text messages from the exported Telegram data and create a word cloud, run the following command:

```bash
python app.py -i result.json
```

Replace `path/to/your/result.json` with the path to your exported Telegram chat history JSON file. This command will generate a word cloud image based on the text messages found in the chat history.

### Extracting URLs and Creating a CSV

To extract all available URLs from the Telegram data and generate a CSV file, run the following command:

```bash
python main.py -i path/to/your/result.json -o path/to/output/urls.csv
```

Replace `path/to/your/result.json` with the path to your exported Telegram chat history JSON file, and `path/to/output/urls.csv` with the desired location for the CSV output.

## Contributing

If you have improvements or additional features to add to this project, feel free to contribute. Please follow the standard GitHub Fork and Pull Request workflow.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
