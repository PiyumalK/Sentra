# SimpleCalculator

## Project Overview

**SimpleCalculator** is a lightweight, browser‑based calculator that performs basic arithmetic operations. It provides a clean, responsive user interface built with HTML, CSS, and vanilla JavaScript. Users can interact with the calculator using on‑screen buttons or their keyboard, making quick calculations fast and intuitive.

Key features:
- Addition, subtraction, multiplication, and division.
- Real‑time display of the current expression and result.
- Keyboard support for numbers, operators, **Enter** (evaluate), **Esc** (clear), and **Backspace** (delete last entry).
- Basic error handling (division by zero, malformed expressions).
- Responsive layout that works on desktop and mobile browsers.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Markup | **HTML5** – defines the calculator layout and button elements. |
| Styling | **CSS3** – styles the calculator, provides a modern look and responsive behavior. |
| Logic | **JavaScript (ES6+)** – handles button clicks, keyboard events, expression parsing, and display updates. |

All code runs entirely in the client’s browser; there is no server‑side component.

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/simple-calculator.git
   cd simple-calculator
   ```
2. **Open the application**
   - Locate the `index.html` file in the project root.
   - Open it directly in a web browser (Chrome, Firefox, Edge, Safari, etc.) by double‑clicking the file or dragging it into a browser window.
   - No additional build steps, package managers, or servers are required.

## Usage

### Button Layout
| Button | Function |
|--------|----------|
| `0‑9`   | Append the corresponding digit to the current expression. |
| `+`, `-`, `*`, `/` | Append the arithmetic operator. |
| `=` or **Enter** | Evaluate the expression and display the result. |
| `C` or **Esc** | Clear the entire expression and reset the display. |
| `←` or **Backspace** | Delete the last character entered. |
| `.` | Insert a decimal point. |

### Keyboard Shortcuts
- **Numbers (0‑9)** – type directly to add digits.
- **Operators (`+ - * /`)** – type to add operators.
- **Enter** – evaluate the expression (same as clicking `=`).
- **Esc** – clear the calculator (same as clicking `C`).
- **Backspace** – delete the last character (same as clicking `←`).
- **.`** – decimal point.

### Error Handling
- **Division by zero** – the calculator displays `Error: Division by zero` and clears the expression after a short pause.
- **Invalid expression** – if the JavaScript `eval` call throws, the display shows `Error` and the input is reset.
- The UI prevents multiple consecutive operators and ensures the expression is syntactically valid before evaluation.

## Development

The project is intentionally simple, but it can be extended in several ways:
- **Scientific functions** – add trigonometric, logarithmic, and power functions.
- **History panel** – keep a list of past calculations.
- **Theming** – allow users to switch between light/dark or custom color schemes.
- **Modularization** – split the JavaScript into separate modules (e.g., `display.js`, `logic.js`) and use a bundler like Webpack for larger feature sets.
- **Testing** – integrate unit tests with a framework such as Jest to verify calculation logic.

When extending functionality, keep the following conventions:
- All DOM queries should be performed in `script.js` (or the main JS file) to keep HTML markup clean.
- Use `const`/`let` instead of `var` and follow the existing naming style (`handleClick`, `updateDisplay`).
- Update the README to reflect any new features or setup steps.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for full details.
