from abc import ABC, abstractmethod


class SpeechToTextPort(ABC):

    @abstractmethod
    async def transcribe(
        self,
        audio: bytes,
    ) -> str:
        raise NotImplementedError


class TextToSpeechPort(ABC):

    @abstractmethod
    async def synthesize(
        self,
        text: str,
    ) -> bytes:
        raise NotImplementedError