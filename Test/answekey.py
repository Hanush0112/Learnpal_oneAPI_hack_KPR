def extract_letters(word):
    # Extract the number of characters to read from the last two digits
    num_chars = int(word[-2:])

    # Determine the starting index (3rd last position)
    start_index = len(word) - 3

    # Initialize an empty list to store valid characters
    valid_letters = []

    # Loop backwards from the starting index
    while len(valid_letters) < num_chars and start_index >= 0:
        # Check if the current character is 'a', 'b', 'c', or 'd'
        if word[start_index] in {'a', 'b', 'c', 'd'}:
            valid_letters.append(word[start_index])

        # Move to the next character
        start_index -= 1

    # Return the list of valid letters (in the original order)
    return valid_letters[::-1]
