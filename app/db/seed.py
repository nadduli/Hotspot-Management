import asyncio
import logging
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed():
    async with SessionLocal() as db:
        try:
            admin_email = "admin@hotspot.com"
            admin = await User.fetch_unique(db, email=admin_email)
            if not admin:
                logger.info(f"Creating super admin: {admin_email}")
                admin = User(
                    email=admin_email,
                    full_name="System Administrator",
                    password_hash=hash_password("Admin@123"),
                )
                await admin.insert(db, commit=False)

            await db.commit()
            logger.info("✅ Database successfully seeded!")

        except Exception as e:
            await db.rollback()
            logger.error(f"Seeding failed: {str(e)}")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
