import sys
import warnings

def read_midi_with_pretty_midi(file_path):
    """
    A reader that loads a MIDI file using pretty_midi and 
    prints basic information about its tracks and notes.
    """
    
    import pretty_midi

    try:
        # Load MIDI file
        print(f"Loading MIDI file (using pretty_midi): {file_path}")
        midi_data = pretty_midi.PrettyMIDI(file_path)
        
        # 1. Print overall file details
        duration = midi_data.get_end_time()
        print(f"Duration: {duration:.2f} seconds")
        print(f"Number of instrument tracks: {len(midi_data.instruments)}")
        print("-" * 40)
        
        # 2. Iterate through instrument tracks
        for i, instrument in enumerate(midi_data.instruments):
            instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
            print(f"Track {i+1}: {instrument_name}")
            print(f"  Program: {instrument.program} | Is Drum: {instrument.is_drum}")
            print(f"  Total Notes: {len(instrument.notes)}")
            
            # Print the first 5 notes as a sample
            print("  First 5 notes sample:")
            for note in instrument.notes[:5]:
                # note.pitch is the MIDI note number (e.g. 60 is Middle C)
                note_name = pretty_midi.note_number_to_name(note.pitch)
                print(f"    - Pitch: {note.pitch} ({note_name}), Start: {note.start:.2f}s, End: {note.end:.2f}s, Velocity: {note.velocity}")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error reading MIDI file: {e}")

def read_midi_with_music21(file_path):
    """
    A reader that loads a MIDI file using music21 and 
    prints basic information about its parts and notes.
    """
    # Suppress library warnings from cluttering stdout/stderr
    warnings.filterwarnings("ignore")
    
    import music21

    try:
        # Load MIDI file
        print(f"Loading MIDI file (using music21): {file_path}")
        score = music21.converter.parse(file_path)
        
        # Get flattened seconds mapping for calculating absolute timestamps
        score_flat = score.flatten()
        sec_map = {item['element']: item for item in score_flat.secondsMap}
        
        # 1. Print overall file details
        # Find maximum end time of any note or chord in the score
        duration = max((item['endTimeSeconds'] for item in score_flat.secondsMap 
                        if 'Note' in item['element'].classes or 'Chord' in item['element'].classes), 
                       default=0.0)
        
        print(f"Duration: {duration:.2f} seconds (Quarter Length: {score.highestTime})")
        print(f"Number of instrument tracks (parts): {len(score.parts)}")
        print("-" * 40)
        
        # 2. Iterate through parts
        for i, part in enumerate(score.parts):
            # Try to determine instrument name
            insts = list(part.recurse().getElementsByClass(music21.instrument.Instrument))
            if insts and insts[0].instrumentName:
                instrument_name = insts[0].instrumentName
            elif part.partName:
                instrument_name = part.partName
            else:
                instrument_name = "Unknown Instrument"
                
            # Get all notes and chords
            notes_and_chords = list(part.recurse().notes)
            
            # Map part element seconds
            part_flat = part.flatten()
            part_sec_map = {item['element']: item for item in part_flat.secondsMap}
            
            # Count total individual notes (chords can have multiple pitches)
            total_notes = sum(len(n.pitches) if n.isChord else 1 for n in notes_and_chords)
            
            print(f"Track {i+1}: {instrument_name}")
            print(f"  Total Notes/Chords: {len(notes_and_chords)} (Total individual notes: {total_notes})")
            
            # Print the first 5 notes as a sample
            print("  First 5 notes/chords sample:")
            for item in notes_and_chords[:5]:
                # Get start and end times in seconds from the secondsMap
                item_sec = part_sec_map.get(item, sec_map.get(item, {}))
                start_sec = item_sec.get('offsetSeconds', 0.0)
                end_sec = item_sec.get('endTimeSeconds', 0.0)
                
                velocity = item.volume.velocity if (item.volume and item.volume.velocity is not None) else "N/A"
                
                if item.isChord:
                    pitches_str = ", ".join(f"{p.midi} ({p.nameWithOctave})" for p in item.pitches)
                    print(f"    - Chord: [{pitches_str}], Start: {start_sec:.2f}s, End: {end_sec:.2f}s, Velocity: {velocity}")
                else:
                    pitch = item.pitch
                    print(f"    - Pitch: {pitch.midi} ({pitch.nameWithOctave}), Start: {start_sec:.2f}s, End: {end_sec:.2f}s, Velocity: {velocity}")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error reading MIDI file: {e}")

if __name__ == "__main__":
    library_choice = "0"
    midi_path = "example.mid"

    if len(sys.argv) > 1:
        # Check if the first argument is specifically choosing the library
        if sys.argv[1] in ("0", "1"):
            library_choice = sys.argv[1]
            if len(sys.argv) > 2:
                midi_path = sys.argv[2]
        else:
            # First argument is not 0 or 1, treat it as the file path, choice defaults to 0
            library_choice = "0"
            midi_path = sys.argv[1]
    else:
        print("Usage: python read_midi.py [0|1] [path_to_midi_file]")
        print("  0: Use music21 (default)")
        print("  1: Use pretty_midi")
        print(f"Defaulting to: Library Choice = {library_choice} (music21), File = {midi_path}\n")

    if library_choice == "0":
        read_midi_with_music21(midi_path)
    else:
        read_midi_with_pretty_midi(midi_path)

