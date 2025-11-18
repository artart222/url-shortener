ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encoder(input_number: int) -> str:
    output_number: str = ""
    while input_number > 0:
        reminder = (input_number % 62)
        output_number = ALPHABET[reminder] + output_number
        input_number //= 62
    return output_number
