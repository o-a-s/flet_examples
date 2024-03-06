import flet as ft
from flet import (
    app,
    Page, 
    Row, 
    Column,
    KeyboardEvent, 
    TextField, 
    ElevatedButton,
    TextStyle,
    ButtonStyle,
    RoundedRectangleBorder,
    MainAxisAlignment
)
from numexpr import evaluate
from re import sub

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

COLORS = {
    "background": "#333333",  # Charcoal gray background for readability
    "textfield_bg": "#444444",  # Slightly darker text field for visual clarity
    "text": "#FFFFFF",  # White text for optimal contrast
    "button_bg": "#009688",  # Teal primary color for a vibrant accent
    "button_bg_selected": "#00BCD4",  # Lighter teal for hover/pressed state
    "operator_bg": "#2196F3",  # Blue for operators, distinct but complementary
    "operator_text": "#FFFFFF",  # White text for operators
}
# Allowed key for input
ALLOWED_KEYS = [
            "1", "2", "3", "4", "5",
            "6", "7","8", "9", "0",
            "+", "-", "*", "/", "(", ")", ".",
        ]
# Numpad operations mapping
NUMPAD_OPERATIONS = {
            "Numpad Add" : "+",
            "Numpad Subtract" : "-",
            "Numpad Multiply" : "*",
            "Numpad Divide" : "/",
            "Numpad Decimal": ".",
        }
# Defines how the button layout will look like
BUTTON_LAYOUT = [
    [["<", "#9E9E9E", "e"], ["(", "#9E9E9E", "("], [")", "#9E9E9E", ")"], ["÷", "#2196F3", "/"]],
    [["7", "#9E9E9E", "7"], ["8", "#9E9E9E", "8"], ["9", "#9E9E9E", "9"], ["x", "#2196F3", "*"]],
    [["4", "#9E9E9E", "4"], ["5", "#9E9E9E", "5"], ["6", "#9E9E9E", "6"], ["-", "#2196F3", "-"]],
    [["1", "#9E9E9E", "1"], ["2", "#9E9E9E", "2"], ["3", "#9E9E9E", "3"], ["+", "#2196F3", "+"]],
    [["C", "#9E9E9E", "c"], ["0", "#9E9E9E", "0"], [".", "#9E9E9E", "."], ["=", "#2196F3", "="]],
]
# Create a list of all valid operators, including those from the numpad.
ALL_OPERATORS = ["+", "-", "*", "/", "(", ")"] + list(
    NUMPAD_OPERATIONS.values())

# ------------------------------------------------------------------------------
# UI Component Creation Functions
# ------------------------------------------------------------------------------

def create_textfield():
    """
    Creates a text field with predefined styles
    """
    return TextField(
        read_only=True,
        border_color=COLORS["text"],
        bgcolor=COLORS["textfield_bg"],
        text_style=TextStyle(size=30, color=COLORS["text"]),
        hint_text="0",
        expand=True,
    )

def create_button(text, background_color, data, on_click):
    
    """
    Creates a button with specified properties
    """
    return ElevatedButton(
        text=text,
        bgcolor=background_color,
        color=COLORS["background"],
        data=data,
        width=70,
        height=50,
        on_click=on_click,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=2),
        ),
    )

# ------------------------------------------------------------------------------
# Logic Functions
# ------------------------------------------------------------------------------

def preprocess_expression(expression: str) -> str:
    """
    Preprocesses the expression by 
    replacing parentheses next to numbers with '*' symbol
    """
    # Remove leading zeros from all numbers:
    expression = sub(r"\b0+(?=\d)", "", expression)  # \b added for word boundaries

    # Replace parentheses next to numbers:
    parentheses_pattern = r"(\d+)\("
    parentheses_replacement = r"\1*("
    expression = sub(parentheses_pattern, parentheses_replacement, expression)

    return expression

def calculate_result():
    """
    Calculates the result of the expression in the text field 
    and updates the text field
    """
    result = ""
    try:
        expression = preprocess_expression(txt_field.value)
        result = evaluate(expression)
        txt_field.value = str(result)
    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
        txt_field.value = f"Error: {e}"

def update_txt_field(data):
    """Updates the text field with input validation"""
    # Handle parentheses first:
    txt_field.value += data
    
    last_char = txt_field.value[-1:] if txt_field.value else ""
    
    # Only append data if it hasn't already been added:
    if data not in txt_field.value:  # Check if data is already present
        if (last_char not in ALL_OPERATORS or data not in ALL_OPERATORS
        ) and not txt_field.value.endswith("0"):
            txt_field.value += data

# # ------------------------------------------------------------------------------
# Main Page Setup
# ------------------------------------------------------------------------------

# Initialize and create the text field
txt_field = create_textfield()

def main(page: Page):
    """
    Sets up the calculator page and handles keyboard events
    """
    
    # Page properties
    page.title = "Calculator"
    page.window_height = 350
    page.window_width = 350
    page.window_min_height=350
    page.window_min_width=350
    page.bgcolor = COLORS["background"]

    # Handle the calculator buttons' operations
    def handle_keyboard_event(event: KeyboardEvent):
        """
        Handles keyboard input and prevents consecutive operators
        """
        # Get the input data from either the keyboard or a pressed button.
        data = event.control.data or event.key
        
        # Append the [keyboard / pressed buttons input] to text field and 
        if data in ALLOWED_KEYS:
            update_txt_field(data)
        
        # Handle numpad input:
        elif isinstance(data, str) and data.startswith("Numpad"):
            if data in NUMPAD_OPERATIONS:
                operation = NUMPAD_OPERATIONS[data]
                update_txt_field(operation)
            else:
                txt_field.value += data[-1]
                
        # Handle "=" or "Enter" to calculate the result 
        # (except when the text field is "0"):
        elif data == "=" or (isinstance(data, str) and data == "Enter"):
            if txt_field.value == "0":
                pass
            else:
                calculate_result()

        # Handle backspace:
        elif data == "e" or (isinstance(data, str) and data == "Backspace"):
            txt_field.value = txt_field.value[:-1]

        # Handle clear:
        elif data == "c":
            txt_field.value = "" 
        
        page.update()
    
    
    

    
    # Put the buttons in rows
    rows = [
        Row(
            controls=[
                create_button(text, background_color, data, on_click=handle_keyboard_event)
                for text, background_color, data in row_buttons
        ],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )
    for row_buttons in BUTTON_LAYOUT
]
    # Put on the page the text field and the rows of buttons in a container
    
    calculator_container = Column(
        controls=[txt_field] + rows,
        alignment=MainAxisAlignment.END,
        expand=True,
    )
    
    # Set the keyboard event handler for the page.
    page.on_keyboard_event = handle_keyboard_event
    # Add the container to the page
    page.add(calculator_container)

# Run the app
app(target=main, assets_dir="assets")

