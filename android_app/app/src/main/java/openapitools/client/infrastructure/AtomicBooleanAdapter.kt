package openapitools.client.infrastructure

import kotlinx.serialization.KSerializer
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.SerialDescriptor
import java.util.concurrent.atomic.AtomicBoolean

object AtomicBooleanAdapter : KSerializer<AtomicBoolean> {
    override fun serialize(encoder: Encoder, value: AtomicBoolean) {
        encoder.encodeBoolean(value.get())
    }

    override fun deserialize(decoder: Decoder): AtomicBoolean = AtomicBoolean(decoder.decodeBoolean())

    override val descriptor: SerialDescriptor = PrimitiveSerialDescriptor("AtomicBoolean", PrimitiveKind.BOOLEAN)
}
