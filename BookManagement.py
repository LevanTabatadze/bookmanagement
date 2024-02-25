import json
import sys


# Creating book class which initialize every book in json library
class Book:
    def __init__(self, title, author, release_year):
        self.title = title
        self.author = author
        self.release_year = release_year

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Release Year: {self.release_year}"


class BookManager:
    # JSON file containing book information
    book_library = "Book_Library.json"

    def add_book(self):
        try:
            # Get new book information from user input
            book_title = str(input("Please Input Title Of Book: "))
            book_author = str(input("Please Input Author Of Book: "))
            book_release_year = int(input("Please Input Release Year Of Book: "))
            print()

            # Create a new Book object
            new_book = Book(book_title, book_author, book_release_year)

            # Add the new book to the library
            self.add_in_library(new_book)

        except TypeError:
            print("Oops Something Went Wrong, Please Input Correct Information")
        else:
            print("Book Added Successfully In Library")

    def search_book_title(self):
        # User inputs book title for search
        book_title = str(
            input("Please Input Book Title For Searching: ")).lower()
        print()

        json_data = self.read_json_file()

        # Use filter to find books with the specified title
        result = list(filter(lambda book: book.title.lower()
                      == book_title, json_data))

        if result:
            # Print information of the found books
            for book in result:
                print(book)
        else:
            print("This Book Is Not In The Library")

    # Display all books in the library

    def show_library(self):

        json_data = self.read_json_file()

        for book in json_data:
            print(book)

    # Add a book to the library in the JSON file
    def add_in_library(self, book: Book):
        try:

            library = self.read_json_file()
            if not isinstance(library, list):
                library = [library]
            library.append(book)
            self.write_json_file(library)

        except FileNotFoundError:
            book = [book]
            self.write_json_file(book)

        except json.JSONDecodeError:
            print("Oops, there is wrong info in json file")

    def read_json_file(self):
        try:
            with open(self.book_library, "r") as json_file:
                return json.load(json_file, object_hook=self.custom_book_deserialization)
        except FileNotFoundError:
            # If the file doesn't exist, return an empty list
            return []


    # Write data to the JSON file
    def write_json_file(self, info):
        
        with open(self.book_library, "w") as json_file:
            json.dump(info, json_file, indent=4,
                      default=self.custom_book_serialization)

    @staticmethod
    def custom_book_serialization(obj):
        # Serialize a Book object to JSON
        if isinstance(obj, Book):
            return {
                "Title": obj.title,
                "Author": obj.author,
                "Release Year": obj.release_year
            }
        return obj

    @staticmethod
    def custom_book_deserialization(json_data):
        # Deserialize JSON data to a Book object
        return Book(json_data["Title"], json_data["Author"], json_data["Release Year"])



while True:
    book_manager = BookManager()

    menu = """
        1. Add Book
        2. Show Library
        3. Search By Title
        4. Shut Down
    """

    print(menu)


    menu_choice = int(input("Please input number which is shown in menu: "))
    print()

    if menu_choice == 1:
        book_manager.add_book()
    elif menu_choice == 2:
        book_manager.show_library()
    elif menu_choice == 3:
        book_manager.search_book_title()
    elif menu_choice == 4:
        print("Good Bye See You Later")
        sys.exit()
    else:
        print("This number is not in menu, please input correct number")
