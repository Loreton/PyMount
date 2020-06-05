# updated by ...: Loreto Notarantonio
# Version ......: 05-06-2020 14.26.39

from pathlib import Path


# per evitare errori applicandosi su diversi progetti
def _exists(filename):
    _this_path=Path(__file__).absolute().parent
    return Path(_this_path / filename).exists()

if _exists('LnLogger.py'):          from . LnLogger import setLogger
if _exists('LnColor.py'):           from . LnColor  import LnColor as Color
if _exists('LnMonkeyFunctions.py'): from . import LnMonkeyFunctions # per Path.LnCopy, Path.LnBackup
if _exists('AES_EncDecrypt.py'):    from . AES_EncDecrypt import (AesEncrypt, AesDecrypt)
if _exists('LnPrompt.py'):
    from . LnPrompt import (prompt, set_prompt)
    set_prompt(Color)


# from . AES_EncDecrypt import (AesEncrypt, AesDecrypt)
# from . import LnMonkeyFunctions # per Path.LnCopy, Path.LnBackup
# from . LnColor  import LnColor as Color
# from . LnLogger import setLogger
# from . LnPrompt import (prompt, set_prompt); set_prompt(Color)

