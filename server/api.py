from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .db import init_db
from server.routes.users import router as UserRouter
from server.routes.property import router as PropertyRouter
from server.routes.booking_history import router as BookingRouter
from server.routes.landingpage import router as LandingPageRouter
from server.routes.admin import router as AdminRouter
from server.routes.affiliate import router as AffiliateRouter
from server.routes.social_auth import router as socialRouter


from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from .settings import CONFIG_SETTINGS
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_config():
    return CONFIG_SETTINGS


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(UserRouter, tags=["Users"], prefix="/users")
app.include_router(socialRouter, tags=["social_auth"], prefix="/social")

app.include_router(PropertyRouter, tags=["Property"], prefix="/property")
app.include_router(BookingRouter, tags=["Booking"], prefix="/booking")
app.include_router(LandingPageRouter, tags=["Landing Page"], prefix="/landing")

app.include_router(AdminRouter, tags=["Admin"], prefix="/admin")
app.include_router(AffiliateRouter, tags=["Affiliate"], prefix="/affiliate")


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def read_root() -> dict:

    return {"message": "Welcome to EVC_Apartment"}
