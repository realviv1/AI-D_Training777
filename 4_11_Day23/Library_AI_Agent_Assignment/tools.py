import json

BOOKS_FILE = "books.json"
RESERVATIONS_FILE = "reservations.json"


def search_books(keyword):
    with open(BOOKS_FILE, "r") as f:
        books = json.load(f)

    results = []

    keyword = keyword.lower()

    for book in books:
        if keyword in book["title"].lower() or \
           keyword in book["category"].lower() or \
           keyword in book["author"].lower():

            results.append(book)

    return results


def reserve_book(book_id, customer_name):

    with open(BOOKS_FILE, "r") as f:
        books = json.load(f)

    with open(RESERVATIONS_FILE, "r") as f:
        reservations = json.load(f)

    for book in books:

        if book["id"] == book_id:

            if book["available_copies"] <= 0:

                return {
                    "success": False,
                    "message": "No copies available."
                }

            confirmation = input(
                f"Reserve '{book['title']}' for {customer_name}? (yes/no): "
            )

            if confirmation.lower() != "yes":
                return {
                    "success": False,
                    "message": "Reservation cancelled."
                }

            book["available_copies"] -= 1

            reservation = {
                "book_id": book_id,
                "customer_name": customer_name,
                "title": book["title"]
            }

            reservations.append(reservation)

            with open(BOOKS_FILE, "w") as f:
                json.dump(books, f, indent=4)

            with open(RESERVATIONS_FILE, "w") as f:
                json.dump(reservations, f, indent=4)

            return {
                "success": True,
                "reservation": reservation
            }

    return {
        "success": False,
        "message": "Book not found."
    }