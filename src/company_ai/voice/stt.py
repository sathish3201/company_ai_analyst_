from company_ai.contracts.voice import SpeechToTextPort


class SpeechToTextService(SpeechToTextPort):

    async def transcribe(
        self,
        audio: bytes,
    ) -> str:

        raise NotImplementedError(
            "STT provider has not been configured."
        )