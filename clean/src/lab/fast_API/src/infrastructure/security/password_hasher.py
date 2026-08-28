import bcrypt


class BcryptPasswordHasher:
    def hash(self, password: str) -> str:
        hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hash_bytes.decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
