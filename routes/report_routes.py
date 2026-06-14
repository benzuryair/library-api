from fastapi import APIRouter, HTTPException
import logging
from database.book_db import SqlBooks
from database.member_db import SqlMember

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/summary")
def router_get_summary():
    logging.info("HTTP request to get a summary of all information")
    total_books = SqlBooks.count_total_books()
    available_books = SqlBooks.count_available_books()
    borrowed_books = SqlBooks.count_borrowed_books()
    active_members = SqlMember.count_active_members()
    logging.info("The system returned a summary of all the information.")
    return {**total_books, **available_books, **borrowed_books, **active_members}


@router.get("/books-by-genre")
def router_books_by_genre():
    logging.info("HTTP request to get a summary of several books per genre")
    genres = ["Fiction", "Non-Fiction", "Science", "History", "Other"]
    summary_list = []
    for genre in genres:
        summary_list.append(SqlBooks.count_by_genre(genre))
    logging.info(
        "The system successfully returned a summary of several books for each genre."
    )
    return summary_list


@router.get("/top-member")
def router_top_member():
    logging.info("HTTP request to get the member with the most borrowed books")
    top_member = SqlMember.get_top_member()

    if not top_member:
        raise HTTPException(status_code=404, detail="No members found in the system.")
        
    logging.info(
        "The system successfully returned the member with the most borrowed books"
    )
    logging.info(
        "The system successfully returned the member with the most borrowed books"
    )
    return {"member id": top_member["id"], "borrowed": top_member["total_borrows"]}
