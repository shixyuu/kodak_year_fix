import os
import piexif
from datetime import datetime

def update_exif_year_only():
    # 1. Get the current year (e.g., "2026")
    current_year = str(datetime.now().year)
    count = 0

    # 2. Iterate through all JPG files in the current directory
    for filename in os.listdir('.'):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            try:
                # Load existing EXIF data
                exif_dict = piexif.load(filename)
                
                # Try to get the original date and time (DateTimeOriginal)
                # EXIF data is read as bytes, e.g., b"2015:08:15 14:30:00"
                original_time_bytes = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
                
                if original_time_bytes:
                    # Decode bytes to a standard string for processing
                    original_time_str = original_time_bytes.decode('utf-8')
                    
                    # 3. Core Step: Replace only the year
                    # The format of original_time_str is "YYYY:MM:DD HH:MM:SS"
                    # original_time_str[4:] preserves everything after the 4th character (":MM:DD HH:MM:SS")
                    new_time_str = current_year + original_time_str[4:]
                    
                    # Convert back to bytes for writing
                    new_time_bytes = new_time_str.encode('utf-8')

                    # 4. Update time tags
                    # Update 'Date Time Original'
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_time_bytes
                    
                    # Check and update other relevant EXIF time tags if they exist
                    if piexif.ExifIFD.DateTimeDigitized in exif_dict["Exif"]:
                        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_time_bytes
                        
                    if piexif.ImageIFD.DateTime in exif_dict["0th"]:
                        exif_dict["0th"][piexif.ImageIFD.DateTime] = new_time_bytes
                        
                    # Dump the modified dictionary back into EXIF bytes and write to file
                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, filename)
                    
                    print(f"✅ Year Updated: '{filename}' | {original_time_str} -> {new_time_str}")
                    count += 1
                else:
                    # Skip if the photo lacks original EXIF time metadata
                    print(f"⚠️ Skipped: '{filename}' has no EXIF time data to preserve month/day/time.")
                    
            except Exception as e:
                print(f"❌ Error processing '{filename}': {e}")

    if count == 0:
        print("\nNo eligible JPG files were found to modify.")
    else:
        print(f"\nProcessing complete! Successfully updated the EXIF year for {count} file(s).")

if __name__ == "__main__":
    update_exif_year_only()
