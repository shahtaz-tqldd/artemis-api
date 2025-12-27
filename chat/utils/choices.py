from enum import Enum

class PLATFORMS(str, Enum):
  """
  Available Platform types
  """
  RESTRO = "restro"
  LOCKIT_TRADE = "lockit_trade"


class SENDER_OPTIONS(str, Enum):
  """
  Available sender options
  """
  USER = "user"
  AI = "ai"
