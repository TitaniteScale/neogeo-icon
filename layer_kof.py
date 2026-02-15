#!/usr/bin/env python3
"""
Script to create KOF marquees by layering the KOF logo on top of background images.
For each background in kof/backgrounds/, this script will:
  1. Open the background image
  2. Layer the kof.png logo on top of it at position (0, 0)
  3. Save the result to marquees/kof{name}.png

Example: kof/backgrounds/98.png -> marquees/kof98.png
"""

import os
import sys

from PIL import Image


def get_background_images(backgrounds_dir):
    """
    Get list of background images from the backgrounds directory.

    Args:
        backgrounds_dir: Path to the backgrounds directory

    Returns:
        List of tuples (filename, full_path)
    """
    backgrounds = []

    if not os.path.exists(backgrounds_dir):
        print(f"Error: Backgrounds directory not found at {backgrounds_dir}")
        return backgrounds

    for filename in os.listdir(backgrounds_dir):
        if filename.endswith(".png"):
            backgrounds.append((filename, os.path.join(backgrounds_dir, filename)))

    return backgrounds


def create_kof_marquee(background_path, logo_path, output_path):
    """
    Layer the KOF logo on top of a background image.

    Args:
        background_path: Path to the background image
        logo_path: Path to the KOF logo image
        output_path: Path where the output marquee will be saved
    """
    # Open the background image
    background = Image.open(background_path).convert("RGBA")
    print(f"  Background dimensions: {background.size}")

    # Open the KOF logo
    logo = Image.open(logo_path).convert("RGBA")
    print(f"  Logo dimensions: {logo.size}")

    # Create a copy of the background to work with
    result = background.copy()

    # Layer the logo at position (0, 0)
    # Using the logo's alpha channel as the mask for transparency
    result.paste(logo, (0, 0), logo)

    # Save the result
    result.save(output_path)
    print(f"  Saved to: {output_path}")


def main():
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kof_dir = os.path.join(base_dir, "kof")
    logo_path = os.path.join(kof_dir, "kof.png")
    backgrounds_dir = os.path.join(kof_dir, "backgrounds")
    marquees_dir = os.path.join(base_dir, "marquees")

    # Check if logo exists
    if not os.path.exists(logo_path):
        print(f"Error: KOF logo not found at {logo_path}")
        sys.exit(1)

    # Check if marquees directory exists, create if it doesn't
    if not os.path.exists(marquees_dir):
        print(f"Creating marquees directory at {marquees_dir}")
        os.makedirs(marquees_dir)

    # Get all background images
    backgrounds = get_background_images(backgrounds_dir)

    if not backgrounds:
        print("Error: No background images found in kof/backgrounds/")
        sys.exit(1)

    print(f"Found {len(backgrounds)} background image(s):")
    for filename, _ in backgrounds:
        print(f"  - {filename}")
    print()

    # Process each background
    print("Creating KOF marquees...")
    for filename, background_path in backgrounds:
        # Extract the base name (e.g., "98" from "98.png")
        base_name = os.path.splitext(filename)[0]

        # Create output filename (e.g., "kof98.png")
        output_filename = f"kof{base_name}.png"
        output_path = os.path.join(marquees_dir, output_filename)

        print(f"\nProcessing {filename} -> {output_filename}")
        create_kof_marquee(background_path, logo_path, output_path)

    print(f"\nSuccess! Created {len(backgrounds)} KOF marquee(s).")


if __name__ == "__main__":
    main()
