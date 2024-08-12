from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password, get_current_user, get_password_hash, create_reset_token, verify_reset_token
from app.crud import crud_user
from app.schemas import user
from app.db.database import get_db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordRequestForm # Tambahkan OAuth2PasswordRequestForm 
@router.post("/login", response_model=user.Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    db_user = crud_user.get_user_by_username(db, name=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=db_user.name)
     # Menyimpan token ke kolom remember_token
    db_user.remember_token = access_token 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
#Menambahkan user_id ke response
    return {"access_token": access_token, "token_type": "bearer", "user_id": db_user.id}



# @router.post("/register", response_model=user.User)
# def register(db: Session = Depends(get_db), user_data: user.UserCreate = Body(...)):
#     db_user = crud_user.get_user_by_email(db, email=user_data.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud_user.create_user(db=db, user=user_data)

@router.post("/register", response_model=user.User)
def register(db: Session = Depends(get_db), user_data: user.UserCreate = Body(...)):
    # Validasi apakah email sudah terdaftar
    if crud_user.get_user_by_email(db, email=user_data.email): 
        raise HTTPException(status_code=400, detail="Email already registered")

    # Jika email belum terdaftar, buat user baru
    return crud_user.create_user(db=db, user=user_data)

security = HTTPBearer()
@router.post("/logout")
def logout(
    response: Response, 
    current_user: user.User = Depends(get_current_user)
):
    # Menghapus remember_token dari database
    current_user.remember_token = None  
    db = next(get_db())  # Mendapatkan session database
    db.add(current_user)
    db.commit()
    response.delete_cookie("access_token")  # Menghapus cookie access_token jika ada
    return {"message": "Successfully logged out"}

@router.put("/change-password")
def change_password(
    current_password: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user)
):
    """
    Mengubah password pengguna yang sedang login.
    """
    db_user = crud_user.get_user(db, user_id=current_user.id)
    if not verify_password(current_password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    hashed_password = get_password_hash(new_password)
    crud_user.update_password(db, user_id=current_user.id, hashed_password=hashed_password)
    return {"message": "Password updated successfully"}
    #return db_user
@router.post("/forgot-password")
def forgot_password(
    email: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_user = crud_user.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist",
        )
    reset_token = create_reset_token(email=db_user.email)
    reset_url = f"https://home.serverdata.my.id/reset-password?token={reset_token}"
    
    send_reset_email(email=db_user.email, reset_url=reset_url)
    
    return {"message": "Password reset email sent"}

@router.put("/reset-password")
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db)
):
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    db_user = crud_user.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = get_password_hash(new_password)
    crud_user.update_password(db, user_id=db_user.id, hashed_password=hashed_password)
    return {"message": "Password updated successfully"}

def send_reset_email(email: str, reset_url: str):
    from_address = "hello@serverdata.my.id"
    to_address = email
    subject = "Password Reset Request"
    
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    
    body = f"Click the link to reset your password: {reset_url}"
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(settings.MAIL_HOST, int(settings.MAIL_PORT)) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(from_address, to_address, msg.as_string())