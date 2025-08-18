import os
import uvicorn
from dotenv import load_dotenv

# 加载环境变量

load_dotenv()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        reload=os.getenv("RELOAD") == "True",
    )
