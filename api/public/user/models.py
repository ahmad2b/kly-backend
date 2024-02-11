from enum import Enum
from typing import Annotated
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from typing import TYPE_CHECKING


# if TYPE_CHECKING:
#     from api.public.url.models import URL


# class User(SQLModel, table=True):
#     id: Optional[str] = Field(
#         default=None,
#         primary_key=True,
#         nullable=False,
#     )
#     username: str = Field(nullable=False, index=True, unique=True)
#     email_address: str = Field(nullable=False, index=True, unique=True)
#     # hash_password: str = Field(nullable=False)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
#     updated_at: Optional[datetime] = Field(default_factory=None)
#     deleted_at: Optional[datetime] = Field(default_factory=None)

#     urls: List["URL"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    email_address: EmailStr
    username: Annotated[str, Field(max_length=50, min_length=6)]
    password: Annotated[str, Field(max_length=50, min_length=8)]


class UserCredentials(SQLModel):
    userIdentifier: str = Field(..., alias="username_or_email")
    password: str


class PasswordHasher(Enum):
    bcrypt = "bcrypt"
    bcrypt_sha256_django = "bcrypt_sha256_django"
    md5 = "md5"
    pbkdf2_sha256 = "pbkdf2_sha256"
    pbkdf2_sha256_django = "pbkdf2_sha256_django"
    phpass = "phpass"
    scrypt_firebase = "scrypt_firebase"
    sha256 = "sha256"
    argon2i = "argon2i"
    argon2id = "argon2id"


class Verification(BaseModel):
    status: str
    strategy: str
    attempts: Optional[int]
    expire_at: Optional[str]


class EmailAddress(BaseModel):
    id: str
    object: str
    email_address: str
    reserved: bool
    verification: Verification
    linked_to: List[str]


class UserSignupResponse(SQLModel):
    id: str
    object: str
    username: str
    first_name: str
    last_name: str
    image_url: str
    has_image: bool
    primary_email_address_id: str
    primary_phone_number_id: Optional[str]
    primary_web3_wallet_id: Optional[str]
    password_enabled: bool
    two_factor_enabled: bool
    totp_enabled: bool
    backup_code_enabled: bool
    email_addresses: List[EmailAddress]
    phone_numbers: List[Optional[str]]
    web3_wallets: List[Optional[str]]
    external_accounts: List[Optional[str]]
    saml_accounts: List[Optional[str]]
    public_metadata: dict
    private_metadata: dict
    unsafe_metadata: dict
    external_id: str
    last_sign_in_at: Optional[str]
    banned: bool
    locked: bool
    lockout_expires_in_seconds: Optional[int]
    verification_attempts_remaining: int
    created_at: int
    updated_at: int
    delete_self_enabled: bool
    create_organization_enabled: bool
    last_active_at: Optional[str]
    profile_image_url: str
