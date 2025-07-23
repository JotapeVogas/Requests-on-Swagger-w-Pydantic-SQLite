from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3

app = FastAPI()
DATABASE = "banco.db"

class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

def get_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def iniciar_banco():
    conn = get_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 
        usuarios (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nome TEXT NOT NULL,
           email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.get("/", response_model=dict) 
def home():
    return {"message": "API de Usuários"}

@app.post("/usuario", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate):
    conn = get_banco()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios(nome, email) VALUES (?, ?)",
        (usuario.nome, usuario.email)
    )
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    return {"id": usuario_id, **usuario.model_dump()}

@app.get("/usuario")
def listar():
    conn = get_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return {"usuarios" : [dict(usuario) for usuario in usuarios]}

@app.get("/usuario/{usuario_id}")
def buscar_por_id(usuario_id: int):
    conn = get_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        return dict(usuario)
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.put("/usuario/{usuario_id}", response_model=Usuario)
def update_user(usuario_id: int, usuario: UsuarioCreate):
    conn = get_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    cursor.execute(
        "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
        (usuario.nome, usuario.email, usuario_id)
    )
    conn.commit()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    usuario_atualizado = cursor.fetchone()
    conn.close()
    return dict(usuario_atualizado)
    
    
@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usuario_id: int):
    conn = get_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()
    return None

if __name__ == "__main__":
    import uvicorn
    iniciar_banco()
    uvicorn.run(
        "seu_arquivo:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4
    )