import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


ADMIN = int(os.getenv("ADMIN"))

conn = None
async def connection():
    global conn
    conn =  await asyncpg.create_pool(
        user=os.getenv('DATABASE_USER'),
        database=os.getenv('DATABASE'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'),
    )

async def create_table():
    try:
        await conn.execute("""CREATE TABLE  IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) UNIQUE,
                        tg_id BIGINT UNIQUE,
                        full_name VARCHAR(255),
                        age SMALLINT CHECK(age>0),
                        address VARCHAR(255) ,
                        contact VARCHAR(17)
        );
        """)
        await conn.execute("""CREATE TABLE  IF NOT EXISTS items(
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) ,
                        description TEXT,
                        price NUMERIC(10, 2) CHECK(price>0),
                        photo_url VARCHAR(255)
        );
        """)
        await conn.execute("""CREATE TABLE  IF NOT EXISTS orders(
                        id SERIAL PRIMARY KEY,
                        item_id INT REFERENCES items(id) ON DELETE SET NULL,
                        user_id BIGINT REFERENCES users(tg_id)   
        );
        """)
        print('tables created ')
    except Exception as e:
        print(e, 'tables bneed debug')
    

    
async def register(username:str, full_name:str, age:int, address: str, contact:str, tg_id: int):
    try:
        q = await conn.execute(
            'INSERT INTO users(username, full_name, age, address, contact, tg_id) VALUES($1, $2, $3, $4, $5, $6)',
        username, full_name, age, address, contact, tg_id
        )
        print(q)
    except Exception as e:
        print(e, 'didnt insert into users')

async def get_user(tg_id):
    try:
        q = await conn.fetchrow(
        'select * from users where tg_id = $1', tg_id
        )
        print(q)
        return q
    except Exception as e:
        print(e, 'didnt insert into users')


async def get_items():
    try:
        items = await conn.fetch('SELECT * FROM items')
        return items
    except Exception as e:
        print(e)

async def get_item_by_id(item_id):
    try:
        item = await conn.fetchrow('SELECT * FROM items where id = $1', item_id)
        return item
    except Exception as e:
        print(e)

async def add_item(title, description, price, photo_url):
    try:
        q = await conn.execute(
            'INSERT INTO items(title, description, price, photo_url)'
            'VALUES ($1, $2, $3, $4)',
            title, description, price, photo_url
        )
        print(q)
        return q
    except Exception as e:
        print(e)


async def add_order(user_id, item_id):
    try:
        q = await conn.execute(
            'INSERT INTO orders(user_id, item_id)'
            'VALUES ($1, $2)',
            user_id, item_id
        )
        print(q)
        return q
    except Exception as e:
        print(e)




async def get_my_orders(user_id):
    try:
        items = await conn.fetch('SELECT i.title as i_title, i.price ' 
        'as i_price from items as i join orders as o on o.item_id = i.id where user_id = $1 ', user_id)
        print(items)
        return items
    except Exception as e:
        print(e)