NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'program': 'Bad input, please refer this spec-\n'
               'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/program_change.htm',
    'notes': 'Bad input, please refer this spec-\n'
             'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm'
}

def number_to_note(number: int) -> tuple:
    octave = number // NOTES_IN_OCTAVE
    assert octave in OCTAVES, errors['notes']
    assert 0 <= number <= 127, errors['notes']
    note = NOTES[number % NOTES_IN_OCTAVE]

    result = str(note + str(octave))
    print(result)
    return result


def note_to_number(note: str, octave: int) -> int:
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']

    return note
result = []
track = [80,76,80,76,80,76,81,80,78,80,76,80,76,80,76,81,80,78,76,73,76,73,76,73,76,75,76,78,81,78,81,78,81,78,83,81,80,81,78,81,78,81,78,83,81,80,81,78,81,78,81,78,81,80,81,83,80,76,80,76,80,76,81,80,78,80,76,80,76,80,76,81,80,78,76,73,76,73,76,73,76,75,76,78,81,78,81,78,81,78,83,81,80,81,78,81,78,81,78,83,81,80,81,78,81,78,81,78,81,80,81,83,83,79,83,79,83,79,84,83,81,83,79,83,79,83,79,84,83,81,79,76,74,79,76,79,76,79,78,79,81,84,81,84,81,84,81,86,84,83,84,81,84,81,84,81,86,84,83,84,83,81,84,81,84,81,84,83,84,86,82,87,86,84,86,87,82,79,80,82,80,79,77,75,79,77,82,91,92,91,89,87,89,91,89,86,89,87,84,86,87,80,79,75,77,79,80,79,82,80,79,77,77,73,77,73,77,73,78,77,75,77,73,75,77,73,77,73,78,77,75,73,70,73,70,73,70,73,72,73,75,78,75,78,75,78,75,80,78,77,78,75,78,75,78,75,80,78,77,78,75,78,75,78,75,78,77,78,80,80,76,80,76,80,76,81,80,78,80,76,80,76,80,76,81,80,78,76,73,76,73,76,73,76,75,76,78,81,78,81,78,81,78,83,81,80,81,78,81,78,81,78,83,81,80,81,78,81,78,81,78,81,80,81,83,83,79,83,79,83,79,84,83,81,83,79,83,79,83,79,84,83,81,79,76,79,76,79,76,79,78,79,81,84,81,84,81,84,81,86,84,83,84,81,84,81,84,81,86,84,83,84,81,84,81,84,81,84,83,84,86,82,87,86,84,86,87,82,79,80,82,80,79,77,75,79,77,82,91,92,91,89,87,89,91,89,86,89,87,84,86,87,80,79,75,77,79,80,79,82,80,79,77]
for note in track:
    result.append(number_to_note(note))
print(result)