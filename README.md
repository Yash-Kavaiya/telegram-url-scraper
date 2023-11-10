<p><a target="_blank" href="https://app.eraser.io/workspace/DZvq2s69MfoqKOuegzD0" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

Cloud Run :- https://telegram-url-extracter-wuv6jff7zq-de.a.run.app
# Telegram url scraper

This repository provides a set of tools to extract urls your Telegram chat history. You can use this tool to export your Telegram user, group, or chat history in JSON format, extract text messages, and  it can help you extract all available URLs in Telegram and generate a CSV file for further analysis.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Exporting Telegram Data](#exporting-telegram-data)
- [Usage](#usage)
  - [Extracting URLs and Creating a CSV](#extracting-urls-and-creating-a-csv)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before using this tool, ensure you have the following installed on your system:

- [Telegram Desktop](https://desktop.telegram.org/)
- [Python](https://www.python.org/) (version 3.7 or higher)
- The required Python packages (you can install them using `pip`):
  - `pandas` for handling data and creating CSV files.

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

### Extracting urls

To extract text messages from the exported Telegram data and create a word cloud, run the following command:

```bash
python app.py -i result.json
```

Replace `path/to/your/result.json` with the path to your exported Telegram chat history JSON file. This command will generate a word cloud image based on the text messages found in the chat history.

## Contributing

If you have improvements or additional features to add to this project, feel free to contribute. Please follow the standard GitHub Fork and Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
