import storage.device
from trezor import wire
from trezor.messages.Success import Success
from trezor.messages.WebAuthnAddResidentCredential import WebAuthnAddResidentCredential
from trezor.ui.layouts import not_cancelled, show_error

from apps.common.confirm import require_confirm

from .confirm import ConfirmContent, ConfirmInfo
from .credential import Fido2Credential
from .resident_credentials import store_resident_credential

if False:
    from typing import Optional


class ConfirmAddCredential(ConfirmInfo):
    def __init__(self, cred: Fido2Credential):
        super().__init__()
        self._cred = cred
        self.load_icon(cred.rp_id_hash)

    def get_header(self) -> str:
        return "Import credential"

    def app_name(self) -> str:
        return self._cred.app_name()

    def account_name(self) -> Optional[str]:
        return self._cred.account_name()


async def add_resident_credential(
    ctx: wire.Context, msg: WebAuthnAddResidentCredential
) -> Success:
    if not storage.device.is_initialized():
        raise wire.NotInitialized("Device is not initialized")
    if not msg.credential_id:
        raise wire.ProcessError("Missing credential ID parameter.")

    try:
        cred = Fido2Credential.from_cred_id(bytes(msg.credential_id), None)
    except Exception:
        await not_cancelled(
            show_error(
                ctx,
                "warning_credential",
                header="Import credential",
                button="Close",
                content="The credential you are trying to import does\nnot belong to this authenticator.",
                red=True,
            )
        )
        raise wire.ActionCancelled

    content = ConfirmContent(ConfirmAddCredential(cred))
    await require_confirm(ctx, content)

    if store_resident_credential(cred):
        return Success(message="Credential added")
    else:
        raise wire.ProcessError("Internal credential storage is full.")
