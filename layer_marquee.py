#!/usr/bin/env python3
"""
Script to layer marquee images on top of the Neo Geo base image.
Fills all four marquee slots with random, non-repeating marquees.
The marquee images (27x31) are placed at positions:
  Slot 1: (79, 141)
  Slot 2: (145, 141)
  Slot 3: (214, 141)
  Slot 4: (277, 141)
"""

import os
import random
import sys

from PIL import Image


def get_available_marquees(marquees_dir, exclude_blank=True):
    """
    Get list of available marquee images from the marquees directory.

    Args:
        marquees_dir: Path to the marquees directory
        exclude_blank: If True, excludes _blank.png from the list

    Returns:
        List of marquee file paths
    """
    marquees = []

    if not os.path.exists(marquees_dir):
        print(f"Error: Marquees directory not found at {marquees_dir}")
        return marquees

    for filename in os.listdir(marquees_dir):
        if filename.endswith(".png"):
            if exclude_blank and filename == "_blank.png":
                continue
            marquees.append(os.path.join(marquees_dir, filename))

    return marquees


def layer_marquees(base_image, marquee_paths, output_path):
    """
    Layer multiple marquee images on top of a base image at predefined positions.

    Args:
        base_image: PIL Image object (already has backlight effect applied)
        marquee_paths: List of up to 4 marquee image paths to overlay
        output_path: Path where the output image will be saved
    """
    # Define the four slot positions
    positions = [
        (79, 141),  # Slot 1
        (145, 141),  # Slot 2
        (214, 141),  # Slot 3
        (277, 141),  # Slot 4
    ]

    print(f"Base image dimensions: {base_image.size}")

    # Create a copy of the base image to work with
    result = base_image.copy()

    # Layer each marquee at its corresponding position
    for i, marquee_path in enumerate(marquee_paths[:4]):  # Limit to 4 slots
        if i >= len(positions):
            break

        # Open the marquee image
        marquee = Image.open(marquee_path).convert("RGBA")
        position = positions[i]

        marquee_name = os.path.basename(marquee_path)
        print(
            f"Slot {i + 1}: Placing '{marquee_name}' at position {position} (size: {marquee.size})"
        )

        # Paste the marquee onto the result image at the specified position
        # Using the marquee's alpha channel as the mask for transparency
        result.paste(marquee, position, marquee)

    # Save the result
    result.save(output_path)
    print(f"\nOutput saved to: {output_path}")


def main():
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_image = os.path.join(base_dir, "neogeo.png")
    marquees_dir = os.path.join(base_dir, "marquees")
    output_image = os.path.join(base_dir, "neogeo.png")

    # Check if base image exists
    if not os.path.exists(base_image):
        print(f"Error: Base image not found at {base_image}")
        sys.exit(1)

    # Get available marquees (excluding _blank.png)
    available_marquees = get_available_marquees(marquees_dir, exclude_blank=True)

    if not available_marquees:
        print("Error: No marquee images found (excluding _blank.png)")
        sys.exit(1)

    print(f"Found {len(available_marquees)} available marquee(s):")
    for marquee in available_marquees:
        print(f"  - {os.path.basename(marquee)}")
    print()

    # If we have fewer than 4 marquees, we need to use them multiple times
    # but we'll shuffle to randomize which ones appear in which slots
    if len(available_marquees) < 4:
        # Duplicate the list until we have at least 4 items
        extended_marquees = available_marquees.copy()
        while len(extended_marquees) < 4:
            extended_marquees.extend(available_marquees)

        # Shuffle and take 4
        random.shuffle(extended_marquees)
        selected_marquees = extended_marquees[:4]
    else:
        # We have 4 or more marquees, randomly select 4 without replacement
        selected_marquees = random.sample(available_marquees, 4)

    print("Selected marquees for each slot:")
    for i, marquee in enumerate(selected_marquees):
        print(f"  Slot {i + 1}: {os.path.basename(marquee)}")
    print()

    # Open the base image
    base = Image.open(base_image).convert("RGBA")

    # Layer the marquee cards on top
    layer_marquees(base, selected_marquees, output_image)
    print("Success! All four marquee slots filled with random marquees.")


if __name__ == "__main__":
    main()
