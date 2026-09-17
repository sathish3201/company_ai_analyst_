from company_ai.contracts.voice import TextToSpeechPort


class TextToSpeechService(TextToSpeechPort):

    async def synthesize(
        self,
        text: str,
    ) -> bytes:

        raise NotImplementedError(
            "TTS provider has not been configured."
        )