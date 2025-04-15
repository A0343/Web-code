#!/usr/bin/env python3
import os
import subprocess
import sys

def create_directory_structure():
    """Create the required directory structure for the project."""
    directories = [
        "app",
        "app/routers",
        "app/static",
        "app/static/css",
        "app/static/images", 
        "app/templates",
        "data",
        "tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies from requirements.txt."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Python dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Python dependencies.")
        sys.exit(1)

def install_node_dependencies():
    """Install Node.js dependencies for Tailwind CSS."""
    try:
        subprocess.run(["npm", "install", "-D", "tailwindcss@latest", "daisyui"], check=True)
        subprocess.run(["npx", "tailwindcss", "init"], check=True)
        print("Node.js dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Node.js dependencies. Make sure Node.js and npm are installed.")
        sys.exit(1)
    except FileNotFoundError:
        print("Node.js or npm not found. Please install Node.js before running this script.")
        sys.exit(1)

def create_placeholder_image():
    """Create a simple placeholder image if needed."""
    # This is just a placeholder function
    # In a real setup, you would either:
    # 1. Download placeholder images
    # 2. Generate them using a library like PIL
    # 3. Prompt the user to manually add images
    print("\nDon't forget to add product images to app/static/images/")
    print("You can use placeholder images if you don't have real product images.")

def main():
    """Main function to set up the project."""
    print("Setting up FastAPI Cloth Store project...")
    
    # Create directory structure
    create_directory_structure()
    
    # Install dependencies
    print("\nInstalling Python dependencies...")
    install_dependencies()
    
    print("\nInstalling Node.js dependencies for Tailwind CSS...")
    install_node_dependencies()
    
    # Create placeholder image
    create_placeholder_image()
    
    print("\nSetup complete!")
    print("\nTo run the application:")
    print("1. Build CSS: npx tailwindcss -i ./app/static/css/styles.css -o ./app/static/css/output.css --watch")
    print("2. Start server: uvicorn app.main:app --reload")
    print("3. Open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main()