# updated by ...: Loreto Notarantonio
# Version ......: 11-06-2020 16.14.15


from . LnLogger import setLogger
from . LnColor  import LnColor as Color
from . import LnMonkeyFunctions # per Path.LnCopy, Path.LnBackup
from . LnPrompt import (prompt, set_prompt); set_prompt(Color)
