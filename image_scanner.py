from PIL import Image, ExifTags
from pathlib import Path


def safe_value(value):
    """Return readable metadata without raw binary content."""

    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            return "[Binary metadata omitted]"

    if isinstance(value, str):
        value = value.replace("\x00", "").strip()

        # Avoid displaying other non-printable characters.
        if any(not ch.isprintable() for ch in value):
            return "[Non-text metadata omitted]"

        return value

    if isinstance(value, dict):
        return {
            str(k): safe_value(v)
            for k, v in value.items()
        }

    if isinstance(value, (tuple, list)):
        return [safe_value(v) for v in value]

    return value


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def clean_reference(value):
    if isinstance(value, bytes):
        value = value.decode("ascii", errors="ignore")

    return str(value).strip().upper()


def convert_gps(values, reference, maximum):
    """Convert EXIF DMS coordinates to decimal degrees."""

    if not values or len(values) != 3:
        return None

    degrees = to_float(values[0])
    minutes = to_float(values[1])
    seconds = to_float(values[2])

    if None in (degrees, minutes, seconds):
        return None

    if degrees < 0:
        return None

    if not (0 <= minutes < 60 and 0 <= seconds < 60):
        return None

    decimal = degrees + minutes / 60 + seconds / 3600

    ref = clean_reference(reference)

    if ref in ("S", "W"):
        decimal = -decimal
    elif ref not in ("N", "E"):
        return None

    if abs(decimal) > maximum:
        return None

    return round(decimal, 8)


def scan_image(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        return {"error": "File does not exist"}

    try:
        with Image.open(file_path) as image:

            result = {
                "filename": file_path.name,
                "format": image.format,
                "dimensions": image.size,
                "mode": image.mode,
                "metadata": {},
                "gps_found": False,
                "gps_coordinates": None,
                "maps_url": None
            }

            exif = image.getexif()

            # Extract ordinary EXIF fields.
            for tag_id, value in exif.items():

                tag_name = ExifTags.TAGS.get(
                    tag_id, str(tag_id)
                )

                # Internal pointers and GPS are handled separately.
                if tag_id in (0x8769, 0x8825):
                    continue

                # Avoid raw binary metadata.
                if tag_name in ("MakerNote", "UserComment"):
                    continue

                result["metadata"][tag_name] = safe_value(value)

            # Extract the EXIF sub-IFD.
            try:
                exif_ifd = exif.get_ifd(0x8769)

                for tag_id, value in exif_ifd.items():

                    tag_name = ExifTags.TAGS.get(
                        tag_id, str(tag_id)
                    )

                    if tag_name in ("MakerNote", "UserComment"):
                        continue

                    result["metadata"][tag_name] = safe_value(value)

            except Exception:
                pass

            # Extract GPS independently.
            try:
                gps = exif.get_ifd(0x8825)

                if gps:

                    result["gps_found"] = True

                    latitude = convert_gps(
                        gps.get(2),
                        gps.get(1),
                        90
                    )

                    longitude = convert_gps(
                        gps.get(4),
                        gps.get(3),
                        180
                    )

                    if latitude is not None and longitude is not None:

                        result["gps_coordinates"] = {
                            "latitude": latitude,
                            "longitude": longitude
                        }

                        result["maps_url"] = (
                            "https://www.google.com/maps?q="
                            f"{latitude},{longitude}"
                        )

            except Exception:
                pass

            return result

    except Exception as error:
        return {"error": str(error)}
