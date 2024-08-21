from fastapi import HTTPException, status


def badrequest_exception(mgs: str):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str,
    )


def http_exception():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


def notfound_exception(entityName: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{entityName} not found"
    )


def forbidden_exception(mgs: str = "Forbidden"):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str)
