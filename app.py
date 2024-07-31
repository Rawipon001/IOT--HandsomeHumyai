from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Books Endpoints
@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    new_book = models.Book(
        title=book['title'],
        author=book['author'],
        year=book['year'],
        is_published=book['is_published'],
        description=book['description'],
        synopsis=book['synopsis'],
        category=book['category']
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    response.status_code = 201
    return new_book

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if existing_book:
        for key, value in book.items():
            setattr(existing_book, key, value)
        db.add(existing_book)
        db.commit()
        db.refresh(existing_book)
        return existing_book
    raise HTTPException(status_code=404, detail="Book not found")

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_to_delete = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book_to_delete:
        db.delete(book_to_delete)
        db.commit()
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# Menus Endpoints
@router_v1.get('/menus')
async def get_menus(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router_v1.post('/menus')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    new_menu = models.Menu(
        drink_name=menu['drink_name'],
        price=menu['price'],
        image=menu['image']
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    response.status_code = 201
    return new_menu

@router_v1.get('/menus/{menu_id}')
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

# Orders Endpoints
@router_v1.post('/menus/{menu_id}/order')
async def create_order(menu_id: int, order: dict, response: Response, db: Session = Depends(get_db)):
    # ตรวจสอบว่า menu_id มีอยู่ในฐานข้อมูลหรือไม่
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    # สร้างอ็อบเจ็กต์คำสั่งซื้อใหม่
    new_order = models.Order(
        menu_id=menu_id,
        quantity=order['quantity'],
        notes=order['notes'],
        menu_name = menu.drink_name,
        menu_Image = menu.image,
    )
    
    # เพิ่มคำสั่งซื้อใหม่ในฐานข้อมูล
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # ตั้งค่าสถานะของคำตอบเป็น 201 Created
    response.status_code = 201
    return new_order
    
@router_v1.get('/orders')
async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
