# A Simple Quiz Bot
simple quiz on discord, using images as questions/results and emojis for answers

## Loading a game
`uv run quiz_loader.py <path/to/sqlite.db> <config.json>`

The config JSON should respect the following structure :
    {
      "gamemaster": "", //should be the gamemaster ID in the server's sqlite db
      "choices": [
        "✅",
        "❌" //emojis (at least 2)
      ],
      "questions": {
        "build/question_1.jpg": ["build/answer_1.jpg", "✅"], //"path/to/question.jpg": ["path/to/answer.jpg", "answer emoji"]
        "build/question_2.jpg": ["build/answer_2.jpg", "❌"],
        "build/question_3.jpg": ["build/answer_3.jpg", "✅"]
      }
    }
