# KingOnTheMars Tap Bot

A tap-to-earn Telegram bot integrated with the TON blockchain.

![kingonthemars](https://github.com/user-attachments/assets/d727fed1-a0fb-4b40-b3f2-ccc182aa3237)


## Project Description

KingOnTheMars Tap Bot is a Telegram bot that allows users to earn TON tokens by tapping. Users can set their TON wallet address and earn tokens based on their tapping activity. The bot implements a daily reward system with increasing reward amounts that reset every 30 days.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/BronzonTech-Cloud/king_on_the_mars_tap_bot.git
    cd king_on_the_mars_tap_bot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python -c "from database import create_db; create_db()"
    ```

5. Update `config.py` with your Telegram bot token and TON API key:
    ```python
    TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    TON_API_KEY = 'YOUR_TON_API_KEY'
    ```

6. Run the bot:
    ```bash
    python bot.py
    ```

7. Schedule the reward distribution:
    - Create a cron job to run `reward_scheduler.py` at regular intervals (if needed).

## Features

- **Tap-to-Earn:** Users can earn tokens by tapping commands.
- **Daily Rewards:** Users can claim daily rewards that increase by 1000 tokens each day, resetting after 30 days.
- **TON Wallet Integration:** Users can connect their TON wallet address to receive rewards.

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any improvements or new features.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE) file for details.
