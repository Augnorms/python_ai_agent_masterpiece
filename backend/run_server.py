import uvicorn

if __name__ == "__main__":
    """ server starting script  """
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)