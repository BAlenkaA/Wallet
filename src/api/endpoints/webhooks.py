from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from config import webhook_settings
from crud.account import account_crud
from crud.replenishment import replenishment_crud
from databases.database import get_async_session
from loggers import logger
from schemas.account import AccountCreateDB, AccountUpdate
from schemas.replenishment import ReplenishmentCreateDB, WebhookRequest
from utilities.validators import existing_transaction, verify_signature

router = APIRouter()


@router.post("/payment")
async def handle_payment_webhook(
    webhook_data: WebhookRequest, db: AsyncSession = Depends(get_async_session)
):
    if not verify_signature(webhook_data, webhook_settings.WEBHOOK_SECRET_KEY):
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        async with db.begin():
            transaction = await existing_transaction(
                webhook_data.transaction_id, db)
            if transaction:
                raise HTTPException(
                    status_code=400, detail="Transaction already exists"
                )

            account = await account_crud.get(webhook_data.account_id, db)
            logger.info(f"account found: {account}")
            if account and account.user_id != webhook_data.user_id:
                raise HTTPException(
                    status_code=400, detail="Account does not belong to user"
                )

            if not account:
                create_data = {
                    "id": webhook_data.account_id,
                    "user_id": webhook_data.user_id,
                    "balance": webhook_data.amount,
                }
                account = await account_crud.create(
                    AccountCreateDB(**create_data), db, commit=False
                )
            else:
                update_data = {
                    "balance": webhook_data.amount + account.balance
                }
                account = await account_crud.update(
                    account, AccountUpdate(**update_data), db, commit=False
                )
            logger.info(f"account found: {account}")
            replenishment_data = {
                "amount": webhook_data.amount,
                "transaction_id": webhook_data.transaction_id,
                "user_id": webhook_data.user_id,
            }
            await replenishment_crud.create(
                ReplenishmentCreateDB(**replenishment_data), db, commit=False
            )

        return {
            "status": "success",
            "message": "Payment processed successfully",
            "transaction_id": webhook_data.transaction_id,
            "new_balance": account.balance,
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in payment webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing payment: {str(e)}"
        )
