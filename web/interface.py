import os
import tempfile
import zipfile
from io import BytesIO
import gradio as gr
from agent.graph import agent
from pathlib import Path

from agent.tools import get_all_files, clear_storage


def  create_project_zip() -> str:
    """Create a ZIP file and return the file path"""
    files = get_all_files()
    if not files:
        return None

    # Create a temporary file
    temp_fd, temp_path = tempfile.mkstemp(suffix='.zip', prefix='project_')
    os.close(temp_fd)  # Close the file descriptor

    # Write ZIP to the temporary file
    with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filepath, content in files.items():
            zip_file.writestr(filepath, content)

    return temp_path


def format_output(result):
    """Format the agent output in a nice, readable way"""
    if isinstance(result, str):
        return result

    output_lines = ["=" * 70, "✅ AGENT EXECUTION COMPLETED", "=" * 70, ""]

    # Add plan details
    if 'plan' in result:
        plan = result['plan']
        output_lines.extend([
            "📋 PROJECT PLAN",
            "─" * 70,
            f"📦 Name: {plan.name}",
            f"📝 Description: {plan.description}",
            f"🔧 Tech Stack: {plan.techstack}",
            "",
            "✨ Features:",
        ])
        for i, feature in enumerate(plan.features, 1):
            output_lines.append(f"   {i}. {feature}")
        output_lines.append("")

    # Add task details
    if 'task_plan' in result:
        task_plan = result['task_plan']
        output_lines.extend([
            f"🏗️  IMPLEMENTATION PLAN ({len(task_plan.implementation_steps)} tasks)",
            "─" * 70,
        ])
        for idx, task in enumerate(task_plan.implementation_steps, 1):
            output_lines.append(f"{idx}. 📄 {task.filepath}")
            output_lines.append(f"   ↳ {task.task_description[:80]}...")
            output_lines.append("")

    # Add completion status
    if 'coder_state' in result:
        coder_state = result['coder_state']
        total_tasks = len(coder_state.task_plan.implementation_steps)
        completed_tasks = coder_state.current_step_idx
        output_lines.extend([
            "💻 CODING PROGRESS",
            "─" * 70,
            f"✓ Completed: {completed_tasks}/{total_tasks} tasks",
            ""
        ])

    # List generated files from memory
    files = get_all_files()
    if files:
        output_lines.extend([
            f"📁 GENERATED FILES ({len(files)})",
            "─" * 70,
        ])
        for filepath, content in sorted(files.items()):
            size = len(content.encode('utf-8'))
            output_lines.append(f"   ✓ {filepath} ({size:,} bytes)")

        output_lines.append("")

    output_lines.extend([
        "=" * 70,
        "🎉 Project generation complete!",
        "📂 Check the 'generated_project' folder for your files.",
        "=" * 70
    ])

    return "\n".join(output_lines)


def process_prompt(user_prompt, recursion_limit):
    """Process the user's project prompt"""
    if not user_prompt.strip():
        return "⚠️ Please enter a project description", None

    try:
        clear_storage()

        # Show processing message
        yield "⏳ Starting SentraAI...\n🔄 This may take a minute...\n", None

        # Call your agent
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": recursion_limit}
        )

        zip_path = create_project_zip()

        # Return formatted result and zip path
        yield format_output(result), zip_path

    except Exception as e:
        error_msg = [
            "=" * 70,
            "❌ ERROR OCCURRED",
            "=" * 70,
            "",
            f"Error: {str(e)}",
            "",
            "💡 Troubleshooting Tips:",
            "  • Ensure your .env file has a valid GROQ_API_KEY",
            "  • Try increasing the recursion limit",
            "  • Make sure your prompt is clear and specific",
            "  • Check that all dependencies are installed",
            "",
            "=" * 70
        ]
        yield "\n".join(error_msg), None


# Custom CSS for better styling
custom_css = """
#header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
}

#header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: bold;
}

#header p {
    margin-top: 0.5rem;
    font-size: 1.1rem;
    opacity: 0.9;
}

#main-container {
    max-width: 1400px;
    margin: 0 auto;
}

.input-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}

.output-section {
    background: #1e1e1e;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #333;
}

#prompt-input textarea {
    font-size: 1rem !important;
    line-height: 1.5 !important;
}

#output-box textarea {
    font-family: 'Courier New', monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    background: #1e1e1e !important;
    color: #00ff00 !important;
}

.feature-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    margin-bottom: 1rem;
}

.tips-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
}

#build-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 2rem !important;
    font-weight: bold !important;
}

.example-card {
    background: #e3f2fd;
    padding: 0.8rem;
    border-radius: 5px;
    border-left: 3px solid #2196f3;
    margin-bottom: 0.5rem;
    cursor: pointer;
}

.example-card:hover {
    background: #bbdefb;
}

footer {
    text-align: center;
    margin-top: 2rem;
    padding: 1rem;
    color: #666;
    font-size: 0.9rem;
}
"""

# Create the UI
with gr.Blocks(title="AI Coding Agent", css=custom_css, theme=gr.themes.Soft()) as demo:
    # Header
    with gr.Group(elem_id="header"):
        gr.Markdown("# 🤖 SentraAI")
        gr.Markdown("Transform your ideas into code with AI-powered multi-agent system")

    with gr.Column(elem_id="main-container"):
        with gr.Row():
            # Left Column - Input
            with gr.Column(scale=1, elem_classes="input-section"):
                gr.Markdown("### 📝 Project Description")

                prompt_input = gr.Textbox(
                    label="",
                    placeholder="Example:\n• Build a modern todo app with HTML, CSS, and JavaScript\n• Create a Flask REST API with user authentication\n• Build a Python data analysis dashboard with Plotly\n\nBe specific about:\n✓ Technology stack\n✓ Key features\n✓ Design requirements",
                    lines=10,
                    elem_id="prompt-input"
                )

                with gr.Row():
                    recursion_limit = gr.Slider(
                        minimum=50,
                        maximum=200,
                        value=100,
                        step=10,
                        label="🔄 Recursion Limit",
                        info="Maximum steps the agent can take"
                    )

                submit_btn = gr.Button(
                    "🚀 Generate Project",
                    variant="primary",
                    size="lg",
                    elem_id="build-btn"
                )

                # Tips Section
                with gr.Accordion("💡 Pro Tips", open=False):
                    gr.Markdown("""
                    **For Best Results:**

                    ✅ **Be Specific**: Mention exact technologies (e.g., "React with TypeScript" not just "frontend")

                    ✅ **List Features**: Break down what you want (e.g., "user login, CRUD operations, dark mode")

                    ✅ **Mention Structure**: Describe file organization if needed (e.g., "separate API and frontend folders")

                    ✅ **Set Constraints**: Mention any requirements (e.g., "mobile-responsive", "uses SQLite")

                    ⚠️ **Avoid Vague Requests**: Instead of "build a website", try "build a landing page with hero section, features grid, and contact form"
                    """)

            # Right Column - Output
            with gr.Column(scale=1, elem_classes="output-section"):
                gr.Markdown("### 🖥️ Agent Output")

                output = gr.Textbox(
                    label="",
                    lines=28,
                    max_lines=35,
                    elem_id="output-box",
                    # show_copy_button=True,
                    interactive=False
                )

                # Download button for ZIP file
                download_btn = gr.File(
                    label="📦 Download Project ZIP",
                    interactive=False
                )

    # Footer
    gr.Markdown("""
    <footer>
        <p>🤖 Powered by LangGraph & Groq LLMs | 📁 Generated files saved to <code>generated_project/</code></p>
        <p>💡 Tip: Check your project folder after generation completes</p>
    </footer>
    """)

    # Event handler
    submit_btn.click(
        fn=process_prompt,
        inputs=[prompt_input, recursion_limit],
        outputs=[output, download_btn]
    )

if __name__ == "__main__":
    demo.launch(server_port=7860)