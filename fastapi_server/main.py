import uvicorn

if __name__ == "__main__":
    from db_api import delete_all

    delete_all()

    uvicorn.run("fast_router:app", host="127.0.0.1", port=8000, reload=True)
