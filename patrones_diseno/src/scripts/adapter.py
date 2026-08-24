from __future__ import annotations

from typing import Protocol


class Notificador(Protocol):
    def enviar(self, destinatario: str, mensaje: str) -> bool: ...


class SMSGatewayLegacy:
    """Simula una librería externa de SMS, con su propia API distinta."""

    def send_message(self, to_number: str, body: str, priority: int = 1) -> int:
        print(
            f"[SMSGatewayLegacy] Enviando SMS a {to_number}: '{body}' (prioridad {priority})"  # noqa: E501
        )
        return 200


class EmailServiceExterno:
    """Otra librería externa distinta, con OTRA forma de hacer lo mismo."""

    def deliver(self, address: str, subject: str, content: str) -> dict:
        print(
            f"[EmailServiceExterno] Enviando email a {address}: [{subject}] {content}"
        )
        return {"status": "sent", "id": "abc123"}


# ---------------------------------------------------------------
# 3. LOS ADAPTERS -- traducen cada interfaz incompatible
#    hacia la interfaz común que tu código espera (Notificador)
# ---------------------------------------------------------------


class SMSAdapter:
    """Adapta SMSGatewayLegacy para que cumpla el contrato Notificador."""

    def __init__(self, gateway: SMSGatewayLegacy):
        self._gateway = gateway

    def enviar(self, destinatario: str, mensaje: str) -> bool:
        # aquí ocurre la "traducción": nombres de parámetros distintos,
        # y un código de estado numérico que convertimos a bool
        codigo = self._gateway.send_message(to_number=destinatario, body=mensaje)
        return codigo == 200


class EmailAdapter:
    """Adapta EmailServiceExterno para que cumpla el mismo contrato Notificador."""

    def __init__(self, servicio: EmailServiceExterno):
        self._servicio = servicio

    def enviar(self, destinatario: str, mensaje: str) -> bool:
        # esta librería pide "subject" además de "content"
        #  lo resolvemos aquí adentro,
        # el código cliente nunca se entera de este detalle
        resultado = self._servicio.deliver(
            address=destinatario,
            subject="Notificación",
            content=mensaje,
        )
        return resultado["status"] == "sent"


# ---------------------------------------------------------------
# 4. CÓDIGO CLIENTE -- solo conoce Notificador, nunca las clases
#    externas ni sus interfaces particulares
# ---------------------------------------------------------------


def notificar_usuario(
    notificador: Notificador, destinatario: str, mensaje: str
) -> None:
    exito = notificador.enviar(destinatario, mensaje)
    estado = "enviado correctamente" if exito else "FALLÓ el envío"
    print(f"  -> {estado}\n")


if __name__ == "__main__":
    sms_adapter = SMSAdapter(SMSGatewayLegacy())
    email_adapter = EmailAdapter(EmailServiceExterno())

    print("Notificando por SMS:")
    notificar_usuario(sms_adapter, "555-1234", "Tu pedido fue enviado")

    print("Notificando por Email:")
    notificar_usuario(email_adapter, "ana@mail.com", "Tu pedido fue enviado")
