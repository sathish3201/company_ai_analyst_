import pytest

from company_ai.voice.stt import SpeechToTextService
from company_ai.voice.tts import TextToSpeechService


@pytest.mark.asyncio
async def test_stt_not_configured():

    service = SpeechToTextService()

    with pytest.raises(
        NotImplementedError,
        match="STT provider",
    ):
        await service.transcribe(
            b"audio"
        )


@pytest.mark.asyncio
async def test_tts_not_configured():

    service = TextToSpeechService()

    with pytest.raises(
        NotImplementedError,
        match="TTS provider",
    ):
        await service.synthesize(
            "Hello"
        )