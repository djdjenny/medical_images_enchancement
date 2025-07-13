# Telegram Image Enhancement bot

This is the capstone project on DLS course part 1 (2025). The main idea of the project is to make a Telegram bot, which enhance medical images (CT or US images in particulary) quality via CycleGAN architecture.


## Project structure

```
telegram_bot/
├── bot.py
├── image_processing.py
├── image_handler.py
├── action_handler.py
├── config.py
├── model/
├── requirements.txt
├── Dockerfile
├── requirements.txt
├── Dockerfile
└── README.md
learning_notebooks/
├── model_training.ipynb
├── model_inference.ipynb
└── README.md
```

## How to install

### Clone the repo

```bash
git clone git@github.com:djdjenny/medical_images_enchancement.git
cd medical_images_enchancement
```

### Install dependencies

directly
```bash
pip install -r requirements.txt
```

or use docker
```bash
pip install -r requirements.txt
```

Due to the big model size, it should be downloaded from google drive and manually replaced to telegram-bot folder.

Bot is hosted on Hetzner VPS, HTTP endpoint obtained by ngrok.


# Model architecture and training
[AAPM challenge](https://www.aapm.org/)
[Ultrasound image enhancement challenge](https://ultrasoundenhance2023.grand-challenge.org/)
