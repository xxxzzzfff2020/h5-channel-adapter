"""Read PNG/JPEG/WebP dimensions without FFmpeg; not a full pixel decoder."""
import struct
import zlib

IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp'}


def image_probe(path):
    """Bound header inspection to 1 MiB; never allocate a decoded pixel buffer."""
    try:
        with path.open('rb') as stream:
            data = stream.read(1024 * 1024)
        width, height, codec = dimensions(data)
        if width <= 0 or height <= 0:
            raise ValueError('Invalid image dimensions')
        return {'method': 'image_header', 'streams': [
            {'codec_type': 'video', 'codec_name': codec, 'width': width, 'height': height}],
            'not_checked': ['full pixel decoding', 'visual quality']}
    except (OSError, ValueError, struct.error) as error:
        return {'method': 'image_header', 'error': str(error)}


def dimensions(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        if len(data) < 33 or data[8:16] != b'\x00\x00\x00\rIHDR':
            raise ValueError('Invalid PNG header')
        if zlib.crc32(data[12:29]) != int.from_bytes(data[29:33], 'big'):
            raise ValueError('Invalid PNG header CRC')
        width, height = struct.unpack('>II', data[16:24])
        return width, height, 'png'
    if data.startswith(b'\xff\xd8'):
        offset = 2
        # SOF markers containing dimensions; exclude DHT, JPG and DAC.
        sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
               0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
        while offset < len(data):
            if data[offset] != 0xFF:
                raise ValueError('Invalid JPEG marker')
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            if offset >= len(data):
                break
            marker = data[offset]
            offset += 1
            if marker in {0xDA, 0xD9}:
                break
            if marker == 0x01 or 0xD0 <= marker <= 0xD7:
                continue
            if offset + 2 > len(data):
                break
            size = int.from_bytes(data[offset:offset + 2], 'big')
            if size < 2 or offset + size > len(data):
                break
            if marker in sof:
                if size < 8:
                    raise ValueError('Invalid JPEG frame header')
                height, width = struct.unpack('>HH', data[offset + 3:offset + 7])
                return width, height, 'mjpeg'
            offset += size
        raise ValueError('JPEG dimensions missing or beyond header scan limit')
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        offset = 12
        container_end = int.from_bytes(data[4:8], 'little') + 8
        while offset + 8 <= min(len(data), container_end):
            kind = data[offset:offset + 4]
            size = int.from_bytes(data[offset + 4:offset + 8], 'little')
            start = offset + 8
            if start + size > container_end:
                raise ValueError('Invalid WebP chunk size')
            header = data[start:start + min(size, 10)]
            if kind == b'VP8X' and size == 10 and len(header) == 10:
                return (1 + int.from_bytes(header[4:7], 'little'),
                        1 + int.from_bytes(header[7:10], 'little'), 'webp')
            if kind == b'VP8L' and len(header) >= 5 and header[0] == 0x2F:
                bits = int.from_bytes(header[1:5], 'little')
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1, 'webp'
            if kind == b'VP8 ' and len(header) >= 10 and header[3:6] == b'\x9d\x01\x2a':
                width, height = struct.unpack('<HH', header[6:10])
                return width & 0x3FFF, height & 0x3FFF, 'webp'
            offset = start + size + (size % 2)
        raise ValueError('WebP dimensions missing or beyond header scan limit')
    raise ValueError('Unsupported image header; expected PNG, JPEG or WebP')
