import json
import os

class PersonalLibraryManager:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        try:
            with open(self.filename, "r") as file:
                books = json.load(file)
                # Standardize keys to lowercase
                for book in books:
                    book["title"] = book.pop("Title", book.get("title", ""))
                    book["author"] = book.pop("Author", book.get("author", ""))
                    book["year"] = book.pop("Year", book.get("year", 0))
                    book["genre"] = book.pop("Genre", book.get("genre", ""))
                    book["status"] = book.pop("Status", book.get("status", "Wishlist"))
                    book["progress"] = book.pop("Progress", book.get("progress", 0))
                return books
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self):
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        year = input("Enter publication year: ").strip()
        genre = input("Enter genre: ").strip()
        status = input("Reading Status (Completed/Reading/Wishlist): ").strip().capitalize()

        # Handle progress input, removing '%' if present
        progress_input = input("Progress Percentage: ").strip().replace('%', '')
        progress = 100 if status == "Completed" else (0 if status == "Wishlist" else int(progress_input))
        
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "status": status,
            "progress": progress
        }

        self.library.append(book)
        self.save_library()
        print(f"'{title}' added to the library!")


    def remove_book(self):
        title = input("Enter the title of the book to remove: ").strip()
        for book in self.library:
            if book["title"].lower() == title.lower():
                self.library.remove(book)
                self.save_library()
                print(f"'{title}' removed from the library.")
                return
        print("Book not found!")

    def search_book(self):
        query = input("Enter book title or author to search: ").strip().lower()
        results = [book for book in self.library if query in book["title"].lower() or query in book["author"].lower()]
        if results:
            print("Search Results:")
            for book in results:
                self.display_book(book)
        else:
            print("No matching books found.")

    def display_all_books(self):
        if not self.library:
            print("No books in the library.")
            return
        print("Library Collection:")
        for book in self.library:
            self.display_book(book)

    def display_book(self, book):
        status_color = {
            "Completed": "Completed",
            "Reading": "Reading",
            "Wishlist": "Wishlist"
        }
        print(f"\033[95mTitle:\033[0m {book['title']} | "
              f"\033[95mAuthor:\033[0m {book['author']} | "
              f"\033[95mYear:\033[0m {book['year']} | "
              f"\033[95mGenre:\033[0m {book['genre']} | "
              f"\033[95mStatus:\033[0m {status_color.get(book['status'], book['status'])} | "
              f"\033[95mProgress:\033[0m {book['progress']}%")

    def display_statistics(self):
        total_books = len(self.library)
        if total_books == 0:
            print("No books in the library to show statistics.")
            return

        completed_books = sum(1 for book in self.library if book["status"] == "Completed")
        reading_books = sum(1 for book in self.library if book["status"] == "Reading")
        wishlist_books = sum(1 for book in self.library if book["status"] == "Wishlist")

        print(f"Total Books: {total_books}")
        print(f"Completed Books: {completed_books}")
        print(f"Currently Reading:{reading_books}")
        print(f"Wishlist:{wishlist_books}")

    def menu(self):
        while True:
            print("Personal Library Manager")

            print("1. Add a Book")
            print("2. Remove a Book")
            print("3. Search for a Book")
            print("4. Display All Books")
            print("5. Display Statistics")
            print("6. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.display_all_books()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                print("Exiting... Happy Reading!")
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    PersonalLibraryManager().menu()
