def read_in_corpus(filename):
    """
    Read and format corpus for consumption. returns a list of strings
    """
    with open(filename) as file_content:
        # unsure if strig is correct
        return [x.lower().strip() for x in file_content.readlines()]