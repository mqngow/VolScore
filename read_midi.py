import sys
import pretty_midi

def read_midi_file(file_path):
    """
    A reader that loads a MIDI file using pretty_midi and 
    prints basic information about its tracks and notes.
    """
    try:
        # Load MIDI file
        print(f"Loading MIDI file: {file_path}")
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

if __name__ == "__main__":
    # If a filename is passed as a command-line argument, use it; otherwise default to a placeholder
    if len(sys.argv) > 1:
        midi_path = sys.argv[1]
    else:
        midi_path = "example.mid"
        print(f"No file provided. Usage: python read_midi.py <path_to_midi_file>")
        print(f"Defaulting to '{midi_path}'\n")
        
    read_midi_file(midi_path)
