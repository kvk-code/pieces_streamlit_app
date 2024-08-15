### `README.md`

```markdown
# Pieces Copilot Streamlit Bot

This project is a Streamlit application that integrates with the Pieces Copilot SDK to create an interactive chat interface. Users can start new conversations, view past conversations, and interact with the Pieces Copilot.

## Features

- Start new conversations
- View past conversations
- Clear current conversation
- Get conversation history
- Interactive chat interface

## Installation

1. Clone the repository:
    ```sh
    git clone hhttps://github.com/kvk-code/pieces_streamlit_app.git
    cd pieces_streamlit_app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run pieces_bot_kvk.py
    ```

2. Open your web browser and go to `http://localhost:8501` to interact with the bot.

## Files

- `pieces_bot_kvk.py`: Main application logic.
- `pieces_bot_sample.py`: Sample application logic.
- `.gitignore`: Git ignore file to exclude virtual environment directories.

## Acknowledgements

The main logic implemented in `pieces_bot_kvk.py` and `pieces_bot_sample.py` is inspired by the example provided at [https://github.com/shivay-at-pieces/pieces_copilot_streamlit_example](https://github.com/shivay-at-pieces/pieces_copilot_streamlit_example).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```