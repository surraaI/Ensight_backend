from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.article import ArticleService
from app.schemas.article import Article, ArticleCreate, ArticleUpdate
from app.models.user import User, Role
from app.dependencies import get_current_user

router = APIRouter(prefix="/article", tags=["articles"])

# Custom dependency for role-based access
def require_role(roles: List[Role]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

@router.get("/{category}", response_model=List[Article])
async def get_articles_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    articles = ArticleService.get_articles_by_category(db, category)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this category")
    return articles

@router.get("/{category}/{subcategory}", response_model=List[Article])
async def get_articles_by_subcategory(
    category: str,
    subcategory: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    articles = ArticleService.get_articles_by_subcategory(db, category, subcategory)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this subcategory")
    return articles

@router.get("/{category}/{subcategory}/{slug}", response_model=Article)
async def get_article_by_slug(
    category: str,
    subcategory: str,
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = ArticleService.get_article_by_slug(db, category, subcategory, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.WRITER, Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]))
):
    article_data = article.dict()
    article_data["author"] = current_user.id
    new_article = ArticleService.create_article(db, article_data)
    return new_article

@router.patch("/{id}", response_model=Article)
async def update_article(
    id: str,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = ArticleService.get_article_by_id(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author != current_user.id and current_user.role not in [Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to edit this article")
    updated_article = ArticleService.update_article(db, id, article_update)
    return updated_article

@router.patch("/{id}/approve", response_model=Article)
async def approve_article(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]))
):
    article = ArticleService.approve_article(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article