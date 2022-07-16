# Optimized for song lyrics for the moment

if __name__ == '__main__':
    import argparse
    import html
    import random
    import genanki


    parser = argparse.ArgumentParser(description='Convert a text file to Anki cards to learn it.')
        # Add help argument
    parser.add_argument('output', type=str, default=None, help='Anki .apkg file to write')
    parser.add_argument('deck_name', type=str, default=None, help='Name of deck')
    parser.add_argument('--input', type=str, default=None, help='File to read')


    args = parser.parse_args()
    if args.input is None:
        import sys
        args.input = sys.stdin
    else:
        args.input = open(args.input, 'r')

    model = genanki.Model(
        random.randrange(1<<30, 1<<31),
        'Basic Model',
        fields=[{'name': 'Front'}, {'name' :'Back'}],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{FrontSide}}\n\n<hr id="answer">\n\n{{Back}}',
            }
        ])

    deck = genanki.Deck(
        random.randrange(1<<30, 1<<31),
        args.deck_name)

    # Read file
    lines = args.input.readlines()
    # Remove and clean empty lines
    lines = [line.strip() for line in lines if line.strip()]
    # Add two lines at the beginning of the file
    lines = ['--BEGIN--', '-------'] + lines

    # Create a list of pairs, where the second element is
    # a word in the lines, and the first element is a string
    # consisting of the two previous lines and the previous
    # words on that line.

    # Initialize the list
    # Loop over the lines
    for i in range(2, len(lines)):
        # Get the current line
        line = lines[i]
        # Get and join the two previous lines
        prev_lines = '\n'.join(lines[i-2:i])
        # For each word in the current line
        words = line.split()
        for j in range(0,len(words)):
            # Get the current word
            word = words[j]
            # Get the previous words
            prev_words = ' '.join(words[:j])

            front = prev_lines + '\n' + prev_words
            back = word
            # Convert to html
            front = html.escape(front).replace('\n', '<br>')
            back = html.escape(back).replace('\n', '<br>')

            # Add a note
            note = genanki.Note(model=model, fields=[front, back])
            deck.add_note(note)

    genanki.Package(deck).write_to_file(args.output)