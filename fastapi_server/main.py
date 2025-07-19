import uvicorn

if __name__ == "__main__":
    from db_api import delete_all

    delete_all()

    uvicorn.run("fast_router:app", host="192.168.31.135", port=1919, reload=True)
