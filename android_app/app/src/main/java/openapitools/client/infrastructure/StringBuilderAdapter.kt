package openapitools.client.infrastructure

import kotlinx.serialization.KSerializer
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.SerialDescriptor

object StringBuilderAdapter : KSerializer<StringBuilder> {
    override fun serialize(encoder: Encoder, value: StringBuilder) {
        encoder.encodeString(value.toString())
    }

    override fun deserialize(decoder: Decoder): StringBuilder = StringBuilder(decoder.decodeString())

    override val descriptor: SerialDescriptor = PrimitiveSerialDescriptor("StringBuilder", PrimitiveKind.STRING)
}
