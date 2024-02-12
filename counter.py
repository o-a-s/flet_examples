from flet import (
    app, 
    Page, 
    Row, 
    TextField, 
    IconButton, 
    icons, 
    border, 
    MainAxisAlignment, 
    TextAlign
    )

def subtract(count, page):
    count.value -= 1
    page.update()

def increment(count, page):
    count.value += 1
    page.update()

def main(page: Page):
    # page properties
    page.title = "Counter"
    page.window_width = 400
    page.window_height = 400
    page.vertical_alignment = MainAxisAlignment.CENTER
    
    # Increase counter button
    increment_button = IconButton( 
        icon=icons.REMOVE,
        on_click=lambda e: subtract(count, page),
        )
    # Counter textfield
    count = TextField(
        width=100,
        value=0, 
        border=border.all(width=1),
        text_align=TextAlign.CENTER
        )
    # Subtract counter button
    subtract_button = IconButton(
        icon=icons.ADD, 
        on_click=lambda e: increment(count, page)
        )
    # Add the buttons and textfield to the page, in a row control
    page.add(
        Row(
            controls=[
            subtract_button, 
            count, 
            increment_button
        ], alignment=MainAxisAlignment.CENTER
            )
        )

app(target=main)
