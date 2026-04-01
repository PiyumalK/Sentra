// script.js
// Calculator class encapsulating calculation logic
class Calculator {
  constructor() {
    this.currentInput = '';
    this.previousValue = null; // number
    this.operator = null; // '+', '-', '*', '/' or null
  }

  // Reset all state
  reset() {
    this.currentInput = '';
    this.previousValue = null;
    this.operator = null;
  }

  // Basic operations
  add(a, b) { return a + b; }
  subtract(a, b) { return a - b; }
  multiply(a, b) { return a * b; }
  divide(a, b) {
    if (b === 0) {
      throw new Error('Division by zero');
    }
    return a / b;
  }

  // Compute based on stored operator and previous value
  compute() {
    if (this.operator === null || this.previousValue === null || this.currentInput === '') {
      // Nothing to compute – return what we have
      return this.currentInput || (this.previousValue !== null ? this.previousValue.toString() : '');
    }
    const current = parseFloat(this.currentInput);
    let result;
    try {
      switch (this.operator) {
        case '+':
          result = this.add(this.previousValue, current);
          break;
        case '-':
          result = this.subtract(this.previousValue, current);
          break;
        case '*':
          result = this.multiply(this.previousValue, current);
          break;
        case '/':
          result = this.divide(this.previousValue, current);
          break;
        default:
          result = current;
      }
    } catch (e) {
      // Division by zero or other error
      this.reset();
      return 'Error';
    }
    // After successful computation, set result as the new current input
    this.currentInput = result.toString();
    this.previousValue = null;
    this.operator = null;
    return this.currentInput;
  }
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
  const display = document.getElementById('display');
  const buttons = document.querySelectorAll('.buttons button');
  const calculator = new Calculator();

  const updateDisplay = (value) => {
    display.textContent = value;
  };

  // Helper to handle operator button press
  const handleOperator = (op) => {
    if (calculator.currentInput === '' && calculator.previousValue !== null) {
      // Change operator without entering a new number
      calculator.operator = op;
      return;
    }
    if (calculator.currentInput !== '') {
      const num = parseFloat(calculator.currentInput);
      if (!isNaN(num)) {
        calculator.previousValue = num;
        calculator.currentInput = '';
        calculator.operator = op;
      }
    }
  };

  // Attach click listeners to buttons
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const action = button.dataset.action;
      const value = button.dataset.value; // for digits/operators if provided

      switch (action) {
        case 'digit':
          if (value === '.') {
            // Decimal handling – ensure only one decimal point
            if (!calculator.currentInput.includes('.')) {
              calculator.currentInput = calculator.currentInput || '0';
              calculator.currentInput += '.';
            }
          } else {
            // Append digit
            calculator.currentInput += value;
          }
          updateDisplay(calculator.currentInput);
          break;
        case 'operator':
          handleOperator(value);
          // Show the stored previous value (or 0) after operator press
          updateDisplay(calculator.previousValue !== null ? calculator.previousValue.toString() : '0');
          break;
        case 'equals':
          const result = calculator.compute();
          updateDisplay(result);
          break;
        case 'clear':
          calculator.reset();
          updateDisplay('');
          break;
        case 'backspace':
          calculator.currentInput = calculator.currentInput.slice(0, -1);
          updateDisplay(calculator.currentInput);
          break;
        default:
          // No action defined
          break;
      }
    });
  });

  // Keyboard handling – map keys to the same actions
  document.addEventListener('keydown', (e) => {
    const key = e.key;
    if (key >= '0' && key <= '9') {
      // Digit
      calculator.currentInput += key;
      updateDisplay(calculator.currentInput);
    } else if (key === '.') {
      if (!calculator.currentInput.includes('.')) {
        calculator.currentInput = calculator.currentInput || '0';
        calculator.currentInput += '.';
      }
      updateDisplay(calculator.currentInput);
    } else if (['+', '-', '*', '/'].includes(key)) {
      handleOperator(key);
      updateDisplay(calculator.previousValue !== null ? calculator.previousValue.toString() : '0');
    } else if (key === 'Enter' || key === '=') {
      const result = calculator.compute();
      updateDisplay(result);
    } else if (key === 'Backspace') {
      calculator.currentInput = calculator.currentInput.slice(0, -1);
      updateDisplay(calculator.currentInput);
    } else if (key === 'Delete') {
      calculator.reset();
      updateDisplay('');
    }
  });
});
