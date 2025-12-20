import asyncio
import logging
from app.db.session import SessionLocal
from app.models.auth import Role
from app.models.branch import Branch
from app.models.organization import Organization
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed():
    async with SessionLocal() as db:
        try:
            # 1. Seed Roles
            logger.info("Seeding roles...")
            role_map = {}
            for role_name in ["ADMIN", "AGENT"]:
                role = await Role.fetch_unique(db, name=role_name)
                if not role:
                    role = Role(name=role_name, description=f"Default {role_name}")
                    await role.insert(db, commit=False)
                    await db.flush()  # Populate role.id
                role_map[role_name] = role

            # 2. Seed Organization
            logger.info("Seeding organization...")
            org = await Organization.fetch_unique(db, name="Main Hotspot Org")
            if not org:
                org = Organization(name="Main Hotspot Org", description="Primary Management Org")
                await org.insert(db, commit=False)
                await db.flush()  # Populate org.id for the branch
            
            # 3. Seed Branch
            logger.info("Seeding branch...")
            branch = await Branch.fetch_unique(db, name="Headquarters")
            if not branch:
                # org.id is now guaranteed to be available because of the flush above
                branch = Branch(
                    name="Headquarters", 
                    organization_id=org.id,
                    address="Default Main Office"
                )
                await branch.insert(db, commit=False)
                await db.flush()  # Populate branch.id for the user

            # 4. Seed Admin User
            admin_email = "admin@hotspot.com"
            admin = await User.fetch_unique(db, email=admin_email)
            if not admin:
                logger.info(f"Creating super admin: {admin_email}")
                admin = User(
                    email=admin_email,
                    full_name="System Administrator",
                    # Note: Use a real hash here in production!
                    hashed_password="hashed_password_here",
                    role_id=role_map["ADMIN"].id,
                    branch_id=branch.id,
                )
                await admin.insert(db, commit=False)

            # Final Step: Commit the entire transaction
            await db.commit()
            logger.info("✅ Database successfully seeded!")

        except Exception as e:
            await db.rollback()
            logger.error(f"Seeding failed: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(seed())