NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
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
track = [67,67,67,63,70,67,74,74,74,75,70,66,63,70,67,70,69,70,66,63,70,74,75,72,82,81,78,86,85,81,84,82,78,75,79,78,77,76,77,79,81,80,79,78,79,81,82,86,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,86,86,86,85,85,85,81,81,81,84,84,84,82,82,82,78,78,78,75,75,75,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,91,91,91,86,86,86,82,82,82,80,80,80,75,75,75,71,71,71,68,68,68,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,86,86,86,85,85,85,81,81,81,84,84,84,82,82,82,78,78,78,75,75,75,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,91,91,91,86,86,86,82,82,82,80,80,80,75,75,75,71,71,71,68,68,68,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,86,86,86,85,85,85,81,81,81,84,84,84,82,82,82,78,78,78,75,75,75,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,91,91,91,86,86,86,82,82,82,80,80,80,75,75,75,71,71,71,68,68,68,74,74,74,75,75,75,72,72,72,82,82,82,81,81,81,78,78,78,85,85,85,84,84,84,80,80,80,83,83,83,81,81,81,77,77,77,74,74,74,80,80,80,81,81,81,78,78,78,88,88,88,87,87,87,84,84,84,85,85,85,84,84,84,80,80,80,83,83,83,81,81,81,77,77,77,74,74,74,70,70,70,71,71,71,68,68,68,78,78,78,77,77,77,74,74,74,91,91,91,86,86,86,82,82,82,80,80,80,75,75,75,71,71,71,68,68,68,76,81,83,84,86,84,85,79,79,79,79,79,78,79,78,79,79,79,79,79,79,79,79,79,79,79,78,78,78,79,79,79,79,79,79,79,79,79,75,82,79,75,82,79,75,82,79,75,79,79]
for note in track:
    result.append(number_to_note(note))
print(result)