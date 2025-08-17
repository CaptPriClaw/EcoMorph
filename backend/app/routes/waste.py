# backend/app/routes/waste.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas import waste_schema, user_schema
from ..services import waste_service, point_service
from ..database import get_db
from ..services.auth_service import get_current_active_user
from ..models.points import PointReason

router = APIRouter(
    prefix="/waste",
    tags=["Waste Management"]
)

@router.post("/", response_model=waste_schema.Waste, status_code=status.HTTP_201_CREATED)
def create_waste_submission(
    waste: waste_schema.WasteCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Creates a new waste submission for the logged-in user.
    """
    return waste_service.create_waste(db=db, waste=waste, uploader_id=current_user.id)


@router.get("/my-submissions", response_model=List[waste_schema.Waste])
def read_user_waste_submissions(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieves all waste submissions for the currently authenticated user.
    """
    wastes = waste_service.get_wastes_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return wastes


@router.get("/{waste_id}", response_model=waste_schema.Waste)
def read_waste_submission(
    waste_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Retrieves a single waste submission by its ID.
    Ensures that the user requesting the item is its owner.
    """
    waste = waste_service.get_waste(db, waste_id=waste_id)
    if waste is None:
        raise HTTPException(status_code=404, detail="Waste item not found")
    if waste.uploader_id != current_user.id:
        # In a real app, an admin might be allowed to view this
        raise HTTPException(status_code=403, detail="Not authorized to view this item")
    return waste


@router.put("/{waste_id}/status", response_model=waste_schema.Waste)
def update_waste_status(
    waste_id: int,
    update_data: waste_schema.WasteUpdate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Updates the status of a waste item. (Primarily for Admins)
    If a waste item is approved, award points to the uploader.
    """
    # Role-based access control
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admins can change waste status.")

    updated_waste = waste_service.update_waste_status(db, waste_id=waste_id, status=update_data.status)
    if not updated_waste:
        raise HTTPException(status_code=404, detail="Waste item not found")

    # If the waste is approved, award points to the original uploader
    if updated_waste.status == waste_schema.WasteStatus.APPROVED:
        point_service.add_points(
            db=db,
            user_id=updated_waste.uploader_id,
            reason=PointReason.WASTE_UPLOAD_APPROVED,
            description=f"Approved: {updated_waste.material_type}"
        )

    return updated_waste