from smtplib import SMTP
import os
personal_email = os.getenv("EMAIL")


subject = f"Suruga-ya Product in Stock! [Product info maybe]"
message = f"An item on your wishlist in in stock: [product name hyperlinked] @ [product price]. "