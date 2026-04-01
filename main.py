from web.interface import demo

if __name__ == "__main__":
    print("=" * 60)
    print("SentraAI")
    print("=" * 60)
    print("Initializing project directory...")
    print("\nLaunching web interface...")
    print("Server will start at: http://localhost:7860")
    print("Please wait for the server to start...\n")
    print("=" * 60)

    # Launch the Gradio interface
    demo.launch(
        server_port=7860,
        server_name="0.0.0.0",  # Allow external access
        share=False,  # Set to True for public link
        show_error=True
    )