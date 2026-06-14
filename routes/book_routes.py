from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging
from database.book_db import SqlBooks
from database.member_db import SqlMember
from typing import Literal

router = APIRouter()


class book(BaseModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"]


class updatedbook(BaseModel):
    title: str | None = Field(max_length=50, default=None)
    author: str | None = Field(max_length=50, default=None)
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"] | None = (
        None
    )


@router.post("", status_code=201)
def router_create_book(body: book):
    logging.info("The system received an HTTP request to add a book.")
    body = body.model_dump()
    new_id = SqlBooks.create_book(body)
    logging.info(f"Book with ID: {new_id} successfully added to the system")
    return {"massage": f"Book with ID: {new_id} successfully added to the system"}


@router.get("")
def router_get_all_books():
    logging.info("HTTP request to display all books")
    list_of_books = SqlBooks.get_all_books()
    logging.info("The system has returned the records of all books.")
    return list_of_books


@router.get("/{id}")
def router_get_book_by_id(id: int):
    logging.info("HTTP request to find a book by ID")
    one_book = SqlBooks.get_book_by_id(id)
    if one_book:
        logging.info("The system returned a book by ID.")
        return one_book
    else:
        logging.error("No book with such ID was found.")
        raise HTTPException(status_code=404, detail="Book not found")


@router.patch("/{id}")
def router_update_book(id: int, body: updatedbook):
    logging.info("HTTP request to update details of one book")
    body = body.model_dump(exclude_none=True)
    changed = SqlBooks.update_book(id, body)
    if changed:
        logging.info(f"Book ID:{id} updated successfully")
        return {"massage": f"Book ID:{id} updated successfully"}
    else:
        logging.error("No book with such ID was found.")
        return {"massage": "No book with such ID was found."}


@router.patch("/{id}/borrow/{member_id}")
def router_borrow_book(id: int, member_id: int):
    logging.info("HTTP request to lend a book to a customer")

    member_dict = SqlMember.get_member_by_id(member_id)
    book_dict = SqlBooks.get_book_by_id(id)

    if member_dict is None:
        logging.error("There is no member in the library with this ID.")
        raise HTTPException(
            status_code=404, detail="There is no member in the library with this ID."
        )

    if not member_dict["is_active"]:
        logging.error("The member is inactive.")
        raise HTTPException(status_code=400, detail="The member is inactive.")

    if member_dict["total_borrows"] >= 3:
        logging.error(
            "You cannot lend to a customer because he has already borrowed 3 books."
        )
        raise HTTPException(
            status_code=400,
            detail="You cannot lend to a customer because he has already borrowed 3 books.",
        )

    if book_dict is None:
        logging.error("The book does not exist.")
        raise HTTPException(status_code=404, detail="The book does not exist.")

    if not book_dict["is_available"]:
        logging.error("The book has already been borrowed.")
        raise HTTPException(
            status_code=400,
            detail="The book has already been borrowed.",
        )

    SqlBooks.set_available(id, False, member_id)
    SqlMember.increment_borrows(member_id)
    logging.info("The system successfully lent the book to the friend.")
    return {
        "massage": f"Book ID:{id} was successfully loaned to library member ID:{member_id}"
    }


@router.patch("/{id}/return/{member_id}")
def router_return_book(id: int, member_id: int):
    logging.info("HTTP request to Return a book to the library")

    member_dict = SqlMember.get_member_by_id(member_id)
    book_dict = SqlBooks.get_book_by_id(id)
    if book_dict is None:
        logging.error("The book does not exist.")
        raise HTTPException(status_code=404, detail="The book does not exist.")

    if member_dict is None:
        logging.error("There is no member in the library with this ID.")
        raise HTTPException(
            status_code=404, detail="There is no member in the library with this ID."
        )

    if book_dict["is_available"]:
        logging.error("The book cannot be returned because it is not borrowed..")
        raise HTTPException(
            status_code=400,
            detail="The book cannot be returned because it is not borrowed.",
        )
    if book["borrowed_by_member_id"] != member_id:
        logging.error(
            "Cannot be returned because the book was not lent to the friend who is trying to return it."
        )
        raise HTTPException(
            status_code=400,
            detail="Cannot be returned because the book was not lent to the friend who is trying to return it.",
        )
    SqlBooks.set_available(id, True, None)
    logging.info("The system successfully returned the book to the library.")
    return {"massage": f"The system successfully returned the book id:{id} to the library."}
