# family_bot

Telegram bot

Features:
  return some quote in English or Russian:
    commands:
      '/quote' # returns quote in English
      '/quote ru' # returns quote in Russian
  save and provide information about portfolio:
    commands:
      '/portfolio' # returns profit/loss for current portfolio in total
      '/portfolio symbol' # returns profit/loss for specified symbol if it's presented in portfolio
      '/save symbol yyyy-mm-dd spendings quantity' # save new opened position in the portfolio
