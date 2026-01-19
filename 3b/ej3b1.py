"""
Enunciado:
En este ejercicio aprenderás a utilizar SQLAlchemy como ORM (Object-Relational Mapper)
independiente de cualquier framework web. SQLAlchemy es una biblioteca potente
que permite trabajar con bases de datos relacionales utilizando objetos de Python.

Tarea:
Implementa un sistema simple de gestión de biblioteca utilizando SQLAlchemy para:
1. Crear modelos para Libros y Autores con una relación entre ellos
2. Realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
3. Realizar consultas básicas y avanzadas

Este ejercicio se enfoca en SQLAlchemy Core y ORM sin depender de Flask u otro framework web.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload, relationship, sessionmaker

# Crea el motor de base de datos (usamos SQLite en memoria para simplificar)
engine = create_engine("sqlite:///:memory:", echo=True)

# Crea la clase Base para los modelos declarativos
Base = declarative_base()


# Define aquí tus modelos
# Debes crear al menos:
# 1. Un modelo Author (autor) con campos id, name (nombre) y una relación con Book
# 2. Un modelo Book (libro) con campos id, title (título), year (año, opcional) y una relación con Author


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=True)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")


# Función para configurar la base de datos
def setup_database():
    """Configura la base de datos y crea las tablas"""
    Base.metadata.create_all(engine)


# Función para crear datos de ejemplo
def create_sample_data(session):
    """Crea datos de ejemplo en la base de datos"""
    author1 = Author(name="Gabriel García Márquez")
    author2 = Author(name="Isabel Allende")

    book1 = Book(title="Cien años de soledad", year=1967, author=author1)
    book2 = Book(title="El amor en los tiempos del cólera", year=1985, author=author1)
    book3 = Book(title="La casa de los espíritus", year=1982, author=author2)

    session.add_all([author1, author2, book1, book2, book3])
    session.commit()


# Funciones para operaciones CRUD
def create_book(session, title, author_name, year=None):
    """
    Crea un nuevo libro con su autor
    Si el autor ya existe, se utiliza el existente
    """
    author = session.query(Author).filter_by(name=author_name).first()

    if author is None:
        author = Author(name=author_name)
        session.add(author)
        session.flush()  # asegura author.id

    book = Book(title=title, year=year, author=author)
    session.add(book)
    session.commit()

    return book


def get_all_books(session):
    """Obtiene todos los libros con sus autores"""
    return session.query(Book).options(joinedload(Book.author)).all()


def get_book_by_id(session, book_id):
    """Obtiene un libro específico por su ID"""
    # Busca un libro por su ID y retórnalo
    # Si no existe, retorna None
    return session.query(Book).filter_by(id=book_id).first()


def update_book(session, book_id, new_title=None, new_year=None):
    """Actualiza la información de un libro existente"""
    book = session.query(Book).filter_by(id=book_id).first()

    if book is None:
        return None

    if new_title is not None:
        book.title = new_title
    if new_year is not None:
        book.year = new_year

    session.commit()
    return book


def delete_book(session, book_id):
    """Elimina un libro de la base de datos"""
    book = session.query(Book).filter_by(id=book_id).first()

    if book:
        session.delete(book)
        session.commit()


def find_books_by_author(session, author_name):
    """Busca libros por el nombre del autor"""
    return (
        session.query(Book).join(Book.author).filter(Author.name == author_name).all()
    )


# Función principal para demostrar el uso de SQLAlchemy
def main():
    """Función principal que demuestra el uso de SQLAlchemy"""
    # Crea un motor y una sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Configura la base de datos
    setup_database()

    try:
        # Crea datos de ejemplo
        create_sample_data(session)

        # Demuestra las operaciones CRUD
        print("\n--- Todos los libros ---")
        books = get_all_books(session)
        for book in books:
            print(f"Libro: {book.title}, Año: {book.year}, Autor: {book.author.name}")

        print("\n--- Crear un nuevo libro ---")
        new_book = create_book(
            session, "Nuevo libro de ejemplo", "Autor de Prueba", 2025
        )
        print(f"Libro creado: {new_book.title} por {new_book.author.name}")

        print("\n--- Buscar libro por ID ---")
        book = get_book_by_id(session, 1)
        if book:
            print(f"Libro encontrado: {book.title} por {book.author.name}")

        print("\n--- Actualizar libro ---")
        updated_book = update_book(
            session, 1, new_title="Título Actualizado", new_year=2026
        )
        if updated_book:
            print(f"Libro actualizado: {updated_book.title}, Año: {updated_book.year}")

        print("\n--- Buscar libros por autor ---")
        author_books = find_books_by_author(session, "Autor de Prueba")
        for book in author_books:
            print(f"Libro: {book.title}, Año: {book.year}")

        print("\n--- Eliminar libro ---")
        delete_book(session, 2)
        print("Libro eliminado. Lista actualizada de libros:")
        for book in get_all_books(session):
            print(f"Libro: {book.title}, Autor: {book.author.name}")
    finally:
        # Cierra la sesión
        session.close()


if __name__ == "__main__":
    main()
