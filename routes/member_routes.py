from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging
from database.member_db import SqlMember
from database.member_db import SqlMember
from mysql.connector import IntegrityError

router = APIRouter()


class Member(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(max_length=255)


class UpdatedMember(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    email: str | None = Field(max_length=255, default=None)


@router.post("", status_code=201)
def router_create_member(body: Member):
    logging.info("HTTP request to add a member to the directory")
    body = body.model_dump()
    try:
        new_id = SqlMember.create_member(body)
        logging.info("Friend added successfully")
        return {"message": f"Member ID: {new_id} Added successfully"}
    except IntegrityError as e:
        logging.exception(e)
        if e.errno == 1062:
            raise HTTPException(status_code=409, detail="Email already exists.")
        raise HTTPException(status_code=400, detail="Bad request")

@router.get("")
def router_get_all_members():
    logging.info("HTTP request to show all members")
    members = SqlMember.get_all_members()
    logging.info("The system successfully returned the member list.")
    return members


@router.get("/{id}")
def router_get_member_by_id(id: int):
    logging.info("HTTP request to display client by ID")
    member = SqlMember.get_member_by_id(id)
    if member:
        logging.info("The system successfully restored the member.")
        return member
    else:
        logging.error("No member with such ID found.")
        raise HTTPException(status_code=404, detail="No member with such ID found.")


@router.patch("/{id}")
def router_update_member(id: int, body: UpdatedMember):
    logging.info("HTTP request to update directory member properties")
    body = body.model_dump(exclude_none=True)
    try:
        changed = SqlMember.update_member(id, body)
        if changed:
            logging.info("The system was updated successfully.")
            return {"message": f"Member ID: {id} updated successfully"}
        else:
            logging.error(f"No member found with ID:{id}")
            raise HTTPException(status_code=404, detail=f"No member found with ID:{id}")
    except IntegrityError as e:
        logging.exception(e)
        if e.errno == 1062:
            raise HTTPException(status_code=409, detail="Email already exists.")
        raise HTTPException(status_code=400, detail="Bad request")

@router.patch("/{id}/deactivate")
def router_deactivate_member(id: int):
    logging.info("HTTP request to deactivate a directory member")
    changed = SqlMember.deactivate_member(id)
    if changed:
        logging.info(f"The friend id:{id}was successfully neutralized.")
        return {"message": f"The friend id:{id}was successfully neutralized."}
    else:
        logging.error(f"No member found with ID:{id}")
        raise HTTPException(status_code=404, detail=f"No member found with ID:{id}")


@router.patch("/{id}/activate")
def router_activate_member(id: int):
    logging.info("HTTP request to eactivate a directory member")
    changed = SqlMember.activate_member(id)
    if changed:
        logging.info(f"The friend id:{id}was successfully activated.")
        return {"message": f"The friend id:{id}was successfully activated."}
    else:
        logging.error(f"No member found with ID:{id}")
        raise HTTPException(status_code=404, detail=f"No member found with ID:{id}")
